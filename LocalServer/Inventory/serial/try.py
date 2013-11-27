import serial
import os
import time

def create_connection():
    if os.name == 'posix':
        PORT = "/dev/ttyUSB1"
    elif os.name == "nt":
        PORT = "COM8"
    return serial.Serial(PORT, 9600, timeout = 0.5)
	
	
def main():
	 print "here"
	 ser = create_connection()
	 print "connection"; 
	 ser.write("#");
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write(1);
	 time.sleep(0.5);
	 ser.write("*");
	 ser.write("p");
	 time.sleep(0.5);
	 ser.write("O");
	 time.sleep(0.5);
	 ser.write("O");
	 time.sleep(0.5);
	 ser.write("r");
	 time.sleep(0.5);
	 ser.write("n");
	 time.sleep(0.5);
	 ser.write("i");
	 time.sleep(0.5);
	 ser.write("m");
	 time.sleep(0.5);
	 ser.write(":");
	 time.sleep(0.5);
	 ser.write("a");
	 time.sleep(0.5);
	 ser.write("m");
	 time.sleep(0.5);
	 ser.write("b");
	 time.sleep(0.5);
	 ser.write("y");
	 print "finished writing"
	 ser.close();
	 
 
if __name__ == '__main__': main()	 
