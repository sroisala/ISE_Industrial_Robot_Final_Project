import socket
import time

class Gripper:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.socket.sendall(b'GET POS\n')
        recv_data = str(self.socket.recv(10), 'UTF-8')
        if recv_data:
            self.socket.send(b'SET ACT 1\n')
            print(str(self.socket.recv(10), 'UTF-8'))
            time.sleep(3)
            self.socket.send(b'SET GTO 1\n')
            self.socket.send(b'SET SPE 255\n')
            self.socket.send(b'SET FOR 255\n')
            print('Gripper Activated')

    def control(self, position):
        self.socket.send(f'SET POS {position}\n'.encode('utf-8'))
        print('Gripper Pos = ' + str(self.socket.recv(10), 'UTF-8'))
        self.socket.send(b'GET POS \n')
        print('Gripper Pos = ' + str(self.socket.recv(10), 'UTF-8'))

if __name__ == "__main__":
    gripper = Gripper()
