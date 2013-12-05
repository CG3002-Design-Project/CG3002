import serial
import time
import requests
import json
NEW_TRANSACTION = '!'
CASHIER_ID = {"1111":"1234"}
shoppc = "127.0.0.1:8000/Inventory"


def parse(val,batchidlist,barcodelist,qtylist,pricelist,finallist):
    barcode = ''
    batch_id = ''
    qty = ''
    count = 1
    all = ''
    words = []
    for m in val:
        all += m
    		
    if not '*' in all:
        qty = str(1)
        if len(all) < 9:
            return -1
        else:
            for a in all:
                if count < 9:
                    barcode += a
                elif count > 8:
                    batch_id += a
                count += 1 			
    else:
        words = all.split('*')		
        qty = words[1]
        if len(words[0]) < 9:
            return -1        		
        for w in words[0]:
            if count < 9:
                barcode += w
    	    elif count > 8:
                batch_id += w
            count += 1 
    payload = { 'barcode': barcode, 'batchid': batch_id, 'qty': int(qty) }
    res = requests.get("http://127.0.0.1:8000/Inventory/getPrice",params=payload)	
    resd = json.loads(res.text)
    error = resd['error']
    if error < 0:
        return error
    else:
        barcodelist.append(barcode)
        batchidlist.append(batch_id)
        qtylist.append(qty)
        pricelist.append(resd['price'])
        finallist.append(int(qty) * float(resd['price']))
        print finallist
        return (str(float(resd['price']) * int(qty)))
		    
def checkCashierID(id):
    payload = { 'id' : id }
    res = requests.get("http://127.0.0.1:8000/Inventory/checkId",params=payload)
    data = json.loads(res.text)
    if data['error'] == 0:
        return True
    else:
        return False	
		
              		
def checkout(barcodelist,batchidlist,qtylist,finallist,cid):
    tot = 0.0
    for f in finallist:
        tot += f
    payload = {}
    list = []
    headers = {'content-type': 'application/json'}
    for a,b,c in zip(barcodelist,batchidlist,qtylist):
        list.append({'barcode':a, 'batchid':b, 'qty':c, 'cid':cid})        
    payload = {'product':list}
    data = json.dumps(payload)
    res = requests.post("http://127.0.0.1:8000/Inventory/deductInventory", data, headers = headers)  	
    return str(tot)	
 

def checkEmployeeId(id):
    return True
    
					
def main():
    ser = serial.Serial('COM20', 9600, timeout = 0)	
    val = []
    eid = ''
    cid = ''
    pid = ''
    paid = ''
    change = 0.0	
	#res = requests.post("http://127.0.0.1:8000/Inventory/write_to_display")   	
    while(True):      	
        a = ser.read(1)
        if a == '=':		
            while(True):
                b = ser.read()
                if b == None:
				    continue
                elif  b in ('1', '2', '3','4','5','6','7','8','9','0'):
                    eid += b
                elif b == '+':
                    break		
            if(checkEmployeeId(eid) == False):
                ser.write('?')
            else:
                ser.write('@')			
                while(True):
                    #res = requests.post("http://127.0.0.1:8000/Inventory/write_to_display")   
                    cid = ''
                    tot = ''
                    paid = ''
                    change = ''
                    beg = ser.read(1)	
                    if beg == None:
                        continue
                    if beg == '!':
                        while(True):
                            c = ser.read()
                            print c
                            time.sleep(1)
                            if c == None:
				                continue
                            if c in ('1', '2', '3','4','5','6','7','8','9','0'):
                                cid += c
                            elif c == '+':
                                break
                            else:
                                continue							
                        if (checkCashierID(cid) == False):
                            ser.write('?')
                        else:		                            
                            print cid
                            barcodelist = []
                            batchidlist = []
                            qtylist = []
                            pricelist = []
                            finallist = []
                            val = []							
                            while(True):
                                d = ser.read()						
                                if d in  ('1', '2', '3','4','5','6','7','8','9','0','*'):       #append product id, batchid , quantity to val
                                    val.append(d)								
                                elif d == '+' and val:                                          #pressing enter after keying in 1 product's info, receiving price for the product
                                    result = parse(val,batchidlist,barcodelist,qtylist,pricelist,finallist)				
                                    if result < 0:
                                        ser.write('e')   
                                  
                                        #time.sleep(3)
                                        #ser.write('`')										
                                    else:
                                        for r in result:
                                            ser.write(r)
                                        ser.write('h')
                                        time.sleep(5)						
                                        ser.write('&')
                                        val = []		
                                elif d == '+' and not val:
                                    ser.write('e')
                                elif d == ')' and val:
                                    val.pop()   
                                elif d == '(' and val:
                                    val = []
                                elif d == '^' and barcodelist and batchidlist and qtylist and pricelist and finallist:
                                    barcodelist = []
                                    batchidlist = []
                                    qtylist = []
                                    pricelist = []
                                    finallist = []
                                elif d == '$' and barcodelist and batchidlist and qtylist and pricelist and finallist:    #checkout, displaying total, calculating change 
                                    tot = checkout(barcodelist,batchidlist,qtylist,finallist,cid)
                                    print 'total = ' + tot
                                    for t in tot:
                                        ser.write(t)
                                    
                                    ser.write(';')	
                                    time.sleep(5) 									
                                    while(True):									
                                        pay = ser.read(1) 	
                                      
                                        if pay == 'p':
                                            break
                                        else:
                                            continue
                                    while(True):
                                        p = ser.read(1)
                                        print p
                                        time.sleep(1)
                                        if p in  ('1', '2', '3','4','5','6','7','8','9','0','.'):
                                            paid += p
                                        elif p == '+' and paid !='':
                                            break
                                        else:
                                            continue				
                                    change = float(paid) - float(tot)                     
					                #change = '2.30'                               
                                    print change
                                    if change < 0 :
                                        ser.write('e')
                                    else:
                                        for c in str(change):
                                            ser.write(c)
                                        ser.write(':')		
                                        time.sleep(5)										
                                    barcodelist = []
                                    batchidlist = []
                                    qtylist = []
                                    pricelist = []
                                    finallist = []									
                                    ser.write('`')
                                    break
								
		ser.close()			      
					# if(b == '`'):
						# for i in ser.read():
							# if i != '+':
								# paid += i
							# else: 
								# break								
						# if paid >= tot:
							# change = paid - tot
							# time.sleep(10)
							# ser.write('`')
						# else:
							# ser.write('r')                        						
					# barcodelist = []
					# batchidlist = []
					# qtylist = []
					# pricelist = []
					# finallist = []							
                    # elif a == '$' and (not barcodelist or not batchidlist or not qtylist or not pricelist or not finallist):
                        # ser.write('?')													
                    # elif a == '\)' and val:
		                # val.pop()
                          # #case for cancel, edit, del	                
                    # elif a == '^':
                        # val = []     #anything else needed for clear - how to start again
                    # elif a == '=':
                        # ser.write('?')
                    # elif a == '\)' and not val:
                        # ser.write('?')						

						
if __name__ == "__main__":
    main()  
	
	