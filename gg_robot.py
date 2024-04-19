import socket
import time

class Robot:
    def __init__(self, ip, port):
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
        moveX, moveY, moveZ = x, y, z
        moveRx, moveRy, moveRz = rx, ry, rz
        cmd_move = f'movel(p[{moveX},{moveY},{moveZ},{moveRx},{moveRy},{moveRz}],0.5,0.5,0,0)\n'.encode('utf-8')
        self.socket.send(cmd_move)
        time.sleep(1)

    def home(self):
        print('Robot start moving')
        self.move(0.06583, -0.31616, 0.01625, 2.191, 2.238, 0)

if __name__ == "__main__":
    robot = Robot()
