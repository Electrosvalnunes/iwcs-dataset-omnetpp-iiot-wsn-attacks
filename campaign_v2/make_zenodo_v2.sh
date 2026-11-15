#!/usr/bin/env bash
# =============================================================================
# Monta o pacote Zenodo da IWCS v2.0.0 em campaign_v2/zenodo_v2/:
#   iwcs_v2_features.csv (+ .sha256)          cópia de release/ (verificada)
#   iwcs_v2_raw_sca.zip                       600 .sca + 600 .ok + progress.tsv/launches.txt
#   iwcs_v2_code_and_provenance.zip           código RPL, patch INET, .ini/.ned, cells.csv,
#                                             scripts, manifest (+ adendo A1), docs/verificacao
#   legacy_v1.1.zip                           README DEPRECATED + RUN_ID_REGIME.md
#   README.md, CITATION.cff, LICENSES.md, ZENODO_*.txt     texto (versionados em git)
#   SHA256SUMS                                sha256 de todos os ficheiros a carregar
# Só usa ficheiros versionados em git (git ls-files) para o código; não inclui binários.
#   uso: ./make_zenodo_v2.sh
# =============================================================================
set -euo pipefail
export LC_ALL=C TZ=UTC
HERE=$(cd "$(dirname "$0")" && pwd)
PROJ=$(dirname "$HERE")
INET=$(cd "$PROJ/../inet" && pwd)
OUT=$HERE/zenodo_v2
STAGE=$(mktemp -d); trap 'rm -rf "$STAGE"' EXIT
cd "$PROJ"

# 0. pré-condições: release completa e sem alterações por commitar no código
grep -q '^COMPLETO: 600/600' "$HERE/release/RELEASE_STATUS.txt" || { echo "ERRO: release não está COMPLETA" >&2; exit 1; }
(cd "$HERE/release" && sha256sum -c --quiet iwcs_v2_features.csv.sha256)
[ "$(ls "$HERE"/results/*.sca | wc -l)" = 600 ] && [ "$(ls "$HERE"/results/*.ok | wc -l)" = 600 ] || { echo "ERRO: esperadas 600 .sca e 600 .ok" >&2; exit 1; }
if ! git diff --quiet HEAD -- src simulations inet campaign_v2 docs; then
  echo "ERRO: há alterações por commitar no código/proveniência" >&2; exit 1
fi
REV=$(git rev-parse HEAD)
INET_TAG=ambiente-revisao-v1
INET_BASE=a3bcad9   # "Estado inicial antes do patch RPL" (INET 4.2.10 sem alterações)

# (a) CSV
cp "$HERE/release/iwcs_v2_features.csv" "$HERE/release/iwcs_v2_features.csv.sha256" "$OUT/"

# (b) dados brutos
rm -f "$OUT/iwcs_v2_raw_sca.zip"
mkdir -p "$STAGE/raw/iwcs_v2_raw_sca/results" "$STAGE/raw/iwcs_v2_raw_sca/campaign_logs"
cp -p "$HERE"/results/*.sca "$HERE"/results/*.ok "$STAGE/raw/iwcs_v2_raw_sca/results/"
cp -p "$HERE/logs/progress.tsv" "$HERE/logs/launches.txt" "$STAGE/raw/iwcs_v2_raw_sca/campaign_logs/"
(cd "$STAGE/raw" && find iwcs_v2_raw_sca -type f | sort | zip -q -X -9 -@ "$OUT/iwcs_v2_raw_sca.zip")

# (c) código e proveniência
C=$STAGE/code/iwcs_v2_code_and_provenance
mkdir -p "$C"
git ls-files -z -- src simulations inet docs/verificacao campaign_v2 Makefile README.md .project .nedfolders .oppbuildspec \
 | grep -zvE '^src/libMAIO_RPL27\.so$|^simulations/.*\.anf$|^campaign_v2/\.gitignore$|^campaign_v2/release/|^campaign_v2/make_zenodo_v2\.sh$|^campaign_v2/zenodo_v2/' \
 | grep -zvE '^simulations/omnetpp_RPL_(64_IEEEP2|EDITAR_IEEEP3|EDITAR_IEEEP3_FLOODING_HOST4_CORRIGIDO|EDITAR_IEEEP4|MP2P_2026|MP2P_IEEE)\.ini$' \
 | xargs -0 -I{} cp --parents {} "$C/"
cp "$HERE/make_zenodo_v2.sh" "$C/campaign_v2/"
mkdir -p "$C/inet_patch"
git -C "$INET" diff "$INET_BASE" "$INET_TAG" > "$C/inet_patch/inet-4.2.10_rpl_patch_${INET_TAG}.diff"
cat > "$C/inet_patch/README.txt" <<EOF
Patch applied to INET 4.2.10 (inet-4.2.10-src.tgz) for this campaign.
Generated with: git diff ${INET_BASE} ${INET_TAG}   (in the INET repository)
  ${INET_BASE} = unmodified INET 4.2.10 tree before the patch
  ${INET_TAG} = $(git -C "$INET" rev-parse "$INET_TAG^{commit}")
Apply from the INET root:  patch -p1 < inet-4.2.10_rpl_patch_${INET_TAG}.diff
The same files are also provided, already patched, under ../inet/ (RPL project layout).
Build: OMNeT++ 5.7.1, INET 4.2.10 in release mode with the Visualization feature ON
(every .ned uses IntegratedCanvasVisualizer); the RPL project needs MSGC:=\$(MSGC) --msg6.
Exact binaries, hashes and command line: ../campaign_v2/manifest.txt.
EOF
cp "$OUT/LICENSES.md" "$C/LICENSES.md"
mkdir -p "$C/LICENSES"
cp /usr/share/common-licenses/GPL-3 "$C/LICENSES/GPL-3.0.txt"
cp /usr/share/common-licenses/LGPL-2.1 "$C/LICENSES/LGPL-2.1.txt"
sed -n '/^## MIT License/,$p' "$OUT/LICENSES.md" | tail -n +3 > "$C/LICENSES/MIT.txt"
echo "git commit (MAIO_RPL27): $REV" > "$C/SOURCE_REVISION.txt"
echo "INET tag $INET_TAG: $(git -C "$INET" rev-parse "$INET_TAG^{commit}")" >> "$C/SOURCE_REVISION.txt"
rm -f "$OUT/iwcs_v2_code_and_provenance.zip"
(cd "$STAGE/code" && find iwcs_v2_code_and_provenance -type f | sort | zip -q -X -9 -@ "$OUT/iwcs_v2_code_and_provenance.zip")

# (d) legado
mkdir -p "$STAGE/leg/legacy_v1.1"
cp "$HERE/release/legacy_v1.1/README.md" "$HERE/release/legacy_v1.1/RUN_ID_REGIME.md" "$STAGE/leg/legacy_v1.1/"
rm -f "$OUT/legacy_v1.1.zip"
(cd "$STAGE/leg" && find legacy_v1.1 -type f | sort | zip -q -X -9 -@ "$OUT/legacy_v1.1.zip")

# verificação e SHA256SUMS
for z in "$OUT"/*.zip; do unzip -tq "$z" >/dev/null; done
[ "$(unzip -Z1 "$OUT/iwcs_v2_raw_sca.zip" | grep -c '\.sca$')" = 600 ]
[ "$(unzip -Z1 "$OUT/iwcs_v2_raw_sca.zip" | grep -c '\.ok$')" = 600 ]
(cd "$OUT" && sha256sum iwcs_v2_features.csv iwcs_v2_features.csv.sha256 iwcs_v2_raw_sca.zip \
   iwcs_v2_code_and_provenance.zip legacy_v1.1.zip README.md CITATION.cff LICENSES.md > SHA256SUMS)
ls -l "$OUT"
