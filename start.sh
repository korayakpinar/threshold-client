#!/bin/bash
/app/silent-threshold --bls-key $BLSKEY --api-port $APIPORT --mempool-url $MEMPOOLURL & 
sleep 2
/app/network -topic $TOPICNAME -privKey $PRIVKEY -rpcURL $RPCURL \
    -proxyPort $PROXYPORT -apiPort $APIPORT -contractAddr $CONTRACTADDR \
    -committeeSize $COMITTEESIZE -ipfsGatewayURL $IPFSGATEWAYURL &

wait