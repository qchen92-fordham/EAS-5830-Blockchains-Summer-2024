from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"


#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/55313acc19f041af8e48d88062d3d574"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

contract_address = Web3.toChecksumAddress(bayc_address)

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }
	
	# Get the owner of the ape
	owner = contract.functions.ownerOf(apeID).call()
	data['owner'] = owner

    # Get the token URI and fetch metadata
	token_uri = contract.functions.tokenURI(apeID).call()
	response = requests.get(token_uri)
	if response.status_code == 200:
		metadata = response.json()
		data['image'] = metadata['image']

        # Find the eyes attribute in the metadata
		for attribute in metadata['attributes']:
			if attribute['trait_type'].lower() == 'eyes':
				data['eyes'] = attribute['value']
				break

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

