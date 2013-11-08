
from django.core.management import setup_environ

from HQProject import settings

setup_environ(settings)


import re
import time
from Product.models import Product,Batch
from Transactions.models import Transactions
from Store.models import Store
import datetime



def addToTables():
	print "inside function"
	transaction = []
	transactionList = []
	with open("Trans_50_2_9_22639.txt") as f:
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
	with open("Inventory_5000.txt") as f:
		for line in f:
			inventory = re.split(":",line)
			t = []
			for i in range(len(inventory)):
				t.append(inventory[i].strip('\n').split(",")[0])
			inventoryList.append(t)
		
	for word in inventoryList:
            p = Product(name = word[0],manufacturer = word[2],product_id = int(word[3]),category = word[1])
	    p.save()     
            inObj = Batch(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00000000,selling_price = 0,product_id_id=int(word[3]),store_id_id=1)
            inObj.save()
		
		#peri = Perishables(product_batch_id = inObj.id, expiry_date = datetime.date.today())
		#peri.save()
	

def main():
	print "here"
	#addToTables() 
	inventoryf()	


if __name__ == '__main__':
	main()   
