# Libraries
from data_types import Block, Transaction, Account, NFT
from requests import get

import datetime

# Variables
# Queues
queue_blocks = [Block]
queue_transactions = [Transaction]
queue_accounts = [Account]

# Constants
API_KEY = "QQCFPZXGZPDPRK7CKMM6GIPJTMGRM3CX8J"
BASE_URL = "https://api.etherscan.io/api"

def Block_URL(block_number):
    url = BASE_URL + f"?module=block&action=getblockreward&blockno={block_number}&apikey={API_KEY}"
    return url

def Transactions_URL(block_number):
    url = BASE_URL + f"?module=account&action=txlistinternal&startblock={block_number}&endblock={block_number}&page=1&offset=500&sort=asc&apikey={API_KEY}"
    return url

def Get_Latest_Block_Number():
    # Get Latest Timestamp
    now = datetime.datetime.now()
    latest_timestamp = datetime.datetime.timestamp(now)
    
    # Fetch Block Using Latest Timestamp
    url = BASE_URL + f"?module=block&action=getblocknobytime&timestamp={latest_timestamp}&closest=before&apikey={API_KEY}"
    response = get(url)
    data = response.json()
    block_number = data["result"]

    return block_number

def Add_Block_To_Queue(block_number):
    block_response = get(Block_URL(block_number))
    data = block_response.json()["result"]

    block_miner = data["blockMiner"]
    timestamp = data["timeStamp"]

    transaction_response = get(Transactions_URL(block_number))
    transactions = transaction_response.json()["result"]
    
    return Block(block_number, timestamp, block_miner, transactions)

# Get Latest Block Number
# Add The Last 5 Blocks to a Queue

# Delete Old Blocks
# Delete Old Transactions
# Delete Old Accounts

# Loop Through Block Queue
# Add All Transactions to TransactionQueue
# Get Block Miner
# Create Block File

# Loop Through Transaction Queue
# Add All Accounts to AccountQueue
# Get Amount Transfered
# Create Transaction File

# Loop Through Each Account
# Get Eth In Balance
# Get Account Type (Miner, Smart Contract, User)
# Create Account File

while (True):
    pass