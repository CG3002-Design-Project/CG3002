import serial

def create_connection():
    if os.name == 'posix':
        PORT = "/dev/ttyUSB1"
    elif os.name == "nt":
        PORT = "COM8"
    return serial.Serial(PORT, 9600, timeout = 0.5)
	
	
def main():
	 ser = create_connection()
	 ser.write("hello");