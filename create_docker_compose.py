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
      - MEMPOOLURL=mempool
      - APIPORT=8081
      - KEYSPATH=/app/keys
      - TOPICNAME=458005e1367b74db64262ef76cda4f631183651ecdd978c0e7dc02dd65d862f1
      - PRIVKEY=/app/sk
      - RPCURL=https://ethereum-holesky.core.chainstack.com/355803c4d8982d49b6487545f3457c62
      - CONTRACTADDR=0xD7D5cB87F810fa9A1D11C7EB6934547Ec3DFAc74
      - PROXYPORT=8082
      - COMITTEESIZE={1}
      - NETWORKSIZE={1}
      - NETWORKINDEX={3}
      - IPFSGATEWAYURL=http://34.27.174.61
      - ADMINKEY=cfe7b12d35c313168008efd31e188e465ccaab0a032a3d6a97c6c04a3d94872d
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

    file = open("docker-compose.yml", "w")
    file.write(HEADER)

    for i in range(1, n + 1):
        file.write(TEMPLATE.format(i, n, 8082 + i - 1, i - 1))

    file.seek(file.tell() - 2, 0)
    file.truncate()

    file.close()


if __name__ == "__main__":
    main()