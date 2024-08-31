import os
import requests
from pathlib import Path
import json

# Configuration settings
IPFS_API_URL = "http://34.27.174.61:5001"
NUM_KEYS = 511

def unpin_all():
    try:
        # Get list of all pinned items
        response = requests.post(f"{IPFS_API_URL}/api/v0/pin/ls")
        if response.status_code != 200:
            print(f"Failed to get list of pinned items. Status code: {response.status_code}")
            return

        pinned_items = json.loads(response.text)
        
        # Unpin each item
        for cid in pinned_items.get('Keys', {}):
            unpin_response = requests.post(f"{IPFS_API_URL}/api/v0/pin/rm", params={'arg': cid})
            if unpin_response.status_code == 200:
                print(f"Unpinned: {cid}")
            else:
                print(f"Failed to unpin {cid}. Status code: {unpin_response.status_code}")
        
        print("All items have been unpinned.")
    except Exception as e:
        print(f"An error occurred while unpinning: {str(e)}")

def add_file_to_ipfs(file_path):
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(
                f"{IPFS_API_URL}/api/v0/add",
                files={'file': file}
            )
        return response.text
    except Exception as e:
        return f"Error occurred while adding file to IPFS: {str(e)}"

def main():
    # First, unpin all existing items
    unpin_all()

    try:
        with open('ipfs_responses.txt', 'w') as output_file:
            for index in range(1, NUM_KEYS + 1):
                file_name = f"{index}-pk"
                file_path = Path('./threshold-encryption/keys') / file_name
                
                # Read the file
                try:
                    with open(file_path, 'rb'):
                        pass
                except FileNotFoundError:
                    print(f"{file_name} file not found. Terminating process.")
                    break
                except Exception as e:
                    print(f"Error reading file: {str(e)}")
                    continue
                
                # Add to IPFS
                response = add_file_to_ipfs(file_path)
                if "Error" in response:
                    print(f"Error occurred while adding {file_name} to IPFS: {response}")
                    continue
                
                # Write response to file
                output_file.write(f"{index} - {response}\n")
                print(f"{file_name} added to IPFS.")
        
        print("Process completed. Responses saved to 'ipfs_responses.txt'.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()