#!/bin/bash
/app/silent-threshold --api-port $APIPORT --mempool-url $MEMPOOLURL --committee-size $COMITTEESIZE & 
sleep 2
/app/network -topic $TOPICNAME -keys $KEYSPATH -rpcURL $RPCURL \
    -proxyPort $PROXYPORT -apiPort $APIPORT -contractAddr $CONTRACTADDR \
    -committeeSize $COMITTEESIZE -networkSize $NETWORKSIZE -networkIndex $NETWORKINDEX -ipfsGatewayURL $IPFSGATEWAYURL -adminKey $ADMINKEY &

wait