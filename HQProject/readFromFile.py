

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","HQProject.settings")

import sys
import re
import time
from Website.models import Product,Store,Inventory,Transaction
import datetime
from decimal import *


def addToTables():
    print "inside function"
    transaction = []
    transactionList = []
    storeid = 00000005
    with open("Trans_50_2_9_1762.txt") as f:
        for line in f:
            transaction = re.split(":",line)
            t = []
            for i in range(len(transaction)):
                t.append(transaction[i].strip('\n').split(",")[0])
            transactionList.append(t)
    print transactionList[0]
    for word in transactionList:
        tdate = datetime.datetime.strptime(word[5], '%d/%m/%Y').date()	
        if not(tdate == datetime.date(2013,9,30)):
            inventory  = Inventory.objects.get(product_id_id = int(word[3]),batch_id=00000001,store_id_id=storeid)
            inventory.qty = inventory.qty - int(word[4])
            inventory.save()
            t = Transaction(transaction_id = int(word[0]), batch_id = 00000001, quantity_sold = int(word[4]),product_id = int(word[3]),transaction_date = tdate,cashier_id=int(word[1]),selling_price = inventory.selling_price, cost_price = inventory.cost_price,store_id=storeid)
            t.save()
            			

def invenf():			
    inventory = []
    inventoryList = []
    with open("Inventory_100.txt") as f:
        for line in f:
            inventory = re.split(":",line)
            t = []
            for i in range(len(inventory)):
                t.append(inventory[i].strip('\n').split(",")[0])
            inventoryList.append(t)
    counter = 0			
    for word in inventoryList:
        p = Product(name = (word[0]),manufacturer = (word[2]),product_id = int(word[3]),category = word[1],min_restock = 0.1*int(word[5]))
        p.save()
        a = 1
        while (a<=5):
            if(counter%50 == 0):
                			
                inObj1 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00001,cost_price = Decimal(word[4]),selling_price = Decimal(str(1.05))*Decimal(word[4]) ,product_id_id = int(word[3]),store_id_id=a,expiry_date=datetime.date(2013,12,15))
                inObj2 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00002,cost_price = Decimal(str(1.1))*Decimal(word[4]),selling_price = Decimal(str(1.15))*Decimal(word[4]) ,product_id_id = int(word[3]),store_id_id=a,expiry_date=datetime.date(2013,12,16))
            else:
                inObj1 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00001,cost_price = Decimal(word[4]),selling_price = Decimal(str(1.05))*Decimal(word[4]) ,product_id_id = int(word[3]),store_id_id=a)
                inObj2 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00002,cost_price = Decimal(str(1.1))*Decimal(word[4]),selling_price = Decimal(str(1.15))*Decimal(word[4]) ,product_id_id = int(word[3]),store_id_id=a)
            inObj1.save()
            inObj2.save()
            a = a + 1
        counter = counter + 1
		
		
		#peri = Perishables(product_batch_id = inObj.id, expiry_date = datetime.date.today())
		#peri.save()
	

def main():
    invenf() 
    #addToTables()
	


if __name__ == '__main__':
	main()   

	

