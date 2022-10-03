# Code version 1.1: only getData
import serial
import keyboard
import time

# Serial_Config
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM9'
ser.timeout = None
ser.open()

# Lists and parameters
static_data_pr = []
static_data_yh = []
packet_data = []
k = 0

def getdata():
    d1 = d2 = 0
    while True:
        symbol = ser.read()
        if symbol == b'\n':
            while len(packet_data) != 6:
                symbol = ser.read()
                # print (symbol)
                try:
                    packet_data.append(int(symbol))
                except:
                    pass
            break

    if packet_data[5] == 2:
        static_data_pr.append(packet_data)
        d1 = static_data_pr[k]
        #print(id(static_data_pr[c_pr]))
        #print(static_data_pr[c_pr])
        #print(len(static_data_pr))

    if packet_data[5] == 3:
        static_data_yh.append(packet_data)
        d2 = static_data_yh[k]
        #print(len(static_data_yh))
        #print(id(static_data_yh[c_yh]))
    print(d1, d2, k, sep="--", end="\n")
    #time.sleep(0.5)

while ser.isOpen() == True:
    getdata()
    packet_data.clear()
