from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool

if __name__ == '__main__':
	sender = 'sender'
	receiver = 'receiver'
	amount = 1
	type = 'TRANSFER'

	transaction = Transaction(sender, receiver, amount, type)
	
	wallet = Wallet()
	fraudulentWallet = Wallet()
	pool = TransactionPool()

	transaction = wallet.createTransaction(receiver, amount, type)

	signatureValid = wallet.signatureValid(transaction.payload(), transaction.signature, wallet.publicKeyString())

	print(signatureValid)

	signatureValid = wallet.signatureValid(transaction.payload(), transaction.signature, fraudulentWallet.publicKeyString())
	print(signatureValid)

	if pool.transactionExists(transaction) == False:
		pool.addTransaction(transaction)

	if pool.transactionExists(transaction) == False:
		pool.addTransaction(transaction)

	print(pool.transactions)