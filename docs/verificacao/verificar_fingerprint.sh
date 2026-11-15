#!/usr/bin/env bash
# Verifica que duas builds de libMAIO_RPL27.so produzem simulações idênticas.
#
# Uso: verificar_fingerprint.sh <dir_lib_antes> <dir_lib_depois> <dir_saida> <ini> <config> [sim_time] [run]
#   <dir_lib_*> contêm libMAIO_RPL27.so (p.ex. extraída com `git show <commit>:src/libMAIO_RPL27.so`)
#   Executar a partir de MAIO_RPL27/simulations, com o OMNeT++ 5.7.1 no PATH.
#
# Passos: (1) corre "antes" e obtém o fingerprint tplx; (2) corre "depois" exigindo
# esse fingerprint (o OMNeT++ verifica); (3) compara .sca e .vec ignorando apenas
# os atributos de cabeçalho que mudam sempre (runId, datetime, processid, resultdir).
set -u
LIB_A=$1; LIB_D=$2; OUT=$3; INI=$4; CFG=$5; T=${6:-200s}; RUN=${7:-0}
mkdir -p "$OUT"
COMMON=(-u Cmdenv -n .:../src:../../inet/src -f "$INI" -c "$CFG" -r "$RUN" --sim-time-limit="$T" --cmdenv-express-mode=true)

opp_run "${COMMON[@]}" -l "$LIB_A/MAIO_RPL27" --result-dir="$OUT/antes" --fingerprint=0000-0000/tplx > "$OUT/antes.log" 2>&1
FP=$(grep -oP 'calculated: \K[0-9a-f]{4}-[0-9a-f]{4}/tplx' "$OUT/antes.log")
EV_A=$(grep -oP 'event #\K[0-9]+' "$OUT/antes.log" | tail -1)

opp_run "${COMMON[@]}" -l "$LIB_D/MAIO_RPL27" --result-dir="$OUT/depois" --fingerprint="$FP" > "$OUT/depois.log" 2>&1
EV_D=$(grep -oP 'event #\K[0-9]+' "$OUT/depois.log" | tail -1)
if grep -q "Fingerprint successfully verified: $FP" "$OUT/depois.log"; then FPOK=SIM; else FPOK=NAO; fi

strip_hdr() { grep -vE '^(run |attr (runId|datetime|processid|resultdir) |version )' "$1"; }
F="${CFG}-${RUN}"
diff <(strip_hdr "$OUT/antes/$F.sca") <(strip_hdr "$OUT/depois/$F.sca") > "$OUT/sca.diff"
REM=$(grep -c '^<' "$OUT/sca.diff"); ADD=$(grep -c '^>' "$OUT/sca.diff")
NEWNAMES=$(grep '^>' "$OUT/sca.diff" | awk '{print $4}' | sort | uniq -c | awk '{printf "%s(%s) ", $2, $1}')
if [ -f "$OUT/antes/$F.vec" ]; then
  if cmp -s <(strip_hdr "$OUT/antes/$F.vec") <(strip_hdr "$OUT/depois/$F.vec"); then VEC="identico ($(strip_hdr "$OUT/antes/$F.vec" | wc -l) linhas)"; else VEC=DIFERENTE; fi
else VEC="sem .vec"; fi

{
  echo "config=$CFG run=$RUN sim-time-limit=$T ini=$INI"
  echo "lib_antes  sha256=$(sha256sum "$LIB_A/libMAIO_RPL27.so" | cut -c1-64)"
  echo "lib_depois sha256=$(sha256sum "$LIB_D/libMAIO_RPL27.so" | cut -c1-64)"
  echo "fingerprint_antes=$FP eventos_antes=$EV_A"
  echo "fingerprint_depois_verificado=$FPOK eventos_depois=$EV_D"
  echo "sca_linhas_alteradas_ou_removidas=$REM"
  echo "sca_linhas_adicionadas=$ADD : $NEWNAMES"
  echo "vec=$VEC"
} | tee "$OUT/resumo.txt"
[ "$FPOK" = SIM ] && [ "$REM" = 0 ] && [ "$EV_A" = "$EV_D" ]
