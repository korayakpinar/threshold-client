source ./config.toml

echo "Building network & threshold-encryption"

go build ./network/main.go
cd threshold-encryption/
cargo build
cd ..

echo "Downloading transcript"

wget https://github.com/ethereum/kzg-ceremony/raw/main/transcript.json

threshold-encryption/target/threshold-encryption --transcript transcript.json --bls-key $blsKey --api-port $apiPort & 
echo "Api server started, waitin 15 seconds for initialization"
sleep 15
./network/main --port $port --privKey $privKey --rpc $rpc --port $proxyPort 

