# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account

from pathlib import Path
from getpass import getpass

load_dotenv()

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account_one = Account.from_key(os.getenv("mnemonic"))


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Import constants.py and necessary functions from bit and web3
from constants import *
from bit import *
from web3 import Web3
from bit import wif_to_key
 
 
# Create a function called `derive_wallets`
def derive_wallets(coin, mnemonic=mnemonic, depth=3):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

derive_wallets()
# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {'btc': derive_wallets(mnemonic=mnemonic,coin=BTC,numderive=3),'eth':derive_wallets(mnemonic=mnemonic,coin=ETH,numderive=3),'btc-test': derive_wallets(mnemonic=mnemonic,coin=BTCTEST,numderive=3)}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    elif coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    
ethprivkeyey = coins["eth"][0]['privkey']
btctestprivkey = coins['btc-test'][1]['privkey']
# print(ethprivkeyey)
# print(btctestprivkey)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }

            
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()


