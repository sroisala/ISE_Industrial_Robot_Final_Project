import time
import socket
import threading
from gg_robot import Robot
from gg_gripper import Gripper
from gg_conv import Conveyor

class Main:
    def __init__(self):
        self.robot = Robot('10.10.0.14', 30003)
        self.gripper = Gripper('10.10.0.14', 63352)
        self.conveyor = Conveyor()
        self.v = None

    def vs_connection(self):
        ### Establish connection to vision system
        vs_ip = '10.10.1.10'
        vs_port = 2024
        self.v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.v.connect((vs_ip, vs_port))
        if self.v.connect:
            print('Connected to Vision system....SUCCESSFULLY!')

    def vs_recv(self):
        detect_status = 0
        angle_status = 0
        v_x = 0
        v_y = 0
        v_rz = 0
        v_data = ''
        v_coor = [0, 0, 0, 0, 0]

        while v_coor == [0, 0, 0, 0, 0]:
            print("Waiting for vision system data...")
            while not v_data:
                self.v.send(b'start!')
                v_data = self.v.recv(256)

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

    def conveyor_task(self):
        self.conveyor = Conveyor()
        self.conveyor.conveyor_control()
    
    def Initialize(self):
        self.robot.connection()
        self.gripper.connection()
        # self.conveyor.convey_socket_connection()
        self.vs_connection()
        # conveyor start
        self.robot.home()
        # Start conveyor as a thread
        conveyor_thread = threading.Thread(target=self.conveyor_task)
        conveyor_thread.start()
        self.gripper.control(0)

    def activating(self):
        while True:
            v_x = 0
            v_y = 0
            v_rz = 0
            status_detect = 0
            status_angle = 0
            delay = 0.3

            time.sleep(delay)
            print("Waiting for object detection")
            while (status_detect!=1 or status_angle!=1):
                 status_detect,status_angle,v_x, v_y, v_rz = self.vs_recv() 

            print(v_x, v_y, v_rz)
            
            self.robot.move(x=v_x, y=v_y, rz=0, mode=0) # Move gripper to top of box
            time.sleep(delay)
            self.robot.move(x=v_x, y=v_y, rz=0, mode=1) # Move gripper down
            time.sleep(delay)
            self.gripper.control(255)
            # time.sleep(delay)
            # self.robot.home()
            time.sleep(delay)
            self.robot.move(x=v_x, y=v_y, rz=0, mode=2) # Lift
            # time.sleep(delay)
            # self.gripper.control(0)
            # time.sleep(0.3)
            # self.robot.home()

            status_detect,status_angle,v_x, v_y, v_rz = self.vs_recv()     

def main():
    controller = Main()
    controller.Initialize()
    controller.activating()

if __name__ == '__main__':
    import sys
    main()
