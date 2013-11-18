import re
import time
from Inventory.models import Inventory, Product
from Transaction.models import Transaction
import datetime

def addToTables():
	print "inside function"
	transaction = []
	transactionList = []
	with open("transaction_temp.txt") as f:
		for line in f:
			transaction = re.split(":",line)
			t = []
			for i in range(len(transaction)):
				t.append(transaction[i].strip('\n').split(",")[0])
			transactionList.append(t)
	
	print transactionList[0]
	for word in transactionList:
		tdate = datetime.datetime.strptime(word[5], '%d/%m/%Y').date()	
		t = Transaction(transaction_id = int(word[0]), batch_id = 00000000, selling_price = 0, quantity_sold = int(word[4]),product_id = int(word[0]),transaction_date = tdate)
		t.save()	

def inventoryf():			
	inventory = []
	inventoryList = []
	with open("test.txt") as f:
		for line in f:
			inventory = re.split(":",line)
			t = []
			for i in range(8):
				t.append(inventory[i].strip('\n').split(",")[0])
			inventoryList.append(t)
		
	for word in inventoryList:
		inObj = Inventory(minimum_qty = int(word[6]),name = word[0], qty = int(word[5]), manufacturer = word[2], batch_id = 00000000,cost_price = float(word[4]),selling_price = 0000000, product_id = int(word[3]), category = word[1]) 
		inObj.save()
		
		#peri = Perishables(product_batch_id = inObj.id, expiry_date = datetime.date.today())
		#peri.save()
	

def main():
	print "here"
	addToTables()
	inventoryf()	


if __name__ == '__main__':
	main()   
