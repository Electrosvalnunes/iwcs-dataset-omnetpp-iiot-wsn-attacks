#!/usr/bin/env bash
# Lote 1 (runs 0-9) e, quando terminar, lote 2 (runs 10-29). Pensado para correr
# destacado do terminal/Claude Desktop:
#   setsid nohup ./run_batches.sh > logs/driver.log 2>&1 < /dev/null &
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
echo $$ > "$HERE/driver.pid"
"$HERE/make_manifest.sh" --launch >> "$HERE/logs/launches.txt"
"$HERE/run_campaign.sh" 0 9
"$HERE/run_campaign.sh" 10 29
echo "[$(date -Is)] campanha terminada"
rm -f "$HERE/driver.pid"
