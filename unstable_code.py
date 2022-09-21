# Code version 1.2: added second band and more drone controlls.
from djitellopy import tello
import serial
import keyboard

#Serial_Config
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM9'
ser.timeout = None
ser.open()

#Lists and parameters
static_data_pr = []
static_data_yh = []
packet_data = []
k = 0
vp,vr,vh,yaw = 0

#Drone setting
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
minspeed = 11 # Minial speed (5-11)

def controll():
    # Band 1 - Pith/Roll, speed: 20 - 99 cm/sec
    if static_data_pr[k][1] > 2 or static_data_pr[k][3] > 2:
        if static_data_pr[k][0] == 0:
            vnp=1
        else:
            vnp=-1

        if static_data_pr[k][2] == 0:
            vnr = 1
        else:
            vnr = -1

        vsp = (minspeed*static_data_pr[k][1])
        vsr = (minspeed*static_data_pr[k][3])
        vp=vsp*vnp
        vr=vsr*vnr
        #print(vp, vr)
    else:
        vr = 0
        vp = 0

    #Band 2 - Up/Down, Yaw 0 - 360
    if static_data_yh[k][1] > 2 or static_data_yh[k][3] > 2:
        if static_data_yh[k][0] == 0:
            vh = 1
        else:
            vh = -1

        if static_data_yh[k][2] == 0:
            yawv = 1
        else:
            yawv = -1

        h = (minspeed*static_data_pr[k][1]) * vh
        yaw = (minspeed*static_data_pr[k][3]) * yawv
        vp=vsp*vnp
    else:
        h = 0
        yaw = 0

    drone.send_rc_control(vr, vp, h, yaw)

def getdata():
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
        print(static_data_pr[k])
    else:
        static_data_yh.append(packet_data)
        print(static_data_yh[k])

while ser.isOpen() == True:
    if keyboard.is_pressed("esc"):
        drone.land()
        break
    if keyboard.is_pressed("enter"):
        drone.takeoff()
        print("UP")
    if keyboard.is_pressed("right shift"):
        drone.land()
        print("DOWN")

    getdata()
    controll()

    packet_data.clear()
    k=k+1

drone.land()

