import os
from web3 import Web3
from eth_account import Account
from eth_utils import to_checksum_address

w3 = Web3(Web3.HTTPProvider('https://ethereum-holesky-rpc.publicnode.com/'))

contract_address = '0x7dE939f946034fc99908E83491C8D01412BbF998'  
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "address[]",
                "name": "recipients",
                "type": "address[]"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "multiSend",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getContractBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]  

contract = w3.eth.contract(address=contract_address, abi=contract_abi)


owner_private_key = 'cfe7b12d35c313168008efd31e188e465ccaab0a032a3d6a97c6c04a3d94872d'

def get_addresses_from_keys(keys_dir):
    addresses = []
    for filename in os.listdir(keys_dir):
        if filename.endswith('-ecdsa'):
            with open(os.path.join(keys_dir, filename), 'r') as f:
                private_key = f.read().strip()
                account = Account.from_key(private_key)
                addresses.append(to_checksum_address(account.address))
    return addresses

def chunk_addresses(addresses, chunk_size=32):
    """Adresleri belirtilen boyutta gruplara ayırır."""
    for i in range(0, len(addresses), chunk_size):
        yield addresses[i:i + chunk_size]

def multi_send(addresses, amount_in_ether):
    amount_in_wei = w3.to_wei(amount_in_ether, 'ether')
    owner_address = w3.eth.account.from_key(owner_private_key).address
    
    for chunk in chunk_addresses(addresses):
        total_amount = amount_in_wei * len(chunk)

        
        nonce = w3.eth.get_transaction_count(owner_address)
        tx = contract.functions.multiSend(chunk, amount_in_wei).build_transaction({
            'from': owner_address,
            'value': total_amount,
            'gas': 3000000,  
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        
        signed_tx = w3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        print(f"Transaction sent for {len(chunk)} addresses: {tx_hash.hex()}")
        
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction confirmed in block {receipt['blockNumber']}")


def main():
    keys_dir = 'threshold-encryption/keys/'
    amount_to_send = 0.01  

    addresses = get_addresses_from_keys(keys_dir)
    print(f"Found {len(addresses)} addresses")

    multi_send(addresses, amount_to_send)

if __name__ == "__main__":
    main()