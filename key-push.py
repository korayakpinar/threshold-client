import json
import time
from pathlib import Path
from typing import List, Dict
from web3 import Web3
from web3.contract import Contract
from eth_account import Account
from eth_typing import Address

BATCH_SIZE = 32
TOTAL_NODES = 511
CONTRACT_ADDRESS = "0x58d9Fc02Cc93cf9d3e3316a7D0fF61673AA7eE38"

ETHEREUM_NODE_URL = "https://ethereum-holesky-rpc.publicnode.com"
CHAIN_ID = 17000
KEYS_DIR = "./threshold-encryption/keys"
IPFS_RESPONSES_FILE = "ipfs_responses.txt"
PRIVATE_KEY = "cfe7b12d35c313168008efd31e188e465ccaab0a032a3d6a97c6c04a3d94872d"
ABI_PATH = "./network/src/contracts/operators.abi"  # ABI dosyasının yolunu buraya ekleyin

def read_abi(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def read_ipfs_responses(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    responses = []
    for line in lines:
        parts = line.strip().split(" - ", 1)
        if len(parts) == 2:
            response = json.loads(parts[1])
            responses.append(response)
    return responses

def read_ethereum_addresses(directory: str) -> List[Address]:
    addresses = []
    for i in range(1, TOTAL_NODES + 1):
        file_name = f"{i}-ecdsa"
        file_path = Path(directory) / file_name
        with open(file_path, 'r') as file:
            private_key = file.read().strip()
        account = Account.from_key(private_key)
        addresses.append(account.address)
    return addresses

def append_operators(w3: Web3, contract: Contract, private_key: str, nodes: List[Dict]) -> None:
    account = Account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)
    
    tx = contract.functions.AppendMultipleOperators(nodes).build_transaction({
        'chainId': CHAIN_ID,
        'gas': 20000000,  # Adjust as needed
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"Transaction hash: {tx_receipt.transactionHash.hex()}")

def main():
    w3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE_URL))
    if not w3.is_connected():
        print("Failed to connect to Ethereum node")
        return

    abi = read_abi(ABI_PATH)
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

    ipfs_responses = read_ipfs_responses(IPFS_RESPONSES_FILE)
    eth_addresses = read_ethereum_addresses(KEYS_DIR)

    for i in range(0, TOTAL_NODES, BATCH_SIZE):
        end = min(i + BATCH_SIZE, TOTAL_NODES)
        nodes = [
            {"operator": eth_addresses[j], "blsPubKeyCID": ipfs_responses[j]['Hash']}
            for j in range(i, end)
        ]

        try:
            append_operators(w3, contract, PRIVATE_KEY, nodes)
            print(f"Operators successfully added (batch {i}-{end-1})")
        except Exception as e:
            print(f"Error adding operators (batch {i}-{end-1}): {e}")

        time.sleep(12)

if __name__ == "__main__":
    main()