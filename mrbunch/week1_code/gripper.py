import socket
import time

#Host information
HOST = '10.10.0.14'
PORT = 30003

#server information
CAMERA= '10.10.1.10'
CAMERA_PORT= 2024

#Gripper information
GRIPPER_PORT = 63352

def gripper_connection() :
   global g
   #Socket communication
   g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   g.connect((HOST, GRIPPER_PORT))
   g.sendall(b'GET POS\n')
   g_recv = str(g.recv(10), 'UTF-8')
   if g_recv :
      g.send(b'SET ACT 1\n')
      g_recv = str(g.recv(10), 'UTF-8')
      print (g_recv)
      time.sleep(3)
      g.send(b'SET GTO 1\n')
      g.send(b'SET SPE 255\n')
      g.send(b'SET FOR 255\n')
      print ('Gripper Activated')

def grip_control(c):
        if c == 0 :
                g.send(b'SET POS 0\n')
        elif c == 255 :
                g.send(b'SET POS 255\n')

        time.sleep(1)
        g_recv = str(g.recv(10), 'UTF-8')
        g.send(b'GET POS \n')
        g_recv = str(g.recv(10), 'UTF-8')
        print ('Gripper Pos =    ' + g_recv)