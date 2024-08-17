import sys

HEADER = """networks:
  my-custom-network:
    external:
      name: bridge_proxy

services:
  threshold_frontend:
    image: threshold-frontend
    ports:
      - "80:3000"

"""

TEMPLATE = """  threshold_node_{0}:
    image: threshold-client
    networks:
      - my-custom-network
    environment:
      - BLSKEY=/app/key
      - MEMPOOLURL=mempool
      - APIPORT=8081
      - TOPICNAME=458005e1367b74db64262ef76cda4f631183651ecdd978c0e7dc02dd65d862f1
      - PRIVKEY=/app/sk
      - RPCURL=https://ethereum-holesky-rpc.publicnode.com/
      - CONTRACTADDR=0xA6E24910b506b387365E8C685B255EB3bfbFb5DC
      - PROXYPORT=8082
      - COMITTEESIZE={1}
      - IPFSGATEWAYURL=https://moccasin-effective-harrier-491.mypinata.cloud
      - BEARERTOKEN=/app/bearertoken
    volumes:
      - ./threshold-encryption/keys/{0}-bls:/app/key
      - ./threshold-encryption/keys/{0}-ecdsa:/app/sk
    ports:
      - {2}:8082

"""


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 create_docker_compose.py <comittee_size>")

    n = int(sys.argv[1])
    assert(((n - 1) & (n)) == 0 and n != 0)

    file = open("docker-compose-1.yml", "w")
    file.write(HEADER)

    for i in range(1, n):
        file.write(TEMPLATE.format(i, n, 8082 + i - 1))

    file.seek(file.tell() - 2, 0)
    file.truncate()

    file.close()


if __name__ == "__main__":
    main()