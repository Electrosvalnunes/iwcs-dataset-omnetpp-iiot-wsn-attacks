#!/usr/bin/env bash
# Estado da campanha IWCS v2: runs completas por lote, falhas, em curso e ETA grosseira.
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
R=$HERE/results; L=$HERE/logs
ok() { local a=$1 b=$2 n=0; for f in "$R"/*.ok; do [ -e "$f" ] || continue; r=${f##*-}; r=${r%.ok}; [ "$r" -ge "$a" ] && [ "$r" -le "$b" ] && n=$((n+1)); done; echo $n; }
echo "Lote 1 (runs 0-9):   $(ok 0 9) / 200 completas"
echo "Lote 2 (runs 10-29): $(ok 10 29) / 400 completas"
# falhas por resolver: runs com tentativa falhada e sem .ok (OK_A1 do adendo A1 conta como concluída)
echo "Falhas por resolver: $(awk -F'\t' 'NR>1 && $5 !~ /^OK/ {print $3"-"$4}' "$L/progress.tsv" 2>/dev/null | sort -u | while read -r k; do [ -f "$R/$k.ok" ] || echo "$k"; done | wc -l)"
echo "Repetidas (A1):      $(awk -F'\t' 'NR>1 && $5=="OK_A1"' "$L/progress.tsv" 2>/dev/null | wc -l) OK_A1"
echo "Em curso:            $(ps -eo comm= | grep -cx 'opp_run') processos opp_run"
if [ -f "$HERE/driver.pid" ] && kill -0 "$(cat "$HERE/driver.pid")" 2>/dev/null; then echo "Driver:              ativo (PID $(cat "$HERE/driver.pid"))"; else echo "Driver:              parado"; fi
echo "Últimas runs terminadas:"; tail -n 5 "$L/progress.tsv" 2>/dev/null | column -t -s $'\t'
