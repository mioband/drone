from djitellopy import tello
import keyboard
import time

#Drone setting
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
vv=25

if __name__ == '__main__':
    print('start')
    drone.takeoff()
    while True:
        s = keyboard.hook()

        if s.name == 'esc':  # esc
            print('esc pressed')
            drone.land()
            break
        elif s.name == ord('w'):
            print('w')
            t = time.time()
            while True:
                drone.send_rc_control(0,vv,0,0)
                time.sleep(0.05)
                if time.time() - t > 0.5:
                    break
        elif s.name == ord('s'):
            print('s')
            t = time.time()
            while True:
                drone.send_rc_control(0,-vv,0,0)
                time.sleep(0.05)
                if time.time() - t > 0.5:
                    break
        elif s.name == ord('a'):
            print('a')
            t = time.time()
            while True:
                drone.send_rc_control(-vv,0,0,0)
                time.sleep(0.05)
                if time.time() - t > 0.5:
                    break
        elif s.name == ord('d'):
            print('d')
            t = time.time()
            while True:
                drone.send_rc_control(vv, 0, 0, 0)
                time.sleep(0.05)
                if time.time() - t > 0.5:
                    break
        elif s.name == ord('h'):
            print('h')
            t = time.time()
            while True:
                drone.send_rc_control(0, 0, vv, 0)
                time.sleep(0.05)
                if time.time() - t > 0.5:
                    break
        elif s.name == ord('l'):
            print('l')
            t = time.time()
            while True:
                drone.send_rc_control(0, 0, -vv, 0)
                time.sleep(0.05)
                if time.time() - t > 0.5:
                    break
        else:
            drone.send_rc_control(0, 0, 0, 0)