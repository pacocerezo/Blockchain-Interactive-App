# INTERACTIVE BLOCKCHAIN

####

#### Description: Flask application that allows you to interact with a blockchain. You can see the blocks on chain, the transactions within them and create new ones and mine blocks. Built on top of a blockchain implementation in Python.

## Motivation:

I've been a bitcoin supporter for a long time. The idea of a digital decentralized reserve of value with transferable and secure attributes captivated me but I didn't fully understand how does it works under the hood.

With my recently gained computer science knowledge on the cs50x course I couldn't wait to code a blockchain and try to really understand some of the terminology I've been hearing about.

## Developing process:

#### Solidity:

I started diving too deep learning how to implement smart contracts with solidity. I wanted to assess the possibility of deploying my project on a testnet and interact with it as production projects do. After some research I decided the scope of this task was too big.

#### JavaScript:

I like javascript, I've learned it and it's widely use for smart contracts development so it seemed like the right choice. I wrote my initial blockchain but found some troubles when confronting the frontend part of the project. Facing the decision between learning Angular or React or transcript my blockchain to python and present it in Flask I choose the latter.

#### Python:

Changing my code from Javascript to Python helped me to solidify all the concepts about the blockchain and build some muscle memory for my coding skills.

#### SQLite:

I run into some troubles with sqlite implementation as I was creating too many tables and taking too many app outputs from the database. Everything started going smoother when I realized I should take the data directly from the blockchain. Finally there's only one table in the database, the one needed for registration and login.

#### CSS:

I adapted almost everything from bootstrap and made some styling changes mostly in the same HTML file.

#### Flask:

I took some elements from the trader app which helped me visualize the app quickly, from that scratch I kept the login_required function, the Jinja templates structure and some small details and made my responsive, duck themed, Harvard brand color app.

## Blockchain code:

The Blockchain is divided in three main classes: Transactions, Blocks and Blockchain.

#### Block:

Basic building piece of blockchains. Each block is a hashed piece of data constructed with the transactions included on it and the hash of the previous block, combining this two inputs its own hash is calculated

```python
def calculateHash(self):
        return updatehash(
            self.previousHash,
            self.transactions,
            self.nonce
        )

def updatehash(*args):
    hashing_text = ""; h = sha256()

    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

```

The nonce element comes from the proof of work mechanism which helps keeping a real blockchain secure. For a block to be added to the chain (mined), its hash has to begin with a number of zeros, what it's called difficulty. An important quantity of computational power has to be dedicated to solve this riddle by trying different nonce numbers until reaching the solution; this makes creating a new block somehow expensive which linked to the consensus mechanism where more than half of the blockchain nodes have to validate the new block makes the network secure.

```python
def mine(self):
        while True:
            if self.calculateHash()[:self.difficulty] == "0" * self.difficulty:
                self.hash = self.calculateHash(); break
            else:
                self.nonce += 1

```

#### Transaction:

This is a simple blockchain implementation where transactions are limited to a sender, a receiver and an amount. We are dealing with a small number of known addresses and a signing process with its keys as we would find in a real network deployed application have not been implemented.

```python
class Transaction():
    def __init__(self, senderAddress, receiverAddress, amount):
        self.senderAddress = senderAddress
        self.receiverAddress = receiverAddress
        self.amount = amount

    def calculateHash(self):
        return sha256(self.senderAddress + self.receiverAddress + self.amount)
```

#### Blockchain:

The blockchain is constructed with a genesis block, as no block can precede the first one it has to be created with a fixed hash and an empty transactions field.

```python
class Blockchain():
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.pendingTx = []
        self.miningReward = 1

    def createGenesisBlock(self):
        return Block([], "0" * 64)
```

From here there have been some functions created to help the chain achieve its purpose like create transactions, get the balance of an address to check for funds availability or a validating function to check for altered transactions details which will result in hash alteration:

```python
    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i - 1]
            _current = self.chain[i]

            if _current.hash != _current.calculateHash():
                return False

            if _current.previousHash != _previous.hash:
                return False
```

But the most important part of the blockchain is the function that takes all the pending transactions waiting to be included in the next block, mine it and append it to the existing chain.

```python
    def minePendingTx(self, miningRewardAddress):

        rewardTx = Transaction("treasury", miningRewardAddress, self.miningReward)
        self.pendingTx.append(rewardTx)

        block = Block(self.pendingTx, self.getLatestBlock().hash)
        block.mine()

        self.chain.append(block)

        self.pendingTx = []
```

As we can see it adds to the block a transaction to reward the miner who solved the proof of work riddle and finally erases the pending transactions list.

## Flask app:

Styling is simple. From the beginning I was focused on the backend coding as I started this project to learn about blockchain. In future works I'll focus on learning Angular or React to be able to present really great looking apps.

Ducks are cool and this is a duck themed app. I tried different approaches but this one I liked it since implementing it for the first time.

Brand color is Harvard's. Form shadows, buttons and details have been adapted. It's mixed with the duck's yellow we can see for example in the flashed messaged.

#### Index:

Nice looking minimalist first glance at the app with the protagonist ducky showing confidence and growth.

#### Registration:

A bootstrap login form with adapted styling accessible by both, the "Get started now" button and the "register" one. As no wallet extension is connected to a working network it is required as an input next to a username and a password.

All fields must be submitted, have a minimum length of four characters and passwords must match; being this one stored in a hashed format.

#### Login:

A bootstrap login form with adapted styling. Both fields must be submitted and any failure trying to log in a valid user will flash a "Invalid username and/or password" message.

#### Dashboard:

The main display of the app divided in three sections.

The blocks on chain division shows each mined block appended to the chain, if no extra block has been mined it will show just the genesis one with a previous hardcoded hash of only zeros and a resultant hash with no compliance with the difficulty as no previous or self transactions has been yet added.

Every subsequent mined block will be presented next to each other in a grid of bootstrap cards. To erase the blockchain and start with an empty one a "Restart blockchain" button is presented at the top of the page.

#### Buy:

Simple form to create a transaction from the blockchain treasury to the logged in user. As tx's are checked for funds availability, buying coins is the first step for a user to have some balance to transact. Amount must be a positive rounded integer.

#### Transactions:

Form to create a transaction from the logged in user to the desired addressee. Receiver must be a registered wallet to avoid the user from losing the funds. Amount must be a positive rounded integer and equal or lower than his balance.

#### Pending-tx:

No created transaction exist in the blockchain or alter it in anyway until they are included in a block. In this section we can see all the pending transactions waiting to be inserted in the next mining process and proceed with it.

## Final thoughts:

It's been challenge to finish this project and I've learn that in the coding world transforming ideas into working products will probably take more time and effort than one could think at the planning phase.

I guess this type of product is not the most useful from a curriculum perspective but I learned by doing something that I really liked and that's hugely rewarding. Although this is by no means a working secure blockchain it served my purpose of learning about how this technology works as well as developing my coding skills in different areas.

I'm glad with the process and the result and I hope you all like it.

## License

[MIT](https://choosealicense.com/licenses/mit/)
