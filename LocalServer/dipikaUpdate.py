

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","local.settings")

import sys
import re
import time
from Inventory.models import Product,Inventory,Transaction
import datetime
from decimal import *


def addToTables():
    print "inside function"
    transaction = []
    transactionList = []
    storeid = 00000001
    with open("Trans_50_2_9_1762.txt") as f:
        for line in f:
            transaction = re.split(":",line)
            t = []
            for i in range(len(transaction)):
                t.append(transaction[i].strip('\n').split(",")[0])
            transactionList.append(t)
    print transactionList[0]
    counter = 0;
    for word in transactionList:
        tdate = datetime.datetime.strptime(word[5], '%d/%m/%Y').date()	
        inventory  = Inventory.objects.get(product_id_id = int(word[3]),batch_id=00000001)
        inventory.qty = inventory.qty - int(word[4])
        inventory.save()
        print counter;
        counter+=1;
        if (tdate == datetime.date(2013,9,30)):
            t = Transaction(transaction_id = int(word[0]), batch_id = 00000001, quantity_sold = int(word[4]),product_id = int(word[3]),transaction_date = tdate,cashier_id=int(word[1]),selling_price = inventory.selling_price, cost_price = inventory.cost_price)
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
        p = Product(name = (word[0]),manufacturer = (word[2]),product_id = int(word[3]),min_restock = 0.1*int(word[5]),category = word[1],status = 'false')
        p.save()

        if(counter%50 == 0):			
			inObj1 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00001,cost_price = Decimal(word[4]),selling_price = Decimal(1.05)*Decimal(word[4]) ,product_id_id = int(word[3]),expiry_date=datetime.date(2013,12,15),strategy_percentage=0)
			inObj2 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00002,cost_price = Decimal(1.1)*Decimal(word[4]),selling_price = Decimal(1.15)*Decimal(word[4]) ,product_id_id = int(word[3]),expiry_date=datetime.date(2013,12,16),strategy_percentage=0)
        else:
			inObj1 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00001,cost_price = Decimal(word[4]),selling_price = Decimal(1.05)*Decimal(word[4]) ,product_id_id = int(word[3]),strategy_percentage=0)
			inObj2 = Inventory(minimum_qty = int(word[6]), qty = int(word[5]),batch_id = 00002,cost_price = Decimal(1.1)*Decimal(word[4]),selling_price = Decimal(1.15)*Decimal(word[4]) ,product_id_id = int(word[3]),strategy_percentage=0)
        inObj1.save()
        inObj2.save()
        counter = counter + 1
		
def main(): 
   addToTables()	
	


if __name__ == '__main__':
	main()   

	

