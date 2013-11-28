import serial
import os
import time

def create_connection():
    if os.name == 'posix':
        PORT = "/dev/ttyUSB1"
    elif os.name == "nt":
        PORT = "COM10"
    return serial.Serial(PORT, 9600, timeout = 0.5)
	
	
def main():
	 print "here"
	 ser = create_connection()
	 print "connection"; 
	 
	 ser.write("@");
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write("#");
	 ser.write("a");
	 time.sleep(0.5);
	 ser.write("m");
	 time.sleep(0.5);
	 ser.write("b");
	 time.sleep(0.5);
	 ser.write("y");
	 time.sleep(0.5);
	 ser.write("$");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 ser.close();
	 
	 #second attempt
	 time.sleep(1);
	 ser = create_connection()
	 ser.write("@");
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write("#");
	 ser.write("d");
	 time.sleep(0.5);
	 ser.write("i");
	 time.sleep(0.5);
	 ser.write("b");
	 time.sleep(0.5);
	 ser.write("i");
	 time.sleep(0.5);
	 ser.write("$");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 time.sleep(0.5);
	 ser.write("9");
	 ser.close();
	 print "finished writing"
	 
	 
 
if __name__ == '__main__': main()	 
