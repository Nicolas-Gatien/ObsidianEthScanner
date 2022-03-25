from unittest import result
from requests import get
from mdutils.mdutils import MdUtils

import datetime
import os

# Constants
API_KEY = "QQCFPZXGZPDPRK7CKMM6GIPJTMGRM3CX8J"
BASE_URL = "https://api.etherscan.io/api"

transactionQueue = []

# Classes
class Colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Block:
    def __init__(self, number, timestamp, miner, transactions):
        self.number = number
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions

class Transaction:
    def __init__(self, fromAddr, toAddr, amount, hash):
        self.hash = hash
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.amout = amount

class Account:
    pass

def get_timestamp():
    now = datetime.datetime.now()
    unixNow = datetime.datetime.timestamp(now)*1000
    latestTimestamp = int(int(unixNow)/1000)
    return latestTimestamp

def get_latest_block():
    url = BASE_URL + f"?module=block&action=getblocknobytime&timestamp={get_timestamp()}&closest=before&apikey={API_KEY}"
    response = get(url)
    data = response.json()
    blockNum = data["result"]

    response = get(get_block_url(blockNum))
    data = response.json()["result"]
    blockMiner = data["blockMiner"]
    timestamp = data["timeStamp"]

    txResponse = get(get_transactions(blockNum))
    txData = txResponse.json()["result"]
    
    return Block(blockNum, timestamp, blockMiner, txData)

def get_block_url(number):
    url = BASE_URL + f"?module=block&action=getblockreward&blockno={number}&apikey={API_KEY}"
    return url

def get_transactions(blockNum):
    url = BASE_URL + f"?module=account&action=txlistinternal&startblock={blockNum}&endblock={blockNum}&page=1&offset=100&sort=asc&apikey={API_KEY}"
    return url

def get_balance(address):
    url = BASE_URL + f"?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}"
    return url

def construct_account_file(hash):
    if(hash != ""):
        accMdFile = MdUtils(file_name=hash,title=("Account: " + hash))
        accMdFile.new_line("#📜Account")

        response = get(get_balance(hash))
        balance = response.json()["result"]
        accMdFile.new_line(f"Balance: {int(balance) / (10 ** 18)} Ether")

        accMdFile.create_md_file()

def construct_block_file(block):
    construct_account_file(block.miner)
    lastBlock = int(block.number) - 1
    nextBlock = int(block.number) + 1
    print(f"{Colours.OKGREEN}Found Block #{block.number}{Colours.ENDC}")

    if (find(block.number + ".md", "./") == "None"):
        mdFile = MdUtils(file_name=block.number,title=("Block #" + block.number))
        mdFile.new_line("#🧊Block")
        mdFile.new_line(f"Last Block: [[{lastBlock}]]")
        mdFile.new_line(f"Next Block: [[{nextBlock}]]")
        mdFile.new_line(f"Miner: [[{block.miner}]]")

        mdFile.new_line(f"\n Transactions:")

        lastHash = ""
        txCount = 0
        for tx in block.transactions:
            transactionQueue.append(Transaction(tx["from"], tx["to"], int(tx["value"]) / (10 ** 18), tx["hash"]))
            print(len(transactionQueue))
            txCount += 1

            '''construct_account_file(toAddr)
            construct_account_file(fromAddr)'''

            '''fileCreated = False
            while(fileCreated == False):
                txMdFile = MdUtils(file_name=hash,title=("Transaction Hash: " + hash))
                txMdFile.new_line("#💸Transaction")
                txMdFile.new_line(f"Block: [[{block.number}]]")
                txMdFile.new_line(f"From: [[{fromAddr}]]")
                txMdFile.new_line(f"To: [[{toAddr}]]")
                txMdFile.new_line(f"Transferred: {int(value) / (10 ** 18)} Ether")
                txMdFile.create_md_file()
                print(f"{Colours.OKGREEN}{txCount}. Creating Transaction File: {hash}{Colours.ENDC}")
                if (find(hash + ".md", "./") != "None"):
                    fileCreated = True

            if hash != lastHash:
                mdFile.new_line(f"[[{hash}]]")
            
            lastHash = hash'''
        mdFile.create_md_file()
    
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        else:
            return "None"

blockCount = 0
checkCount = 0
lastCheckBlock = ""
while(blockCount < 25):
    block = get_latest_block()
    checkCount += 1
    if(block.number != lastCheckBlock):
        construct_block_file(block)
        blockCount += 1
        checkCount = 0
    else:
        print(f"{Colours.WARNING}{checkCount} No New Blocks | Current Count: {block.number}{Colours.ENDC}")
    lastCheckBlock = block.number
