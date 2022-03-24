from unittest import result
from requests import get
from mdutils.mdutils import MdUtils

import datetime
import os

API_KEY = "QQCFPZXGZPDPRK7CKMM6GIPJTMGRM3CX8J"
address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"

BASE_URL = "https://api.etherscan.io/api"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_latest_block(timestamp):
    url = BASE_URL + f"?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={API_KEY}"
    return url

def get_block(number):
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

def construct_block_file(url):
    response = get(url)
    data = response.json()["result"]
    blockNum = data["blockNumber"]
    blockMiner = data["blockMiner"]
    construct_account_file(blockMiner)
    lastBlock = int(blockNum) - 1
    nextBlock = int(blockNum) + 1
    print(f"{bcolors.OKGREEN}Found Block #{blockNum}{bcolors.ENDC}")

    if (find(blockNum + ".md", "./") == "None"):
        mdFile = MdUtils(file_name=blockNum,title=("Block #" + blockNum))
        mdFile.new_line("#🧊Block")
        mdFile.new_line(f"Last Block: [[{lastBlock}]]")
        mdFile.new_line(f"Next Block: [[{nextBlock}]]")
        mdFile.new_line(f"Miner: [[{blockMiner}]]")

        mdFile.new_line(f"\n Transactions:")

        txResponse = get(get_transactions(blockNum))
        txData = txResponse.json()["result"]

        lastHash = ""
        txCount = 0
        for tx in txData:
            toAddr = tx["to"]
            fromAddr = tx["from"]
            hash = tx["hash"]
            value = tx["value"]
            txCount += 1

            construct_account_file(toAddr)
            construct_account_file(fromAddr)

            fileCreated = False
            while(fileCreated == False):
                txMdFile = MdUtils(file_name=hash,title=("Transaction Hash: " + hash))
                txMdFile.new_line("#💸Transaction")
                txMdFile.new_line(f"Block: [[{blockNum}]]")
                txMdFile.new_line(f"From: [[{fromAddr}]]")
                txMdFile.new_line(f"To: [[{toAddr}]]")
                txMdFile.new_line(f"Transferred: {int(value) / (10 ** 18)} Ether")
                txMdFile.create_md_file()
                print(f"{bcolors.OKGREEN}{txCount}. Creating Transaction File: {hash}{bcolors.ENDC}")
                if (find(hash + ".md", "./") != "None"):
                    fileCreated = True

            if hash != lastHash:
                mdFile.new_line(f"[[{hash}]]")
            
            lastHash = hash
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
    now = datetime.datetime.now()
    unixNow = datetime.datetime.timestamp(now)*1000
    blockURL = get_latest_block(int(int(unixNow)/1000))
    response = get(blockURL)
    data = response.json()
    blockNum = data["result"]
    checkCount += 1
    if(blockNum != lastCheckBlock):
        construct_block_file(get_block(blockNum))
        blockCount += 1
        checkCount = 0
    else:
        print(f"{bcolors.WARNING}{checkCount} No New Blocks | Current Count: {blockCount}{bcolors.ENDC}")
    lastCheckBlock = blockNum