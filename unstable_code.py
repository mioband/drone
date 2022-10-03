# Code version 1.2: added second band and more drone controlls.
from djitellopy import tello
import serial
import keyboard

# Serial_Config
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM9'
ser.timeout = None
ser.open()

# Lists and parameters
packet_data = []
fly_ok = False

# Drone setting
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
minspeed = 11  # Minial speed (5-11)
minspeed_rp = 11
last_h = 0
last_vr = 0
last_vp = 0
last_yaw = 0


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
    return packet_data

def controll(packet_data, last_vr, last_vp, last_h, last_yaw):
    vr = last_vr
    vp = last_vp
    h = last_h
    yaw = last_yaw
    if packet_data[5] == 2:
        if packet_data[1] > 2 or packet_data[3] > 2:
            if packet_data[0] == 0:
                vnp = 1
            else:
                vnp = -1

            if packet_data[2] == 0:
                vnr = 1
            else:
                vnr = -1

            vsp = (minspeed_rp  * packet_data[1])
            vsr = (minspeed_rp  * packet_data[3])
            vp = vsp * vnp
            vr = vsr * vnr
            # print(vp, vr)
        else:
            vr = 0
            vp = 0
        last_vr = vr
        last_vp = vp

    if packet_data[5] == 3:

        if packet_data[1] > 4 or packet_data[3] > 4:
            if packet_data[0] == 0:
                vh = -1
            else:
                vh = 1

            if packet_data[2] == 0:
                yawv = 1
            else:
                yawv = -1

            h = (minspeed * packet_data[1]) * vh
            yaw = (minspeed * packet_data[3]) * yawv
        else:
            h = 0
            yaw = 0
        last_h = h
        last_yaw = yaw

    drone.send_rc_control(vr, vp, h, yaw)
    return last_vr, last_vp, last_h, last_yaw


while ser.isOpen() == True:
    if keyboard.is_pressed("esc"):
        drone.land()
        break
    if keyboard.is_pressed("enter"):
        drone.takeoff()
        fly_ok =True
        print("UP")
    if keyboard.is_pressed("right shift"):
        drone.land()
        fly_ok=False
        print("DOWN")

    packet_data = getdata()
    if fly_ok:
        last_vr, last_vp, last_h, last_yaw = controll(packet_data, last_vr, last_vp, last_h, last_yaw)
    packet_data.clear()

drone.land()
