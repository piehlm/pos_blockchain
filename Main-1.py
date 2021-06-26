from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
import pprint

if __name__ == '__main__':
	sender = 'sender'
	receiver = 'receiver'
	amount = 1
	type = 'TRANSFER'

	wallet = Wallet()
	fraudulentWallet = Wallet()
	pool = TransactionPool()
	accountModel = AccountModel()

	transaction = wallet.createTransaction(receiver, amount, type)

	signatureValid = wallet.signatureValid(transaction.payload(), transaction.signature, wallet.publicKeyString())
	print('Real Wallet signature check: ', signatureValid)

	signatureValid = wallet.signatureValid(transaction.payload(), transaction.signature, fraudulentWallet.publicKeyString())
	print('Fake Wallet signature check: ', signatureValid)

	if pool.transactionExists(transaction) == False:
		pool.addTransaction(transaction)

	blockchain = Blockchain()
	# get the lastHash
	lastHash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
	blockCount = blockchain.blocks[-1].blockCount + 1

	block = wallet.createBlock(pool.transactions, lastHash, blockCount)
	signatureValid = Wallet.signatureValid(block.payload(), block.signature, wallet.publicKeyString())	
	print('Block signature check: ', signatureValid)

	if not blockchain.lastBlockHashValid(block):
		print('lastBlockHash is not valid')

	if not blockchain.blockCountValid(block):
		print('BlockCount is not valid')

	if blockchain.lastBlockHashValid(block) and blockchain.blockCountValid(block):
		blockchain.addBlock(block)
		pool.removeFromPool(block.transactions)
	
	accountModel.updateBalance(wallet.publicKeyString(), 10)
	accountModel.updateBalance(wallet.publicKeyString(), -5)
	print('Account Model Balance: ', accountModel.balances)

	alice = Wallet()
	bob = Wallet()
	exchange = Wallet()
	forger = Wallet()

	exchangeTransaction = exchange.createTransaction(alice.publicKeyString(), 10, 'EXCHANGE')
	if not pool.transactionExists(exchangeTransaction):
		pool.addTransaction(exchangeTransaction)

	coveredTransactions = blockchain.getCoveredTransactionSet(pool.transactions)
	lastHash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
	blockCount = blockchain.blocks[-1].blockCount + 1
	blockOne = forger.createBlock(coveredTransactions, lastHash, blockCount)
	blockchain.addBlock(blockOne)
	pool.removeFromPool(blockOne.transactions)

	''' Alice wants to send 5 tokens to bob '''
	transaction = alice.createTransaction(bob.publicKeyString(), 5, 'TRANSFER')

	if not pool.transactionExists(transaction):
		pool.addTransaction(transaction)

	coveredTransactions = blockchain.getCoveredTransactionSet(pool.transactions)
	lastHash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
	blockCount = blockchain.blocks[-1].blockCount + 1
	blockTwo = forger.createBlock(coveredTransactions, lastHash, blockCount)
	blockchain.addBlock(blockTwo)
	pool.removeFromPool(blockTwo.transactions)

	pprint.pprint(blockchain.toJson())

