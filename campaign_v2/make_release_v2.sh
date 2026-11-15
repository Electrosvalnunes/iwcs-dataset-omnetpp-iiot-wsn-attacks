#!/usr/bin/env bash
# Prepara campaign_v2/release/: extrai, verifica e copia o CSV v2 com o seu sha256.
#   uso: ./make_release_v2.sh [--allow-partial]
#   Sem --allow-partial, exige as 600 runs (20 células x runs 0-29) e zero falhas nas verificações.
set -euo pipefail
export LC_ALL=C
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REL=$HERE/release
PARTIAL=0; [ "${1:-}" = "--allow-partial" ] && PARTIAL=1

python3 -I "$HERE/extract_v2.py" --strict
if [ $PARTIAL = 1 ]; then
  python3 -I "$HERE/make_tables_v2.py"
else
  python3 -I "$HERE/make_tables_v2.py" --require-complete
fi

cp "$HERE/features_v2.csv" "$REL/iwcs_v2_features.csv"
( cd "$REL" && sha256sum iwcs_v2_features.csv > iwcs_v2_features.csv.sha256 && sha256sum -c iwcs_v2_features.csv.sha256 )
N=$(($(wc -l < "$REL/iwcs_v2_features.csv") - 1))
if [ $PARTIAL = 1 ] && [ "$N" -lt 600 ]; then
  echo "PARCIAL: $N/600 runs ($(date -Is)). NÃO publicar." > "$REL/RELEASE_STATUS.txt"
else
  echo "COMPLETO: $N/600 runs ($(date -Is))." > "$REL/RELEASE_STATUS.txt"
fi
cat "$REL/RELEASE_STATUS.txt"
