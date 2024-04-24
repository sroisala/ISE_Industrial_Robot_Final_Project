import socket
import time

class Robot:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.socket = None
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        recv_data = self.socket.recv(1024)
        if recv_data:
            print('Connected to Robot RTDE....SUCCESSFULLY!')
        else:
            print('Connected to Robot RTDE...FAILED!')
    
    def move(self, x, y, z, rx, ry, rz, mode=0):
        #Home values
        moveX,moveY,moveZ,moveRx,moveRy,moveRz=Robot.gipper_global_location()

        #Camera offset
        cameraY=(y*0.79-20.54)/1000 #mm
        cameraX=(x*0.8936-85)/1000 #mm
        #11.6168

        #Offsets
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
               
        cmd_move = f'movel(p[{moveX},{moveY},{moveZ},{moveRx},{moveRy},{moveRz}],0.5,0.5,0,0)\n'.encode('utf-8')
        self.socket.send(cmd_move)
        time.sleep(1)

    def gipper_global_location():
        # My group
        # moveX  = 0.06583
        # moveY  = -0.31616
        # moveZ  = 0.01625
        # moveRx = 2.191
        # moveRy = 2.238
        # moveRz = 0

        # #Compare to son
        # moveX = 0.056
        # moveY = -0.331
        # moveZ = 0.05
        # moveRx = 2.233
        # moveRy = 2.257
        # moveRz = 0.039  

        #Compare to jom
        moveX=.046
        moveY=-.32
        moveZ=.065
        moveRx=2.2
        moveRy=2.24
        moveRz=0

        return moveX,moveY,moveZ,moveRx,moveRy,moveRz

    def home(self):
        print('Robot start moving')
        moveX,moveY,moveZ,moveRx,moveRy,moveRz=Robot.gipper_global_location()
        self.move(moveX, moveY,moveZ, moveRx, moveRy, moveRz)

if __name__ == "__main__":
    robot = Robot()
