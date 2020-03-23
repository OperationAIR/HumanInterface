from time import sleep
import serial
from time import sleep
from settings import Settings

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)    #Open port with baud rate
ser.flushInput()

def sendCommand(sendtype, settings):

    bit_repr = settings.get_bit_string()
    ser.write(bit_repr)
    reading = ser.readline()
    print(reading)
