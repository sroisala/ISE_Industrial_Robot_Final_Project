import time
import socket
import threading
from gg_robot import Robot
from gg_gripper import Gripper
from gg_conv import Conveyor

robot = Robot('10.10.0.14', 30003)
gripper = Gripper('10.10.0.14', 63352)

def vs_connection():
    global v
    ### Establish connection to vision system
    vs_ip = '10.10.1.10'
    vs_port = 2024
    v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    v.connect((vs_ip, vs_port))
    if v.connect:
        print('Connected to Vision system....SUCCESSFULLY!')

def vs_recv():
    detect_status = 0
    angle_status = 0
    v_x = 0
    v_y = 0
    v_rz = 0
    v_data = ''
    v_coor = [0, 0, 0, 0, 0]

    while v_coor == [0, 0, 0, 0, 0]:
        print("Waiting for vision system data...")
        while v_data == '':
            v.send(b'start!')
            v_data = v.recv(1024)

        coor_str = str(v_data, 'UTF-8')
        a = coor_str.split("[")
        b = a[1].split("]")
        coor_int = b[0].split(",")
        detect_status = int(coor_int[5])
        angle_status = int(coor_int[1])

        if detect_status == 1:
            v_x = float(coor_int[3])
            offset = float(coor_int[2])
            v_y = offset
        if angle_status == 1:
            v_rz = float(coor_int[4])

        v_coor = [detect_status, angle_status, v_x, v_y, v_rz]
        print('Vision coordinates:' + str(v_coor))
        v_data = ''

    return v_coor

def conveyor_task():
    conveyor = Conveyor()
    conveyor.conveyor_control()

def Initialize():
    robot.connection()
    gripper.connection()
    # conveyor.convey_socket_connection()
    vs_connection()
    # conveyor start
    robot.home()
    # Start conveyor as a thread
    print('Hi')
    conveyor_thread = threading.Thread(target=conveyor_task)

    conveyor_thread.start()
    print("hi2")        
    gripper.control(0)

def activating():
    while True:
        v_x = 0
        v_y = 0
        v_rz = 0
        status_detect = 0
        status_angle = 0
        delay = 0.2

        time.sleep(delay)
        print("Waiting for object detection")
        while (status_detect!=1):
            status_detect,status_angle,v_x, v_y, v_rz = vs_recv() 

        print(v_x, v_y, v_rz)
        
        # robot.move(x=v_x, y=v_y, rz=0, mode=0) # Move gripper to top of box
        robot.move(x=v_x, y=v_y, rz=0, mode=1) # Move gripper down
        gripper.control(255)
        # time.sleep(delay)
        time.sleep(delay)
        robot.move(x=v_x, y=v_y, rz=0, mode=2) # Move gripper upward
        # time.sleep(delay)
        # gripper.control(0)
        # time.sleep(0.3)
        # robot.home()

        for i in range(7):
            status_detect,status_angle,v_x, v_y, v_rz = vs_recv()     

def main():
    Initialize()
    activating()

if __name__ == '__main__':
    import sys
    main()
