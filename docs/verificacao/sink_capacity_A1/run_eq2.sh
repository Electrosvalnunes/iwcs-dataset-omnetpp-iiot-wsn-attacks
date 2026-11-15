#!/usr/bin/env bash
# uso: run_eq.sh INI CONFIG RUN TAG [opções extra...]
S=$(cd "$(dirname "$0")" && pwd); P=/home/osvaldo/Documentos/OMET57/MAIO_RPL27
export PATH=${OMNETPP_ROOT:-$HOME/Downloads/omnetpp-5.7.1}/bin:$PATH LD_LIBRARY_PATH=${OMNETPP_ROOT:-$HOME/Downloads/omnetpp-5.7.1}/lib:${LD_LIBRARY_PATH:-}
INI=$1 CFG=$2 RUN=$3 TAG=$4; shift 4
OUT=$S/$TAG; mkdir -p $OUT
cd $P/simulations && nice -n 5 opp_run -u Cmdenv -l $P/src/MAIO_RPL27 -n $P/simulations:$P/src:$P/../inet/src \
  -f $INI -c $CFG -r $RUN --sim-time-limit=3600s --result-dir=$OUT '--**.vector-recording=false' \
  --cmdenv-express-mode=true --cmdenv-status-frequency=600s --fingerprint=0000-0000/tplx,0000-0000/tplx "--fingerprint-modules=*,not **.sink*.energyStorage" "$@" > $OUT/log.txt 2>&1
echo "rc=$?" >> $OUT/log.txt
