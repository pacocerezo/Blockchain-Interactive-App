# Import hashing algorithm
from hashlib import sha256

# Function to help the hash function
def updatehash(*args):

    hashing_text = ""; h = sha256()

    # Adding args
    for arg in args:
        hashing_text += str(arg)

    # Hashing them & returning in hex
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Transaction():

    # Constructor
    def __init__(self, senderAddress, receiverAddress, amount):
        self.senderAddress = senderAddress
        self.receiverAddress = receiverAddress
        self.amount = amount

    # Get transaction hash
    def calculateHash(self):
        return sha256(self.senderAddress + self.receiverAddress + self.amount)

# What each block looks like
class Block():

    nonce = 0
    difficulty = 4

    # Constructor
    def __init__(self, transactions, previousHash = ''):
        self.transactions = transactions
        self.previousHash = previousHash
        self.hash = self.calculateHash()

    # Setting block's hash
    def calculateHash(self):
        return updatehash(
            self.previousHash,
            self.transactions,
            self.nonce
        )

    # Mining function to add pending tx's in new block
    def mine(self):
        while True:
            if self.calculateHash()[:self.difficulty] == "0" * self.difficulty:
                self.hash = self.calculateHash(); break
            else:
                self.nonce += 1

    # Method to print the block nicely
    def __str__(self):
        return str("Hash: %s\nPrevious: %s\nTx's: %s\nNonce: %s\n" %(
            self.calculateHash(),
            self.previousHash,
            self.transactions,
            self.nonce
            )
        )

# What our blockchain looks like
class Blockchain():

    # Number of starting zeros required for hash riddle solution
    difficulty = 4

    #Constructor
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.pendingTx = []
        self.miningReward = 1

    # Create first block without having a previous hash
    def createGenesisBlock(self):
        return Block([], "0" * 64)

    # Function to retrieve the latest mined block
    def getLatestBlock(self):
        return self.chain[(len(self.chain) - 1)]

    # Mining a new block to add to blockchain
    def minePendingTx(self, miningRewardAddress):

        rewardTx = Transaction("treasury", miningRewardAddress, self.miningReward)
        self.pendingTx.append(rewardTx)

        block = Block(self.pendingTx, self.getLatestBlock().hash)
        block.mine()

        self.chain.append(block)

        self.pendingTx = []

    # Create a tx and append it to the pending's array
    def createTx(self, transaction):
        self.pendingTx.append(transaction)

    # Iterate in every tx in every block to get balance
    def getBalance(self, address):

        if address == 'treasury':
            balance = 1000
        else:
            balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.receiverAddress == address:
                    balance += transaction.amount
                if transaction.senderAddress == address:
                    balance -= transaction.amount

        return balance

    # Check for difficulty compliance & hash concurrence
    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i - 1]
            _current = self.chain[i]

            if _current.hash != _current.calculateHash():
                return False

            if _current.previousHash != _previous.hash:
                return False

        return True