import socket
import time

class Robot:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.r = None
    
    def connection(self):
        #### Establish connection to controller
        self.r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r.connect((self.ip, self.port))
        recv_data = self.r.recv(1024)
        if recv_data:
            print('Connected to Robot RTDE....SUCCESSFULLY!')
        else:
            print('Connected to Robot RTDE...FAILED!')
    
    def move(self, x, y, rz, mode=0):
        moveX  = 0.06583
        moveY  = -0.31616
        moveZ  = 0.01625
        moveRx = 2.191
        moveRy = 2.238
        moveRz = 0

        #Camera offset
        cameraY=(y*0.79-20.54)/1000 #mm
        cameraX=(x*0.8936-11.6168)/1000 #mm

        #Robot offsets
        offsetZ= - 0.250
        offsetX= 0.250
        if mode == 0:
               moveZ = offsetZ+0.066
               moveX = offsetX+cameraX
               moveY+=cameraY
        elif mode == 1:
               moveZ = offsetZ
               moveX = offsetX+cameraX
               moveY+=cameraY
        elif mode == 2:
               moveZ = 0.01625

        cmd_move = str.encode('movel(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        self.r.send(cmd_move)
        time.sleep(1)

    def home(self):
        print('Robot start moving')
        moveX  = 0.06583
        moveY  = -0.31616
        moveZ  = 0.01625
        moveRx = 2.191
        moveRy = 2.238
        moveRz = 0

        cmd_move = str.encode('movel(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')

        print(cmd_move)
        self.r.send(cmd_move)
        time.sleep(1)

if __name__ == "__main__":
    robot = Robot()
