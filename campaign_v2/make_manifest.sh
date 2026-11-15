#!/usr/bin/env bash
# Gera o manifest do ambiente da campanha IWCS v2 (stdout).
#   sem argumentos: manifest estático (versionado em manifest.txt)
#   --launch:       acrescenta data/hora e HEAD no momento do lançamento
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJ=$(dirname "$HERE"); INET=$(cd "$PROJ/../inet" && pwd)
O=${OMNETPP_ROOT:-$HOME/Downloads/omnetpp-5.7.1}
g() { git -C "$1" "${@:2}"; }
echo "# Manifest - campanha IWCS v2"
if [ "${1:-}" = "--launch" ]; then
  echo "launch_time: $(date -Is)"
  echo "MAIO_RPL27_HEAD: $(g "$PROJ" rev-parse HEAD)  dirty_files: $(g "$PROJ" status --porcelain --untracked-files=no | wc -l)"
fi
echo
echo "## Repositórios (tag ambiente-revisao-v1)"
echo "MAIO_RPL27 tag ambiente-revisao-v1 -> $(g "$PROJ" rev-parse 'ambiente-revisao-v1^{commit}')"
echo "MAIO_RPL27 src/ e simulations/ idênticos à tag: $(g "$PROJ" diff --quiet 'ambiente-revisao-v1' HEAD -- src simulations && echo sim || echo NAO)"
echo "OMET57/inet tag ambiente-revisao-v1 -> $(g "$INET" rev-parse 'ambiente-revisao-v1^{commit}')"
echo "OMET57/inet HEAD -> $(g "$INET" rev-parse HEAD)  (igual à tag: $([ "$(g "$INET" rev-parse HEAD)" = "$(g "$INET" rev-parse 'ambiente-revisao-v1^{commit}')" ] && echo sim || echo NAO))"
echo
echo "## Versões"
echo "OMNeT++: $("$O/bin/opp_run" -v 2>/dev/null | grep -E '^Version' | head -1)  ($O)"
echo "INET: $(cat "$INET/Version")  (INETDefs.h: $(grep -E 'define INET_(VERSION|PATCH_LEVEL)' "$INET/src/inet/common/INETDefs.h" | awk '{print $2"="$3}' | tr '\n' ' '))"
echo "Compilador: $(clang++ --version 2>/dev/null | head -1)"
echo "SO: $(uname -sr)"
echo
echo "## Binários e entradas (sha256)"
for f in "$INET/src/libINET.so" "$PROJ/src/libMAIO_RPL27.so" \
         "$PROJ"/simulations/omnetpp_RPL_GRID{35,48,63,99}_NORMAL.ini "$PROJ"/simulations/RplNetworkGrid{35,48,63,99}.ned \
         "$PROJ"/src/Rpl.ned "$HERE/cells.csv" "$HERE/run_campaign.sh"; do
  echo "$(sha256sum "$f" | cut -c1-64)  OMET57/${f#$(dirname "$PROJ")/}"
done
echo
echo "## Linha de comando exata por run (cwd = MAIO_RPL27/simulations)"
echo "opp_run -u Cmdenv -l <MAIO_RPL27>/src/MAIO_RPL27 -n <MAIO_RPL27>/simulations:<MAIO_RPL27>/src:<OMET57>/inet/src \\"
echo "  -f <ini> -c <config> -r <run> --sim-time-limit=3600s --result-dir=<MAIO_RPL27>/campaign_v2/results \\"
echo "  '--**.vector-recording=false' --cmdenv-express-mode=true --cmdenv-status-frequency=600s"
echo
echo "## RNG"
echo "num-rngs=10 (cMersenneTwister, default); seed-set não definido => \${runnumber} (seedset = run); runs 0-29."
echo "Mapeamento: **.mobility.rng-0=1 (não usado: posições fixas), **.wlan[*].mac.rng-0=2, restantes módulos RNG 0."
echo
echo "## Canal (tal como corre)"
echo "As linhas **.radioMedium.attenuation.* dos .ini são inertes (não existe esse submódulo no INET 4.2.10)."
echo "Modelo efetivo: BreakpointPathLoss (l01=40.2, alpha1=2, l02=58.5, alpha2=3.3, breakpoint 8 m), sem shadowing."
