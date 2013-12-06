import serial
import time

def main():
    ser = serial.Serial('COM9', 9600, timeout = 0.5)
    #ser_write = lambda x: ser.write(str(x).zfill(SEND_PAYLOAD_LEN))
    ser_read = lambda x: ser.read(x)
    abcd = []
    while(True):        	
        x = ser_read(1)
        print x
        if x == '1' or x =='2' or x == '3' or x =='4' or x == '5' or x =='6'or  x == '7' or x =='8' or x == '9' or x =='0':
            print 'yo'
            if len(abcd) != 4:
                abcd.append(x) 		
            elif len(abcd) == 4:
                ser.write('@')
                for a in abcd:
					b = int(a)
				    ser.write(b)
					time.sleep(0.5)		
						
        print abcd
        #y = int(x)
        #print(y)
if __name__ == "__main__":
    main()		

