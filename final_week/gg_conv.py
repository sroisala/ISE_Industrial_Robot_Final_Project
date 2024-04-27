####### Command for control conveyor #################
#### activate tcp        = activate,tcp
#### power on servo      = pwr_on,conv,0
#### power off servo     = pwr_off,conv,0
#### set velocity x mm/s = set_vel,conv,x   # x = 0 to 200
#### jog forward         = jog_fwd,conv,0
#### jog backward        = jog_bwd,conv,0
#### stop conveyor       = jog_stop,conv,0
#########################################################

import time
from socket import *

host    = '10.10.0.98'
port_conv = 2002

convey_speed=40
convey_duration=20


class Conveyor:
    def __init__(self) -> None:
        # nesseary parameters
        self.addr = (host, port_conv)
        self.speed = convey_speed
        self.duration = convey_duration

        self.convey_socket_connection()

    def convey_socket_connection(self):

        # Start a server to allow connection from conveyor
        self.c = socket(AF_INET, SOCK_STREAM)
        self.c.bind(self.addr)
        print ("socket binded to %s" %(self.addr[1]))
        
        # Listen 1 connection
        self.c.listen(1)
        print("Waiting for connection...")
        self.cong, self.client_addr = self.c.accept()

        print(f"Connected by {self.client_addr}")
        self.cong.sendall(b'activate,tcp,0.0\n')
        self.cong.sendall(b'pwr_on,conv,0\n')

    def conveyor_control(self):
        '''
        Control the conveyor with speed (mm/s) and duration (s)
        '''
        speed = self.speed
        duration = self.duration
        command_speed=f"set_vel,conv,{speed}".encode('utf-8')
        self.cong.sendall(command_speed)
        print(f"conveyor speed is {speed} mm/s")
        time.sleep(0.5)

        print(f"Moving conveyor forward for {duration} seconds")
        self.cong.send(b'jog_fwd,conv,0\n')
        time.sleep(duration)

        # Stop conveyor
        self.cong.send(b'jog_stop,conv,0\n')
        time.sleep(0.5)
        print(f"Conveyor response: {self.cong.recv(100)}")

    def terminate(self):
        self.cong.send(b'pwr_off,conv,0\n')
        self.cong.close()
        self.server_fd.close()
            

if __name__ == "__main__":
    conveyor = Conveyor()
    conveyor.conveyor_control()
