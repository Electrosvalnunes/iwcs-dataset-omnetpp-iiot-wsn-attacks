#!/usr/bin/env python3
"""
benchmark_v2.py: baselines de diagnóstico sobre features_v2.csv -> tables/table10_v2.tex

    python3 -I benchmark_v2.py [--features features_v2.csv] [--tables-dir ../manuscript_v2/tables]
                               [--train-max-run 23] [--seed 42] [--n-jobs 2]

Requer: numpy e scikit-learn, nas versões de requirements-benchmark.txt (venv em .venv/). As versões usadas são
gravadas no cabeçalho do .tex e em benchmark_v2_results.csv.

ALVO
    condition (5 classes: Normal, Blackhole, Flooding, Backoff, Wormhole). topology, run, seed,
    config, cell_id e todas as colunas auxiliares (Energy_Total_J, DIS_Total, DAO_*) NUNCA entram
    como preditores. A topologia só é usada para as partições LOTO.

MODELOS (iguais aos do manuscrito R2)
    DT  DecisionTreeClassifier(max_depth=5, random_state=42)
    RF  RandomForestClassifier(n_estimators=200, random_state=42)
    LR  Pipeline(StandardScaler, LogisticRegression(max_iter=5000))   (LR padronizada)

PROTOCOLOS
    random80/20  train_test_split(test_size=0.2, stratify=alvo, random_state=42)
    run-split    treino: run <= 23 (runs 0-23); teste: run >= 24 (runs 24-29)
                 (--train-max-run muda o limite; útil para testar com campanhas incompletas)
    LOTO         Leave-One-Topology-Out: treino em 3 topologias, teste na 4.ª; reporta-se a
                 média das 4 dobras (cada dobra fica em benchmark_v2_results.csv)
    Métricas: accuracy e macro-F1. Um protocolo sem dados de treino/teste, ou com uma só classe
    no treino, é reportado como n/a (com o motivo no CSV).

CONJUNTOS DE FEATURES (as linhas do placeholder manuscript_v2/tables/table10_v2.tex, mais uma)
    F6 (principal)  DIO_Count, Rank_Changes, PDR_percent, Avg_Delay_ms, Throughput_kbps,
                    Energy_Consumed_J: as 6 features informativas. RSSI e DIS ficam de fora porque
                    são constantes na v2 (canal determinístico; DIS só na formação da rede).
                    DT, RF e LR em random 80/20 e run split; RF e LR em LOTO.
    Ablações (RF e LR; random 80/20 e LOTO):
      sem PDR                 F6 sem PDR_percent
      sem Delay               F6 sem Avg_Delay_ms
      contadores de routing   só DIO_Count e Rank_Changes
    Linha extra: só PDR_percent, DT com max_depth=3, random 80/20. Serve para comparar com o
    valor da v1.1 (0.9179, mesma configuração na R2).
"""
import argparse, csv, hashlib, os, sys

GENERATOR_VERSION = "1.1.0"
F6 = ["DIO_Count", "Rank_Changes", "PDR_percent", "Avg_Delay_ms", "Throughput_kbps", "Energy_Consumed_J"]
NO_PDR = [f for f in F6 if f != "PDR_percent"]
NO_DELAY = [f for f in F6 if f != "Avg_Delay_ms"]
ROUTING = ["DIO_Count", "Rank_Changes"]

# (rótulo, features, alvo, [(protocolo, [modelos])]); a ordem é a da Tabela 10
EXPERIMENTS = [
    ("6 informative features", F6, "condition",
     [("random", ["DT", "RF", "LR"]), ("run", ["DT", "RF", "LR"]), ("loto", ["RF", "LR"])]),
    ("Ablation: without PDR", NO_PDR, "condition", [("random", ["RF", "LR"]), ("loto", ["RF", "LR"])]),
    ("Ablation: without Delay", NO_DELAY, "condition", [("random", ["RF", "LR"]), ("loto", ["RF", "LR"])]),
    ("Ablation: routing counters only", ROUTING, "condition", [("random", ["RF", "LR"]), ("loto", ["RF", "LR"])]),
    ("PDR only (v1.1: 0.9179)", ["PDR_percent"], "condition", [("random", ["DT3"])]),
]
PROTO_LABEL = {"random": "random 80/20", "run": "run-index split", "loto": "LOTO mean"}


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--features", default=os.path.join(here, "features_v2.csv"))
    ap.add_argument("--tables-dir", default=os.path.join(os.path.dirname(here), "manuscript_v2", "tables"))
    ap.add_argument("--train-max-run", type=int, default=23)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n-jobs", type=int, default=2)
    a = ap.parse_args()

    import numpy as np
    import sklearn
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    def model(name):
        if name == "DT":
            return DecisionTreeClassifier(max_depth=5, random_state=a.seed)
        if name == "DT3":
            return DecisionTreeClassifier(max_depth=3, random_state=a.seed)
        if name == "RF":
            return RandomForestClassifier(n_estimators=200, random_state=a.seed, n_jobs=a.n_jobs)
        if name == "LR":
            return make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000))
        raise ValueError(name)

    with open(a.features, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit("features_v2.csv vazio")
    runs = np.array([int(r["run"]) for r in rows])
    topo = np.array([r["topology"] for r in rows])

    def fit_eval(mname, X, y, tr, te):
        if tr.sum() == 0 or te.sum() == 0:
            return None, "treino ou teste vazio"
        if len(set(y[tr])) < 2:
            return None, "uma só classe no treino"
        m = model(mname).fit(X[tr], y[tr])
        p = m.predict(X[te])
        return (accuracy_score(y[te], p), f1_score(y[te], p, average="macro"), int(tr.sum()), int(te.sum())), ""

    results = []   # dicts
    for label, feats, target, plan in EXPERIMENTS:
        X = np.array([[float(r[f]) for f in feats] for r in rows])
        y = np.array([r[target] for r in rows])
        for proto, models in plan:
            for mname in models:
                base = {"feature_set": label, "features": ";".join(feats), "target": target,
                        "protocol": proto, "model": mname}
                if proto == "random":
                    idx = np.arange(len(rows))
                    try:
                        itr, ite = train_test_split(idx, test_size=0.2, stratify=y, random_state=a.seed)
                    except ValueError as e:
                        results.append({**base, "fold": "", "status": f"n/a: {e}"}); continue
                    tr = np.isin(idx, itr); te = np.isin(idx, ite)
                    folds = [("", tr, te)]
                elif proto == "run":
                    folds = [(f"train<= {a.train_max_run}", runs <= a.train_max_run, runs > a.train_max_run)]
                else:
                    folds = [(t, topo != t, topo == t) for t in sorted(set(topo), key=lambda s: int(s.replace("Grid", "")))]
                accs = []
                for fname, tr, te in folds:
                    r, why = fit_eval(mname, X, y, tr, te)
                    if r is None:
                        results.append({**base, "fold": fname, "status": f"n/a: {why}"})
                        continue
                    results.append({**base, "fold": fname, "status": "ok", "accuracy": r[0], "macro_f1": r[1],
                                    "n_train": r[2], "n_test": r[3]})
                    accs.append(r)
                if proto == "loto":
                    if accs and len(accs) == len(folds):
                        results.append({**base, "fold": "mean", "status": "ok",
                                        "accuracy": float(np.mean([x[0] for x in accs])),
                                        "macro_f1": float(np.mean([x[1] for x in accs])),
                                        "n_train": "", "n_test": sum(x[3] for x in accs)})
                    else:
                        results.append({**base, "fold": "mean", "status": f"n/a: {len(accs)}/{len(folds)} dobras válidas"})

    os.makedirs(a.tables_dir, exist_ok=True)
    fsha = sha256(a.features)
    vers = f"python {sys.version.split()[0]}, numpy {np.__version__}, scikit-learn {sklearn.__version__}"
    rc = os.path.join(a.tables_dir, "benchmark_v2_results.csv")
    cols = ["feature_set", "features", "target", "protocol", "model", "fold", "status",
            "accuracy", "macro_f1", "n_train", "n_test"]
    with open(rc, "w", newline="", encoding="utf-8") as fh:
        fh.write(f"# benchmark_v2.py {GENERATOR_VERSION}; features sha256={fsha}; {vers}; seed={a.seed}; train_max_run={a.train_max_run}\n")
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in results:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})

    # tabela 10: uma linha por (conjunto, protocolo, modelo); LOTO = média
    tex = []
    T = tex.append
    T(f"% Gerado por campaign_v2/benchmark_v2.py {GENERATOR_VERSION}. NÃO EDITAR À MÃO.")
    T(f"% Fonte: {os.path.basename(a.features)} sha256={fsha} ({len(rows)} runs); {vers}")
    T(f"% random_state={a.seed}; run split: treino run<={a.train_max_run}, teste run>{a.train_max_run}; dobras LOTO em benchmark_v2_results.csv")
    T("\\begin{table}[!ht]")
    T("\\caption{Diagnostic baselines on IWCS v2 (accuracy / macro-F1).}")
    T("\\label{tab:benchmarks}")
    T("\\centering")
    T("\\scriptsize")
    T("\\setlength{\\tabcolsep}{2.0pt}")
    T("\\renewcommand{\\arraystretch}{0.98}")
    T("\\begin{tabularx}{\\columnwidth}{@{}>{\\RaggedRight\\arraybackslash}X l r r@{}}")
    T("\\toprule")
    T("\\textbf{Feature set / protocol} & \\textbf{Model} & \\textbf{Acc.} & \\textbf{F1} \\\\")
    T("\\midrule")
    first = True
    for label, feats, target, plan in EXPERIMENTS:
        if not first and (label.startswith("Ablation: without PDR") or label.startswith("PDR only")):
            T("\\midrule")
        first = False
        for proto, models in plan:
            for mname in models:
                sel = [r for r in results if r["feature_set"] == label and r["protocol"] == proto
                       and r["model"] == mname and (proto != "loto" or r["fold"] == "mean")]
                r = sel[-1] if sel else {"status": "n/a"}
                mlabel = "DT (depth 3)" if mname == "DT3" else mname
                if r["status"] == "ok":
                    T(f"{label}, {PROTO_LABEL[proto]} & {mlabel} & {r['accuracy']:.4f} & {r['macro_f1']:.4f} \\\\")
                else:
                    T(f"{label}, {PROTO_LABEL[proto]} & {mlabel} & n/a & n/a \\\\")
    T("\\bottomrule")
    T("\\end{tabularx}")
    T("\\end{table}")
    with open(os.path.join(a.tables_dir, "table10_v2.tex"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(tex) + "\n")
    na = sum(1 for r in results if r["status"] != "ok")
    print(f"table10_v2.tex e benchmark_v2_results.csv escritos em {a.tables_dir}; "
          f"{len(results)} linhas de resultados, {na} n/a", file=sys.stderr)


if __name__ == "__main__":
    main()
