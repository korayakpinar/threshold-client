# threshold-client

```sh
cd threshold-encryption
cargo build --release
cargo build --release --example mempool
docker build -t mempool .
cargo run --release --example create_keys -- -n comittee_size -k key_count
docker-compose up -d

cd ../network
go build main.go

cd ..
docker build -t threshold-client .
docker-compose up
```