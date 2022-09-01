from djitellopy import tello
import serial,time
import keyboard

#Serial_Config
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM9'
ser.timeout = None
#print(ser)
ser.open()

# Lists and parametrs
datalist = []
datad = []
k = 0

#Drone setting
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
#drone.takeoff()
minspeed = 10
start = False


def print_pressed_keys(e):
    print(e.name)
    if e.name == 'esc':
        drone.land()
        print('LANDING')
        return True
    if e.name == 'enter':
        drone.takeoff()

        print('TAKEOFF')
        return True

while ser.isOpen() == True:
    s = keyboard.hook(print_pressed_keys)

    while True:
        symbol = ser.read()
        if symbol == b'\n':
            while len(datad) != 6:
                symbol = ser.read()
                # print (symbol)
                try:
                    datad.append(int(symbol))
                except:
                    pass


            break

    datalist.append(datad)
    print(datalist[k])
    if datalist[k][1] > 2 or datalist[k][3] > 2:
        if datalist[k][0] == 0:
            vnp=1
        else:
            vnp=-1
        if datalist[k][2] == 0:
            vnr = 1
        else:
            vnr = -1

        #vnp = datalist[k][0]
        vsp = (minspeed*datalist[k][1])
        #vnr = datalist[k][2]
        vsr = (minspeed*datalist[k][3])
        vp=vsp*vnp
        vr=vsr*vnr
        #print(vp, vr)
    else:
        vr = 0
        vp = 0
    drone.send_rc_control(vr, vp, 0, 0)
    datad.clear()
    k=k+1



