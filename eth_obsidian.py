from unittest import result
from requests import get
from mdutils.mdutils import MdUtils
from threading import Thread
from data_types import Block, Account, Transaction, NFT

import datetime
import os

from nice_print import cyan_print, green_print, yellow_print

# Constants
API_KEY = "QQCFPZXGZPDPRK7CKMM6GIPJTMGRM3CX8J"
BASE_URL = "https://api.etherscan.io/api"

transaction_queue = []
account_queue = []

def GetBlockURL(block_number):
    url = BASE_URL + f"?module=block&action=getblockreward&blockno={block_number}&apikey={API_KEY}"
    return url

def GetLatestBlockURL():
    url = BASE_URL + f"?module=block&action=getblocknobytime&timestamp={GetLatestTimestamp()}&closest=before&apikey={API_KEY}"
    return url

def GetLatestTimestamp():
    now = datetime.datetime.now()
    latest_timestamp = int(datetime.datetime.timestamp(now))
    return latest_timestamp

def GetLatestBlockNumber():
    response = get(GetLatestBlockURL())
    data = response.json()
    block_number = data["result"]
    return block_number

def get_latest_block():
    block_number = GetLatestBlockNumber()

    response = get(GetBlockURL(block_number))
    data = response.json()["result"]
    block_miner = data["blockMiner"]
    timestamp = data["timeStamp"]

    transaction_response = get(get_transactions(block_number))
    transaction_data = transaction_response.json()["result"]

    return Block(block_number, timestamp, block_miner, transaction_data)

def get_transactions(blockNum):
    url = BASE_URL + f"?module=account&action=txlistinternal&startblock={blockNum}&endblock={blockNum}&page=1&offset=500&sort=asc&apikey={API_KEY}"
    return url

def get_balance(address):
    url = BASE_URL + f"?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}"
    return url

def construct_account_file(hash):
    if(hash != ""):
        account_md_file = MdUtils(file_name=f"vault/{hash}",title=("Account: " + hash))
        account_md_file.new_line("#📜Account")

        response = get(get_balance(hash))
        balance = response.json()["result"]
        account_md_file.new_line(f"Balance: {int(balance) / (10 ** 18)} Ether")

        account_md_file.create_md_file()

def construct_transaction_file(block):
    for tx in range(len(transaction_queue)):
        if tx < len(transaction_queue):
            ClearVault()
            transaction = transaction_queue[tx]
            transaction_md_file = MdUtils(file_name=f"vault/{transaction.hash}",title=("Transaction Hash: " + transaction.hash))
            transaction_md_file.new_line("#💸Transaction")
            transaction_md_file.new_line(f"Block: [[{block.number}]]")
            transaction_md_file.new_line(f"From: [[{transaction.from_address}]]")
            transaction_md_file.new_line(f"To: [[{transaction.to_address}]]")
            transaction_md_file.new_line(f"Transferred: {transaction.amount} Ether")

            cyan_print(f"{transaction.hash}")

            transaction_md_file.create_md_file()
            if(len(transaction_queue)>0):
                transaction_queue.pop(tx)

        '''construct_account_file(transaction.toAddr)
        construct_account_file(transaction.fromAddr)'''


def construct_block_file(block):
    construct_account_file(block.miner)
    last_block = int(block.number) - 1
    next_block = int(block.number) + 1
    green_print(f"Found Block #{block.number}")

    if (find(block.number + ".md", "./") == "None"):
        md_file = MdUtils(file_name=f"vault/{block.number}",title=("Block #" + block.number))
        md_file.new_line("#🧊Block")
        md_file.new_line(f"Last Block: [[{last_block}]]")
        md_file.new_line(f"Next Block: [[{next_block}]]")
        md_file.new_line(f"Miner: [[{block.miner}]]")

        md_file.new_line(f"\n Transactions:")

        lastHash = ""
        txCount = 0
        for tx in block.transactions:
            transaction_queue.append(Transaction(tx["from"], tx["to"], int(tx["value"]) / (10 ** 18), tx["hash"]))
            txCount += 1
        md_file.create_md_file()
        print(f"{len(transaction_queue)} Transactions Found")

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        else:
            return "None"

def ClearVault():
    path = "vault/"
    max_Files = 100
    
    def sorted_ls(path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))
    
    del_list = sorted_ls(path)[0:(len(sorted_ls(path))-max_Files)]
    
    for dfile in del_list:
        if(path + dfile == "vault/.obisidan"):
            pass
        else:
            os.remove(path + dfile)


'''blocks_created = 0
check_count = 0
latest_block_found = ""
while(blocks_created < 250):
    block = get_latest_block()
    check_count += 1

    if(len(transaction_queue)> 0):
        thread = Thread(target = construct_transaction_file())
        thread.start()
        thread.join()

    if(block.number != latest_block_found):
        construct_block_file(block)

        blocks_created += 1
        check_count = 0
    else:
        yellow_print(f"{check_count} No New Blocks | Current Count: {block.number} | Transaction Queue: {len(transaction_queue)}")
    latest_block_found = block.number'''
