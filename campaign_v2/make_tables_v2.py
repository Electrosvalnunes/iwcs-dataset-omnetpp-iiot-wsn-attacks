#!/usr/bin/env python3
"""
make_tables_v2.py: features_v2.csv -> tables/table9_v2.tex + tables/table9_v2_checks.txt

    python3 -I make_tables_v2.py [--features features_v2.csv] [--cells cells.csv]
                                 [--results results] [--tables-dir ../manuscript_v2/tables]
                                 [--expected-runs 30] [--require-complete]

Só usa a biblioteca padrão do Python 3.

table9_v2.tex
    Uma linha por célula (topologia x condição), com n (número de runs) e média ± desvio-padrão
    amostral (ddof = 1) das 8 features de extract_v2.py. A energia é Energy_Consumed_J, que já
    é a energia MÉDIA POR SENSOR (J/nó, inclui o warmup). Com n = 1, o desvio é "--".
    A topologia é rotulada pelo número total de nós (sensores + sink), como no manuscrito:
    Grid35 -> "Grid 36", e assim por diante.

table9_v2_checks.txt
    1. Proveniência: sha256 do CSV, número de linhas e dataset_version.
    2. Valores em falta: vazios, NaN ou inf, por coluna.
    3. Duplicados: (config, run) e sca_sha256.
    4. Uma linha por run aceite: o conjunto (config, run) do CSV tem de ser igual ao conjunto
       dos marcadores <config>-<run>.ok em results/; seed == run.
    5. Cobertura: n por célula face a --expected-runs, com a lista das runs em falta.
    6. Intervalos: PDR em [0, 100] (ver abaixo o caso PDR > 100); atraso > 0; throughput >= 0; energia por nó em (0, 1500];
       Energy_Total_J = |H| * Energy_Consumed_J; contagens inteiras >= 0; RSSI em [-85, 0];
       DIS_Count <= DIS_Total; DAO_Forwarded_Total <= DAO_Received_Total.
    7. Variância por célula de Avg_RSSI_dBm, DIS_Count e DIS_Total (desvio, mínimo e máximo).

PDR > 100 (efeito de fronteira da janela [W]): tx e rx contam só a partir do fim do warmup
    (80 s), por isso um pacote enviado antes dos 80 s e recebido depois conta em rx e não em tx.
    A PDR é publicada sem corte. Se o excesso rx - tx (rx = Throughput_kbps * T_meas / 8 / 56 B,
    tx = 100 * rx / PDR) estiver em (0, |H|], é AVISO: com sendInterval >= 6 s e atrasos de
    milissegundos, cada sensor tem no máximo um pacote a atravessar a fronteira. Acima disso é
    FALHA. Caso verificado: Grid48_Normal run 14, rx = 3033, tx = 3032; o pacote foi enviado em
    t = 79.992 s e recebido em t = 80.013 s (repetição da run até 120 s com o vetor
    endToEndDelay da sink).

Código de saída: 1 se houver FALHAS (pontos 2, 3, 4 e 6). A cobertura incompleta é só um
AVISO, exceto com --require-complete.
"""
import argparse, csv, glob, hashlib, math, os, statistics, sys

GENERATOR_VERSION = "1.2.0"
T_MEAS_S = 3520.0   # janela [W] de extract_v2.py: 80-3600 s
APP_BYTES = 56      # bytes de aplicação por pacote legítimo
FEATURES = ["Avg_RSSI_dBm", "DIO_Count", "DIS_Count", "Rank_Changes", "PDR_percent",
            "Avg_Delay_ms", "Throughput_kbps", "Energy_Consumed_J"]
FMT = {"Avg_RSSI_dBm": 3, "DIO_Count": 1, "DIS_Count": 1, "Rank_Changes": 1,
       "PDR_percent": 2, "Avg_Delay_ms": 2, "Throughput_kbps": 3, "Energy_Consumed_J": 3}
HEAD = {"Avg_RSSI_dBm": "RSSI (dBm)", "DIO_Count": "DIO", "DIS_Count": "DIS",
        "Rank_Changes": "Rank ch.", "PDR_percent": "PDR (\\%)", "Avg_Delay_ms": "Delay (ms)",
        "Throughput_kbps": "Thr. (kbps)", "Energy_Consumed_J": "Energy (J/node)"}
INT_COLS = ["DIO_Count", "DIS_Count", "Rank_Changes", "DIS_Total", "DAO_Sent_Total",
            "DAO_Received_Total", "DAO_AckReceived_Total", "DAO_Forwarded_Total", "DAO_Dropped_Total"]
# ordem das colunas da Tabela 9, igual à do placeholder manuscript_v2/tables/table9_v2.tex
TABLE_COLS = ["PDR_percent", "Avg_Delay_ms", "Throughput_kbps", "Energy_Consumed_J",
              "Avg_RSSI_dBm", "DIO_Count", "DIS_Count", "Rank_Changes"]
COND_ORDER = ["Normal", "Flooding", "Blackhole", "Wormhole", "Backoff"]   # ordem do manuscrito


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def num(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return float("nan")
    return v


def ranges(xs):
    """[0,1,2,5,7,8] -> '0-2,5,7-8'"""
    out, i = [], 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1:
            j += 1
        out.append(f"{xs[i]}" if i == j else f"{xs[i]}-{xs[j]}")
        i = j + 1
    return ",".join(out)


def mean_sd(vals, nd):
    if not vals or not all(math.isfinite(v) for v in vals):
        return "NaN"            # nunca deve acontecer: a secção 2 das verificações reporta-o como FALHA
    m = statistics.fmean(vals)
    if len(vals) < 2:
        return f"{m:.{nd}f} $\\pm$ --"
    return f"{m:.{nd}f} $\\pm$ {statistics.stdev(vals):.{nd}f}"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--features", default=os.path.join(here, "features_v2.csv"))
    ap.add_argument("--cells", default=os.path.join(here, "cells.csv"))
    ap.add_argument("--results", default=os.path.join(here, "results"))
    ap.add_argument("--tables-dir", default=os.path.join(os.path.dirname(here), "manuscript_v2", "tables"))
    ap.add_argument("--expected-runs", type=int, default=30)
    ap.add_argument("--require-complete", action="store_true")
    a = ap.parse_args()

    with open(a.cells, newline="", encoding="utf-8") as fh:
        cells = list(csv.DictReader(fh))
    by_cfg = {c["config"]: c for c in cells}
    with open(a.features, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        cols = rd.fieldnames or []
        rows = list(rd)

    fails, warns, out = [], [], []
    P = out.append
    P(f"# Verificações de {os.path.basename(a.features)} (make_tables_v2.py {GENERATOR_VERSION})")
    P(f"features_sha256: {sha256(a.features)}")
    P(f"linhas: {len(rows)}")
    P(f"dataset_version: {sorted({r.get('dataset_version', '') for r in rows})}")

    # 2. valores em falta
    P("\n## 2. Valores em falta (vazio / NaN / inf)")
    need = ["topology", "condition", "run", "seed", "config", "dataset_version"] + FEATURES
    for c in need:
        if c not in cols:
            fails.append(f"coluna '{c}' ausente"); P(f"  {c}: COLUNA AUSENTE")
    miss = {}
    for c in cols:
        bad = [r for r in rows if r[c] == "" or (c not in ("topology", "condition", "config",
               "dataset_version", "cell_id", "sca_sha256") and not math.isfinite(num(r[c])))]
        if bad:
            miss[c] = len(bad)
    if miss:
        for c, n in miss.items():
            P(f"  {c}: {n} linha(s)")
        fails.append(f"valores em falta: {miss}")
    else:
        P("  nenhum")

    # 3. duplicados
    P("\n## 3. Duplicados")
    seen, dups = {}, []
    for r in rows:
        k = (r["config"], r["run"])
        if k in seen:
            dups.append(k)
        seen[k] = r
    shas = [r.get("sca_sha256", "") for r in rows]
    dsha = len(shas) - len(set(shas))
    P(f"  (config, run) duplicados: {len(dups)} {dups[:10]}")
    P(f"  sca_sha256 duplicados: {dsha}")
    if dups or dsha:
        fails.append(f"duplicados: {len(dups)} (config,run), {dsha} sha256")

    # 4. uma linha por run aceite
    P("\n## 4. Uma linha por run aceite (.ok em results/)")
    # .ok criados depois do CSV (a campanha continua a correr) não contam como falha
    t_csv = os.path.getmtime(a.features)
    oks, later = set(), []
    for f in glob.glob(os.path.join(a.results, "*.ok")):
        b = os.path.basename(f)[:-3]
        cfg, _, run = b.rpartition("-")
        if cfg in by_cfg:
            (later.append((cfg, run)) if os.path.getmtime(f) > t_csv else oks.add((cfg, run)))
    csvk = set(seen)
    only_ok, only_csv = sorted(oks - csvk), sorted(csvk - oks - set(later))
    P(f"  runs aceites (.ok) até à escrita do CSV: {len(oks)}; linhas no CSV: {len(csvk)}")
    P(f"  runs terminadas depois do CSV (ignoradas): {len(later)} {sorted(later)[:10]}")
    P(f"  aceites sem linha no CSV: {len(only_ok)} {only_ok[:10]}")
    P(f"  linhas sem .ok: {len(only_csv)} {only_csv[:10]}")
    if only_ok or only_csv:
        fails.append(f"CSV != runs aceites ({len(only_ok)} em falta, {len(only_csv)} a mais)")
    badseed = [(r["config"], r["run"]) for r in rows if r["seed"] != r["run"]]
    P(f"  seed != run: {len(badseed)}")
    if badseed:
        fails.append(f"seed != run em {len(badseed)} linhas")
    unknown = sorted({r["config"] for r in rows} - set(by_cfg))
    if unknown:
        fails.append(f"configs fora de cells.csv: {unknown}")

    # agrupar
    groups = {c["config"]: [] for c in cells}
    for r in rows:
        if r["config"] in groups:
            groups[r["config"]].append(r)

    # 5. cobertura
    P(f"\n## 5. Cobertura (esperado: runs 0-{a.expected_runs - 1} por célula)")
    incomplete = 0
    for c in cells:
        runs = {int(r["run"]) for r in groups[c["config"]]}
        missing = [i for i in range(a.expected_runs) if i not in runs]
        extra = sorted(i for i in runs if i >= a.expected_runs)
        if missing or extra:
            incomplete += 1
        txt = "completa" if not missing else f"faltam {len(missing)}: {ranges(missing)}"
        P(f"  {c['cell_id']:<14} n={len(runs):>2}/{a.expected_runs}  {txt}{'  EXTRA ' + str(extra) if extra else ''}")
    if incomplete:
        (fails if a.require_complete else warns).append(f"{incomplete} célula(s) incompletas")

    # 6. intervalos
    P("\n## 6. Intervalos")
    rng, boundary = [], []
    for r in rows:
        k = f"{r['config']}-{r['run']}"
        v = {c: num(r[c]) for c in cols if c not in ("topology", "condition", "config",
                                                     "dataset_version", "cell_id", "sca_sha256")}
        H = int(by_cfg[r["config"]]["n_nodes"]) - 1 if r["config"] in by_cfg else None
        pdr_ok = 0 <= v["PDR_percent"] <= 100
        if v["PDR_percent"] > 100 and H:
            rx = v["Throughput_kbps"] * T_MEAS_S * 1000 / 8 / APP_BYTES
            tx = 100 * rx / v["PDR_percent"]
            excess = round(rx - tx)
            if 0 < excess <= H:
                pdr_ok = True
                boundary.append(f"{k}: PDR {v['PDR_percent']:.4f} %, rx - tx = {excess} pacote(s) (<= |H| = {H})")
        checks = [
            (pdr_ok, "PDR fora de [0,100] e não explicável pela fronteira do warmup"),
            (v["Avg_Delay_ms"] > 0, "atraso <= 0"),
            (v["Throughput_kbps"] >= 0, "throughput < 0"),
            (0 < v["Energy_Consumed_J"] <= 1500, "energia por nó fora de (0,1500]"),
            (-85 <= v["Avg_RSSI_dBm"] <= 0, "RSSI fora de [-85,0]"),
        ]
        for c in INT_COLS:
            if c in v:
                checks.append((v[c] >= 0 and float(v[c]).is_integer(), f"{c} não é inteiro >= 0"))
        if "DIS_Total" in v:
            checks.append((v["DIS_Count"] <= v["DIS_Total"], "DIS_Count > DIS_Total"))
        if "DAO_Forwarded_Total" in v:
            checks.append((v["DAO_Forwarded_Total"] <= v["DAO_Received_Total"], "DAO fwd > rx"))
        if "Energy_Total_J" in v and H:
            checks.append((abs(v["Energy_Total_J"] - H * v["Energy_Consumed_J"]) <= 1e-5 * max(1, v["Energy_Total_J"]) + H * 1e-6,
                           f"Energy_Total_J != {H} x Energy_Consumed_J"))
        for ok, msg in checks:
            if not ok:
                rng.append(f"{k}: {msg}")
    P(f"  violações: {len(rng)}")
    for x in rng[:50]:
        P(f"    {x}")
    if rng:
        fails.append(f"{len(rng)} violações de intervalo")
    P(f"  PDR > 100 por pacotes na fronteira do warmup (aviso, valor publicado sem corte): {len(boundary)}")
    for x in boundary:
        P(f"    {x}")
    if boundary:
        P("    tx e rx contam só a partir de 80 s; um pacote enviado antes e recebido depois conta só em rx.")
        warns.append(f"{len(boundary)} run(s) com PDR > 100 % por pacotes na fronteira do warmup (ver secção 6)")

    # 7. variância
    P("\n## 7. Variância por célula (desvio-padrão amostral; min..max)")
    P(f"  {'cell_id':<14} {'n':>3}  {'sd RSSI':>9} {'RSSI min..max':>21}  {'sd DIS':>7} {'DIS min..max':>12}  {'sd DIS_T':>8} {'DIS_T min..max':>14}")
    zero = []
    for c in cells:
        g = groups[c["config"]]
        if not g:
            P(f"  {c['cell_id']:<14} {0:>3}  (sem runs)")
            continue
        def s(col):
            vals = [num(r[col]) for r in g]
            sd = statistics.stdev(vals) if len(vals) > 1 else float("nan")
            return sd, min(vals), max(vals)
        r1, r2, r3 = s("Avg_RSSI_dBm"), s("DIS_Count"), s("DIS_Total") if "DIS_Total" in cols else (float("nan"),) * 3
        P(f"  {c['cell_id']:<14} {len(g):>3}  {r1[0]:>9.5f} {r1[1]:>10.4f}..{r1[2]:<10.4f} {r2[0]:>7.3f} {r2[1]:>5.0f}..{r2[2]:<5.0f}  {r3[0]:>8.3f} {r3[1]:>6.0f}..{r3[2]:<6.0f}")
        for name, t in (("Avg_RSSI_dBm", r1), ("DIS_Count", r2), ("DIS_Total", r3)):
            if len(g) > 1 and t[0] == 0:
                zero.append(f"{c['cell_id']}:{name}")
    P(f"  variância nula (n>1): {len(zero)} -> {zero}")
    if zero:
        warns.append(f"{len(zero)} pares célula/feature com variância nula (ver secção 7)")

    P("\n## Resultado")
    P(f"  FALHAS: {len(fails)}")
    for x in fails:
        P(f"    - {x}")
    P(f"  AVISOS: {len(warns)}")
    for x in warns:
        P(f"    - {x}")
    P(f"  RESULTADO: {'FALHAS' if fails else ('AVISOS' if warns else 'OK')}")

    # tabela 9
    os.makedirs(a.tables_dir, exist_ok=True)
    with open(os.path.join(a.tables_dir, "table9_v2_checks.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    tex = []
    T = tex.append
    T(f"% Gerado por campaign_v2/make_tables_v2.py {GENERATOR_VERSION}. NÃO EDITAR À MÃO.")
    T(f"% Fonte: {os.path.basename(a.features)} sha256={sha256(a.features)} ({len(rows)} runs)")
    T("% Média $\\pm$ desvio-padrão amostral por célula; Energy = energia média por sensor (inclui warmup).")
    T("\\begin{table*}[!t]")
    ns = {len(groups[c["config"]]) for c in cells}
    ntxt = f"$n={ns.pop()}$ runs per cell" if len(ns) == 1 else "$n$ runs per cell, see column $n$"
    T("\\caption{Mean $\\pm$ standard deviation of the eight features of IWCS v2 in raw units, "
      f"per topology and condition ({ntxt}).}}")
    T("\\label{tab:metrics}")
    T("\\centering")
    T("\\scriptsize")
    T("\\renewcommand{\\arraystretch}{1.00}")
    T("\\setlength{\\tabcolsep}{2.0pt}")
    T("\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}llr" + "r" * len(TABLE_COLS) + "@{}}")
    T("\\toprule")
    T("\\textbf{Topology} & \\textbf{Condition} & \\textbf{$n$} & "
      + " & ".join(f"\\textbf{{{HEAD[f]}}}" for f in TABLE_COLS) + " \\\\")
    T("\\midrule")
    topos = []
    for c in cells:
        if c["topology"] not in topos:
            topos.append(c["topology"])
    for i, tp in enumerate(topos):
        tc = sorted([c for c in cells if c["topology"] == tp], key=lambda c: COND_ORDER.index(c["condition"]))
        label = f"Grid {tc[0]['n_nodes']}"
        for j, c in enumerate(tc):
            g = groups[c["config"]]
            first = f"\\multirow{{{len(tc)}}}{{*}}{{{label}}}" if j == 0 else ""
            if g:
                vals = " & ".join(mean_sd([num(r[f]) for r in g], FMT[f]) for f in TABLE_COLS)
            else:
                vals = " & ".join("--" for _ in TABLE_COLS)
            T(f"{first} & {c['condition']} & {len(g)} & {vals} \\\\")
        if i < len(topos) - 1:
            T("\\addlinespace[2pt]")
    T("\\bottomrule")
    T("\\end{tabular*}")
    T("\\end{table*}")
    with open(os.path.join(a.tables_dir, "table9_v2.tex"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(tex) + "\n")
    print(f"table9_v2.tex e table9_v2_checks.txt escritos em {a.tables_dir}; "
          f"{len(fails)} falhas, {len(warns)} avisos", file=sys.stderr)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
