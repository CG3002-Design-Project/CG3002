import serial
import time
import requests
import json
NEW_TRANSACTION = '!'
CASHIER_ID = {"1111":"1234"}
shoppc = "127.0.0.1:8000/Inventory"


def write_to_ui():
	 payload = {
	 'batchid':1234,
	 'barcode':12289374,
	 'qty':100,
	 'price':100.11
	 }
	 data = json.dumps(payload)
	 headers = {'content-type': 'application/json'}
	 res = requests.post("http://127.0.0.1:8000/Inventory/transaction/add_cachier_transaction", data, headers = headers)

def main():
	write_to_ui()
	 
	 
if __name__ == "__main__":
    main()  
		 