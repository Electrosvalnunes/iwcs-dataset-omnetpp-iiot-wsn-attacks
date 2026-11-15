#!/usr/bin/env bash
# =============================================================================
# Campanha IWCS v2, adendo A1: repete as runs de Flooding que falharam porque a
# bateria de 55 J do sink[0] se esgotou (ModuleCrashOperation sem suporte no
# Icmpv6 do INET 4.2.10). Ver manifest_addendum_A1.txt.
#
#   uso:  ./rerun_sink_capacity.sh [--dry-run]
#   env:  JOBS (7)  SINK_CAPACITY (1500J)
#
# - Não altera os .ini nem o run_campaign.sh. A única diferença em relação à
#   linha de comando da campanha são duas opções:
#     --**.sink[*].energyStorage.nominalCapacity=$SINK_CAPACITY
#     --**.sink[*].energyStorage.initialCapacity=$SINK_CAPACITY
# - Só corre depois de a campanha terminar (o driver não pode estar ativo).
# - Seleção: as runs das células de Flooding (cells.csv) com estado FAIL em
#   logs/progress.tsv, sem .ok, e cujo log contém o erro ModuleCrashOperation
#   no sink[0]. Qualquer outra falha é listada e NÃO é repetida.
# - Cada run repetida recebe um .ok com mais duas linhas
#   (sink_capacity_override e addendum=A1), e uma linha OK_A1/FAIL_A1 em
#   logs/progress.tsv. O log original da run falhada é preservado como
#   <config>-<run>.log.A0.
# =============================================================================
set -uo pipefail
export LC_ALL=C
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJ=$(dirname "$HERE")
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
export OMNETPP_ROOT=${OMNETPP_ROOT:-$HOME/Downloads/omnetpp-5.7.1}
export JOBS=${JOBS:-7}
export SINK_CAPACITY=${SINK_CAPACITY:-1500J}
export SIM_TIME=3600s
export RESULTS=$HERE/results LOGS=$HERE/logs PROJ SIMDIR=$PROJ/simulations
export INET_SRC=$(cd "$PROJ/../inet/src" && pwd)
export PATH=$OMNETPP_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$OMNETPP_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

if [ -f "$HERE/driver.pid" ] && kill -0 "$(cat "$HERE/driver.pid")" 2>/dev/null; then
  echo "ERRO: a campanha ainda está a correr (driver $(cat "$HERE/driver.pid")). Repetir só no fim." >&2; exit 1
fi

# runs candidatas: FAIL em células de Flooding, sem .ok
if [ $DRY = 1 ]; then LIST=$(mktemp); else LIST=$LOGS/rerun_A1_jobs.txt; fi; : > "$LIST"
awk -F, 'NR>1 && $6=="Flooding"{print $1","$2","$3}' "$HERE/cells.csv" | while IFS=, read -r CELL INI CFG; do
  awk -F'\t' -v c="$CFG" 'NR>1 && $3==c && $5 ~ /^FAIL/ {print $4}' "$LOGS/progress.tsv" | sort -un | while read -r RUN; do
    [ -f "$RESULTS/$CFG-$RUN.ok" ] && continue
    if grep -q "ModuleCrashOperation.*sink\[0\]" "$LOGS/$CFG-$RUN.log" 2>/dev/null; then
      echo "$CELL $INI $CFG $RUN" >> "$LIST"
    else
      echo "AVISO: $CFG-$RUN falhou por outra razão; não é repetida" >&2
    fi
  done
done
echo "Runs a repetir (adendo A1, sink=$SINK_CAPACITY): $(wc -l < "$LIST")"; cat "$LIST"
[ $DRY = 1 ] && exit 0

run_a1() {   # CELL INI CFG RUN
  local CELL=$1 INI=$2 CFG=$3 RUN=$4
  local SCA="$RESULTS/$CFG-$RUN.sca" OK="$RESULTS/$CFG-$RUN.ok" LOG="$LOGS/$CFG-$RUN.log"
  [ -f "$LOG" ] && [ ! -f "$LOG.A0" ] && mv "$LOG" "$LOG.A0"
  rm -f "$SCA" "$OK"
  local T0=$(date +%s.%N)
  ( cd "$SIMDIR" && exec opp_run -u Cmdenv \
      -l "$PROJ/src/MAIO_RPL27" -n "$SIMDIR:$PROJ/src:$INET_SRC" \
      -f "$INI" -c "$CFG" -r "$RUN" \
      --sim-time-limit="$SIM_TIME" \
      --result-dir="$RESULTS" \
      '--**.vector-recording=false' \
      --cmdenv-express-mode=true --cmdenv-status-frequency=600s \
      "--**.sink[*].energyStorage.nominalCapacity=$SINK_CAPACITY" \
      "--**.sink[*].energyStorage.initialCapacity=$SINK_CAPACITY" ) > "$LOG" 2>&1
  local RC=$?
  local WALL=$(echo "$(date +%s.%N) - $T0" | bc)
  local EV=$(grep -oP 'event #\K[0-9]+' "$LOG" | tail -1)
  local STATUS=FAIL_A1
  if [ $RC -eq 0 ] && grep -q "Simulation time limit reached -- at t=${SIM_TIME%s}s" "$LOG" \
     && [ -f "$SCA" ] && grep -q " daoSentCount " "$SCA"; then
    STATUS=OK_A1
    printf "cell=%s\nconfig=%s\nrun=%s\nsim_time=%s\nexit=%s\nwall_s=%s\nevents=%s\nsca_sha256=%s\nfinished=%s\nsink_capacity_override=%s\naddendum=A1\n" \
      "$CELL" "$CFG" "$RUN" "$SIM_TIME" "$RC" "$WALL" "$EV" "$(sha256sum "$SCA" | cut -c1-64)" "$(date -Is)" "$SINK_CAPACITY" > "$OK"
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%.1f\t%s\n" "$(date -Is)" "$CELL" "$CFG" "$RUN" "$STATUS" "$RC" "$WALL" "${EV:-}" >> "$LOGS/progress.tsv"
}
export -f run_a1
echo "[$(date -Is)] início adendo A1" | tee -a "$LOGS/launches.txt"
xargs -P "$JOBS" -L 1 bash -c 'run_a1 "$0" "$1" "$2" "$3"' < "$LIST"
echo "[$(date -Is)] fim adendo A1: $(grep -c OK_A1 "$LOGS/progress.tsv") OK_A1, $(grep -c FAIL_A1 "$LOGS/progress.tsv") FAIL_A1" | tee -a "$LOGS/launches.txt"
