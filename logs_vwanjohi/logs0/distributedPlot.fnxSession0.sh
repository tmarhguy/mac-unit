#!/bin/sh


# generated at: Mon Oct 19 23:04:33 2026
# 
unset LD_LIBRARY_PATH
unset CDS_W3264_LIBPATH
unset W3264_USER_PATH
unset W3264_USER_LIBPATH
unset OS_ID
unset REL_VERSION

LOGDIR="/vast/projects/radway/ese-5700-fall/tmarhguy/project_1/logs_vwanjohi/logs0/"
OUTPUTLOG="/vast/projects/radway/ese-5700-fall/tmarhguy/project_1/logs_vwanjohi/logs0/distributedPlot.fnxSession0.log"
export CDSHOME="/vast/projects/radway/cad-tools/cadence/installs/IC231"

env >$LOGDIR/distributedPlot.fnxSession0.env.log 2>/dev/null
BLDVER="`$CDSHOME/bin/srrversion -build 2>/dev/null `"

#
if [ -z "$DISPLAY" ]; then
    export DISPLAY=10.218.10.114:7.0
fi

#

if [ "$BLDVER" =  "" ]; then
    echo "[`date`] Error: target machine (`hostname`) cannot run ViVA. Probably wrong system.">$LOGDIR/distributedPlot.fnxSession0.err
    sync $LOGDIR/distributedPlot.fnxSession0.err
    exit 1
fi
#
$CDSHOME/bin/srrversion -sysinfo >>$LOGDIR/distributedPlot.fnxSession0.env.log 2>/dev/null
$CDSHOME/bin/srrversion -envinfo >>$LOGDIR/distributedPlot.fnxSession0.env.log 2>/dev/null
#
# Check for X11 connectivity....
ERR="`srrversion -x11`"
if [ "$ERR" != "OK" ]; then
    echo "[`date`] Error: $ERR.">$LOGDIR/distributedPlot.fnxSession0.err
    exit 1
fi
# 
# 
export CDN_VIVA_SERVICE_LINGER_TIME=60
export CDN_VIVA_SERVICE_SEND_JSON_GRPC=1
# 
CMD="$CDSHOME/bin/viva  -brokerAddress epyc-2-12:37521 -tag 3a3a842034f3a15a1640de4bfff79fd6 -axlsession fnxSession0 -libCellView proj1_lib:tb_read_col:maestro -adeService distribuedPlot -noautostart  -distributedPlot 1 -log /vast/projects/radway/ese-5700-fall/tmarhguy/project_1/logs_vwanjohi/logs0/distributedPlot.0.log -no-ciw -nocdsinit"


WORK_DIR=/vast/projects/radway/ese-5700-fall/tmarhguy/project_1
if [ -d $WORK_DIR ]; then
    cd $WORK_DIR
    $CMD &
    PID=$!
    wait $PID
fi


