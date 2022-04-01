class Block:
    def __init__(self, number, timestamp, miner, transactions):
        self.number = number
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions

class Transaction:
    def __init__(self, from_address, to_address, amount, hash):
        self.hash = hash
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

class Account:
    def __init__(self, address, balance, account_type):
        self.address = address
        self.balace = balance
        self.account_type = account_type

class NFT:
    def __init__(self, hash):
        self.hash = hash