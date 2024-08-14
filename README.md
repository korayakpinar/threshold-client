# threshold-client

```sh
cd threshold-encryption
cargo run --release --example mempool
docker build -t mempool .
docker-compose up -d

cd ../network
go build main.go

cd ..
docker build -t threshold-encryption .
docker-compose up
```