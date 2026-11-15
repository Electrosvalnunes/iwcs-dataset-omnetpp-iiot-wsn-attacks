#!/usr/bin/env bash
# =============================================================================
# Campanha IWCS v2: corre as runs [FIRST..LAST] das 20 células de cells.csv.
#
#   uso:  ./run_campaign.sh FIRST_RUN LAST_RUN
#   env:  JOBS (10)  SIM_TIME (3600s)  RESULTS (./results)  LOGS (./logs)
#         ONLY_CELL (cell_id, opcional: corre só essa célula)
#         OMNETPP_ROOT (~/Downloads/omnetpp-5.7.1)
#
# - Não modifica os .ini: tudo o que difere da execução "normal" é passado por
#   opções de linha de comando (ver CMD abaixo / manifest.txt).
# - Grava apenas scalars (--**.vector-recording=false), um ficheiro
#   <config>-<run>.sca por run em $RESULTS (padrão do .ini: ${resultdir}/${configname}-${runnumber}.sca).
# - Ordem: células mais pesadas primeiro (est_events_M decrescente), depois run.
# - Retoma: uma run é saltada se existir <config>-<run>.ok com o mesmo SIM_TIME
#   e o .sca correspondente. Uma run só recebe .ok se: exit 0, a simulação
#   chegou ao sim-time-limit, o .sca existe e contém os scalars de finish().
# - Log por run em $LOGS/<config>-<run>.log; resumo em $LOGS/progress.tsv:
#   data  cell_id  config  run  status  exit  wall_s  events
# =============================================================================
set -uo pipefail
export LC_ALL=C   # números com ponto decimal no progress.tsv/.ok

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJ=$(dirname "$HERE")
FIRST=${1:?uso: run_campaign.sh FIRST_RUN LAST_RUN}
LAST=${2:?uso: run_campaign.sh FIRST_RUN LAST_RUN}

export OMNETPP_ROOT=${OMNETPP_ROOT:-$HOME/Downloads/omnetpp-5.7.1}
export JOBS=${JOBS:-10}
export SIM_TIME=${SIM_TIME:-3600s}
export RESULTS=${RESULTS:-$HERE/results}
export LOGS=${LOGS:-$HERE/logs}
export PROJ
export SIMDIR=$PROJ/simulations
export INET_SRC=$(cd "$PROJ/../inet/src" && pwd)
export PATH=$OMNETPP_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$OMNETPP_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
ONLY_CELL=${ONLY_CELL:-}

mkdir -p "$RESULTS" "$LOGS"
[ -f "$LOGS/progress.tsv" ] || printf "date\tcell_id\tconfig\trun\tstatus\texit\twall_s\tevents\n" > "$LOGS/progress.tsv"

run_one() {   # CELL_ID INI CONFIG RUN
  local CELL=$1 INI=$2 CFG=$3 RUN=$4
  local SCA="$RESULTS/$CFG-$RUN.sca" OK="$RESULTS/$CFG-$RUN.ok" LOG="$LOGS/$CFG-$RUN.log"
  if [ -f "$OK" ] && [ -f "$SCA" ] && grep -qx "sim_time=$SIM_TIME" "$OK"; then
    return 0                                     # já completa: retoma
  fi
  rm -f "$SCA" "$OK" "$RESULTS/$CFG-$RUN.vec" "$RESULTS/$CFG-$RUN.vci"
  local T0=$(date +%s.%N)
  ( cd "$SIMDIR" && exec opp_run -u Cmdenv \
      -l "$PROJ/src/MAIO_RPL27" -n "$SIMDIR:$PROJ/src:$INET_SRC" \
      -f "$INI" -c "$CFG" -r "$RUN" \
      --sim-time-limit="$SIM_TIME" \
      --result-dir="$RESULTS" \
      '--**.vector-recording=false' \
      --cmdenv-express-mode=true --cmdenv-status-frequency=600s ) > "$LOG" 2>&1
  local RC=$?
  local WALL=$(echo "$(date +%s.%N) - $T0" | bc)
  local EV=$(grep -oP 'event #\K[0-9]+' "$LOG" | tail -1)
  local STATUS=FAIL
  if [ $RC -eq 0 ] && grep -q "Simulation time limit reached -- at t=${SIM_TIME%s}s" "$LOG" \
     && [ -f "$SCA" ] && grep -q " daoSentCount " "$SCA"; then
    STATUS=OK
    printf "cell=%s\nconfig=%s\nrun=%s\nsim_time=%s\nexit=%s\nwall_s=%s\nevents=%s\nsca_sha256=%s\nfinished=%s\n" \
      "$CELL" "$CFG" "$RUN" "$SIM_TIME" "$RC" "$WALL" "$EV" "$(sha256sum "$SCA" | cut -c1-64)" "$(date -Is)" > "$OK"
  fi
  [ -f "$RESULTS/$CFG-$RUN.vec" ] && STATUS="${STATUS}_VEC!"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%.1f\t%s\n" "$(date -Is)" "$CELL" "$CFG" "$RUN" "$STATUS" "$RC" "$WALL" "${EV:-}" >> "$LOGS/progress.tsv"
}
export -f run_one

# lista de jobs: células por custo decrescente, depois run crescente
tail -n +2 "$HERE/cells.csv" | awk -F, -v only="$ONLY_CELL" '(only=="" || $1==only){print $10","$1","$2","$3}' \
 | sort -t, -k1,1gr \
 | while IFS=, read -r EST CELL INI CFG; do
     for ((r=FIRST; r<=LAST; r++)); do echo "$CELL $INI $CFG $r"; done
   done > "$LOGS/jobs_${FIRST}-${LAST}.txt"

echo "[$(date -Is)] início runs $FIRST-$LAST: $(wc -l < "$LOGS/jobs_${FIRST}-${LAST}.txt") jobs, JOBS=$JOBS, SIM_TIME=$SIM_TIME, RESULTS=$RESULTS"
xargs -P "$JOBS" -L 1 bash -c 'run_one "$0" "$1" "$2" "$3"' < "$LOGS/jobs_${FIRST}-${LAST}.txt"
echo "[$(date -Is)] fim runs $FIRST-$LAST: OK=$(ls "$RESULTS"/*.ok 2>/dev/null | wc -l) (total acumulado)"
