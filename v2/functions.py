from time import sleep
import serial
from time import sleep

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)    #Open port with baud rate
ser.flushInput()

def sendCommand(sendtype, sendvalue):

    if sendtype == "PEEP":
        print("now sending..")
        ser.write(b"PEEP-"+bytes(sendvalue,'utf-8'))
        sleep(0.01)
        reading = ser.readline()
        print(reading)
        if reading != "PEEPOK-" + str(sendvalue):
            print("communication ERROR")
            return
    elif sendtype == "Freq":
        ser.write("FREQ-"+str(sendvalue))
        sleep(0.01)
        if ser.readLine() != "FREQOK-" + str(sendvalue):
            print("communication ERROR")
            return 0
    elif sendtype == "Tida":
        ser.write("TIDA-"+str(sendvalue))
        sleep(0.01)
        if ser.readLine() != "TIDAOK-" + str(sendvalue):
            print("communication ERROR")
            return 0
    elif sendtype == "Pres":
        ser.write("PRES-"+str(sendvalue))
        sleep(0.01)
        if ser.readLine() != "PRESOK-" + str(sendvalue):
            print("communication ERROR")
            return 0  
    else:
        print("send succesful")


