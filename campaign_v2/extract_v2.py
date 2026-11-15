#!/usr/bin/env python3
"""
extract_v2.py: extrator versionado .sca -> CSV da campanha IWCS v2 (uma linha por run).

    python3 -I extract_v2.py [--results DIR] [--cells cells.csv] [--out features_v2.csv]
                             [--sim-time 3600] [--warmup 80] [--strict] [SCA ...]

Só usa a biblioteca padrão do Python 3. Lê os .sca no formato OMNeT++ 5.x (version 2).
Se não forem dados ficheiros .sca, processa <results>/*.sca. Por omissão, só aceita runs
com o marcador <config>-<run>.ok gerado por run_campaign.sh.

DATASET_VERSION = "2.0.0"

------------------------------------------------------------------------------------
DEFINIÇÕES
------------------------------------------------------------------------------------
H        = conjunto dos nós sensores host[i] da rede (inclui os nós atacantes; exclui o sink).
           TODAS as features e colunas auxiliares são calculadas só sobre H.
sink     = sink[0] (raiz da DODAG, recebe o tráfego legítimo na app[0], porta 1000).
           Só é usado como recetor no PDR, no atraso e no throughput.
Janelas temporais:
  [W]    = janela de registo pós-warmup [80 s, 3600 s], com T_meas = 3600 - 80 = 3520 s.
           Aplica-se às estatísticas @statistic (:count, :sum, :mean, histogram).
  [T]    = simulação completa [0 s, 3600 s], incluindo o warmup e a formação da DODAG.
           Aplica-se aos scalars gravados em finish() com recordScalar() e ao estado
           final da bateria (:last).

====================================================================================
A) AS 8 FEATURES PRINCIPAIS
====================================================================================
Coluna             Janela  Fonte no .sca -> fórmula
------------------------------------------------------------------------------------
Avg_RSSI_dBm       [W]   scalar host[i].rpl  rssi:mean   (RSSI em dBm de cada DIO recebido,
                         a partir do SignalPowerInd da camada física)
                         = média aritmética simples de rssi:mean(h), sobre os h em H com valor
                         finito. Não é ponderada pelo número de DIO, porque o .sca não grava a
                         contagem do rssi.
                         NOTA: com o canal efetivo (BreakpointPathLoss, sem shadowing; as linhas
                         radioMedium.attenuation.* dos .ini são inertes) e a grelha regular de
                         40 m, o RSSI é praticamente constante (cerca de -81.56 dBm). É reportado
                         tal como sai do simulador, mas a sua variância é quase nula.

DIO_Count          [W]   scalar host[i].rpl  dioReceived:count
                         = soma sobre h em H.

DIS_Count          [W]   scalar host[i].rpl  disReceived:count
                         = soma sobre h em H. Para o valor da simulação completa, ver DIS_Total.

Rank_Changes       [W]   scalar host[i].rpl  rankUpdated:count
                         = soma sobre h em H. Inclui o salto de rank do próprio atacante no
                         início do ataque.

PDR_percent        [W]   scalar sink[0].app[0]  packetReceived:count ;
                         scalar host[i].app[0]  packetSent:count
                         = 100 * rx_sink / soma_h tx_h.
                         Conta só o tráfego legítimo (app[0] -> porta 1000). O tráfego de ataque
                         do Flooding/Backoff usa a app[1] -> sink.app[1] (porta 1001) e fica
                         excluído.
                         Sem corte: tx e rx contam só a partir de 80 s, por isso um pacote
                         enviado antes dos 80 s e recebido depois conta em rx mas não em tx, e a
                         PDR pode passar ligeiramente de 100 %. Na v2 acontece uma vez:
                         Grid48_Normal run 14, rx = 3033, tx = 3032 (100.033 %), com o pacote
                         enviado em t = 79.992 s e recebido em t = 80.013 s. make_tables_v2.py
                         assinala este caso como aviso.

Avg_Delay_ms       [W]   statistic sink[0].app[0]  endToEndDelay:histogram, campo mean   (em s)
                         = 1000 * mean (atraso médio extremo-a-extremo dos pacotes legítimos
                         recebidos).

Throughput_kbps    [W]   scalar sink[0].app[0]  packetReceived:sum(packetBytes)
                         (bytes de aplicação, 56 B/pkt)
                         = bytes * 8 / T_meas / 1000.
                         O @statistic throughput do UdpSink só existe como vetor e não é usado.

Energy_Consumed_J  [T]   scalar host[i].energyStorage  residualEnergyCapacity:last ;
                         param  **.host[*].energyStorage.initialCapacity
                         (1500 J, lido do cabeçalho do .sca)
                         = (1/|H|) * soma sobre h em H de (initialCapacity - residualEnergyCapacity:last(h))
                         = energia MÉDIA consumida por sensor.
                         EXCEÇÃO AO WARMUP: :last é o estado da bateria no fim da simulação, por
                         isso inclui o consumo desde t = 0, incluindo o warmup.

====================================================================================
B) COLUNAS AUXILIARES (não são features do modelo; servem para análise e verificação)
====================================================================================
Energy_Total_J         [T]  = soma sobre h em H de (initialCapacity - residualEnergyCapacity:last(h))
                            = |H| * Energy_Consumed_J. Inclui o warmup.
DIS_Total              [T]  scalar host[i].rpl  disReceivedCount (recordScalar em finish())
                            = soma sobre h em H.
DAO_Sent_Total         [T]  scalar host[i].rpl  daoSentCount         = soma sobre h em H.
DAO_Received_Total     [T]  scalar host[i].rpl  daoReceivedCount     = soma sobre h em H.
DAO_AckReceived_Total  [T]  scalar host[i].rpl  daoAckReceivedCount  = soma sobre h em H.
DAO_Forwarded_Total    [T]  scalar host[i].rpl  daoForwardedCount    = soma sobre h em H.
DAO_Dropped_Total      [T]  scalar host[i].rpl  daoDroppedCount      = soma sobre h em H.
    Os cinco contadores DAO foram acrescentados no commit 0515e40 (MAIO_RPL27). Como H
    exclui o sink, os DAO recebidos pela raiz NÃO entram em DAO_Received_Total.

====================================================================================
C) COLUNAS DE IDENTIFICAÇÃO E RASTREIO
====================================================================================
topology, condition, cell_id   de cells.csv (chave: config)
run, seed                      atributos runnumber e seedset do .sca (seed-set = runnumber)
config                         atributo configname do .sca
dataset_version                constante DATASET_VERSION
sca_sha256                     sha256 do .sca de origem (liga cada linha ao ficheiro bruto)
------------------------------------------------------------------------------------
"""
import argparse, csv, glob, hashlib, math, os, re, shlex, sys

DATASET_VERSION = "2.0.0"
HOST_RE = re.compile(r"^[^.]+\.host\[(\d+)\]\.(.+)$")
SINK0 = re.compile(r"^[^.]+\.sink\[0\]\.(.+)$")

ID_COLUMNS = ["topology", "condition", "run", "seed", "config", "dataset_version"]
FEATURES = ["Avg_RSSI_dBm", "DIO_Count", "DIS_Count", "Rank_Changes", "PDR_percent",
            "Avg_Delay_ms", "Throughput_kbps", "Energy_Consumed_J"]
AUX_COLUMNS = ["Energy_Total_J", "DIS_Total", "DAO_Sent_Total", "DAO_Received_Total",
               "DAO_AckReceived_Total", "DAO_Forwarded_Total", "DAO_Dropped_Total"]
TRACE_COLUMNS = ["cell_id", "sca_sha256"]
COLUMNS = ID_COLUMNS + FEATURES + AUX_COLUMNS + TRACE_COLUMNS


def fnum(s):
    s = s.strip()
    try:
        return float(s)
    except ValueError:
        return float("nan")


def parse_sca(path):
    """Devolve (attrs, params, scalars{(module,name):v}, stats{(module,name):{field:v}})."""
    attrs, params, scalars, stats = {}, {}, {}, {}
    cur = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line or line[0] in "\n#":
                continue
            if line.startswith("scalar "):
                t = shlex.split(line)
                if len(t) >= 4:
                    scalars[(t[1], t[2])] = fnum(t[3])
                cur = None
            elif line.startswith("statistic "):
                t = shlex.split(line)
                cur = (t[1], t[2]); stats[cur] = {}
            elif line.startswith("field ") and cur is not None:
                t = line.split()
                stats[cur][t[1]] = fnum(t[2])
            elif line.startswith("attr ") and cur is None:
                t = line.split(None, 2)
                attrs[t[1]] = t[2].strip() if len(t) > 2 else ""
            elif line.startswith("param "):
                t = line.split(None, 2)
                params[t[1]] = t[2].strip() if len(t) > 2 else ""
            elif line.startswith(("run ", "version ", "bin")):
                if not line.startswith("bin"):
                    cur = None
    return attrs, params, scalars, stats


def value_with_unit(s, unit):
    s = s.strip().strip('"')
    m = re.fullmatch(r"([-+0-9.eE]+)\s*" + re.escape(unit) + r"?", s)
    if not m:
        raise ValueError(f"valor '{s}' não é um número em {unit}")
    return float(m.group(1))


def features(path, sim_time, warmup):
    attrs, params, sc, st = parse_sca(path)
    T_meas = sim_time - warmup

    hosts = {}
    for (mod, name), v in sc.items():
        m = HOST_RE.match(mod)
        if m:
            hosts.setdefault(int(m.group(1)), {})[(m.group(2), name)] = v
    if not hosts:
        raise ValueError("nenhum host[i] no .sca")

    def hsum(sub, name):
        vals = [d[(sub, name)] for d in hosts.values() if (sub, name) in d]
        if len(vals) != len(hosts):
            raise ValueError(f"{sub} {name}: presente em {len(vals)}/{len(hosts)} hosts")
        return sum(vals)

    def sink(sub, name, store=sc):
        for (mod, n), v in store.items():
            m = SINK0.match(mod)
            if m and m.group(1) == sub and n == name:
                return v
        raise ValueError(f"sink[0].{sub} {name} em falta")

    # run completo? (scalars de finish() do RPL)
    if not any(n == "daoSentCount" for (_, n) in sc):
        raise ValueError("sem scalars de finish() (run incompleta?)")

    rssi = [d[("rpl", "rssi:mean")] for d in hosts.values()
            if ("rpl", "rssi:mean") in d and math.isfinite(d[("rpl", "rssi:mean")])]
    tx = hsum("app[0]", "packetSent:count")
    rx = sink("app[0]", "packetReceived:count")
    rx_bytes = sink("app[0]", "packetReceived:sum(packetBytes)")
    delay = sink("app[0]", "endToEndDelay:histogram", st).get("mean", float("nan"))

    cap_key = [k for k in params if k.endswith("host[*].energyStorage.initialCapacity")]
    if len(cap_key) != 1:
        raise ValueError(f"initialCapacity dos hosts não encontrado no cabeçalho ({cap_key})")
    cap = value_with_unit(params[cap_key[0]], "J")
    if sum(("energyStorage", "residualEnergyCapacity:last") in d for d in hosts.values()) != len(hosts):
        raise ValueError("residualEnergyCapacity:last em falta nalgum host")
    energy_total = sum(cap - d[("energyStorage", "residualEnergyCapacity:last")] for d in hosts.values())

    return attrs, {
        "Avg_RSSI_dBm": sum(rssi) / len(rssi) if rssi else float("nan"),
        "DIO_Count": int(hsum("rpl", "dioReceived:count")),
        "DIS_Count": int(hsum("rpl", "disReceived:count")),
        "Rank_Changes": int(hsum("rpl", "rankUpdated:count")),
        "PDR_percent": 100.0 * rx / tx if tx > 0 else float("nan"),
        "Avg_Delay_ms": 1000.0 * delay,
        "Throughput_kbps": rx_bytes * 8.0 / T_meas / 1000.0,
        "Energy_Consumed_J": energy_total / len(hosts),
        # auxiliares [T]
        "Energy_Total_J": energy_total,
        "DIS_Total": int(hsum("rpl", "disReceivedCount")),
        "DAO_Sent_Total": int(hsum("rpl", "daoSentCount")),
        "DAO_Received_Total": int(hsum("rpl", "daoReceivedCount")),
        "DAO_AckReceived_Total": int(hsum("rpl", "daoAckReceivedCount")),
        "DAO_Forwarded_Total": int(hsum("rpl", "daoForwardedCount")),
        "DAO_Dropped_Total": int(hsum("rpl", "daoDroppedCount")),
    }


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("sca", nargs="*", help="ficheiros .sca (por omissão: <results>/*.sca)")
    ap.add_argument("--results", default=os.path.join(here, "results"))
    ap.add_argument("--cells", default=os.path.join(here, "cells.csv"))
    ap.add_argument("--out", default=os.path.join(here, "features_v2.csv"))
    ap.add_argument("--sim-time", type=float, default=3600.0)
    ap.add_argument("--warmup", type=float, default=80.0)
    ap.add_argument("--no-require-ok", action="store_true", help="aceitar .sca sem marcador .ok")
    ap.add_argument("--strict", action="store_true", help="falhar ao primeiro .sca inválido")
    a = ap.parse_args()

    with open(a.cells, newline="", encoding="utf-8") as fh:
        cells = {r["config"]: r for r in csv.DictReader(fh)}

    files = sorted(a.sca) if a.sca else sorted(glob.glob(os.path.join(a.results, "*.sca")))
    rows, errors = [], 0
    for f in files:
        try:
            if not a.no_require_ok:
                ok = f[:-4] + ".ok"
                if not os.path.exists(ok):
                    raise ValueError("sem marcador .ok")
                okd = dict(l.strip().split("=", 1) for l in open(ok) if "=" in l)
                if okd.get("sim_time") != f"{a.sim_time:g}s":
                    raise ValueError(f"sim_time do .ok = {okd.get('sim_time')} != {a.sim_time:g}s")
            attrs, feat = features(f, a.sim_time, a.warmup)
            cfg = attrs["configname"]
            if cfg not in cells:
                raise ValueError(f"config '{cfg}' não está em cells.csv")
            c = cells[cfg]
            row = {"topology": c["topology"], "condition": c["condition"],
                   "run": int(attrs["runnumber"]), "seed": int(attrs["seedset"]),
                   "config": cfg, "dataset_version": DATASET_VERSION, "cell_id": c["cell_id"],
                   "sca_sha256": hashlib.sha256(open(f, "rb").read()).hexdigest()}
            row.update(feat)
            rows.append(row)
        except Exception as e:
            errors += 1
            print(f"ERRO {f}: {e}", file=sys.stderr)
            if a.strict:
                sys.exit(1)

    order = {"Normal": 0, "Blackhole": 1, "Flooding": 2, "Backoff": 3, "Wormhole": 4}
    rows.sort(key=lambda r: (int(r["topology"].replace("Grid", "")), order.get(r["condition"], 9), r["run"]))
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    print(f"{len(rows)} linhas escritas em {a.out}; {errors} ficheiros com erro", file=sys.stderr)
    sys.exit(1 if errors and a.strict else 0)


if __name__ == "__main__":
    main()
