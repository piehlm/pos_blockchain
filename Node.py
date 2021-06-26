from Blockchain import Blockchain
from TransactionPool import TransactionPool
from Wallet import Wallet

class Node():

	def __init__(self):
		self.blockchain = Blockchain()
		self.transactionPool = TransactionPool()
		self.wallet = Wallet()