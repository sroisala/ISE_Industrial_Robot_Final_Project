#!/usr/bin/env python
# encoding: utf=8

""" 
#UR Controller Primary Client Interface Reader
# For software version 3.0
#
# Overview of client interface      : https://www.universal-robots.com/articles/ur/interface-communication/overview-of-client-interfaces/
# Datastream info found             : https://www.universal-robots.com/articles/ur/interface-communication/remote-control-via-tcpip/
# Script command for control robot  : https://s3-eu-west-1.amazonaws.com/ur-support-site/124999/scriptManual_3.15.4.pdf
"""

import socket, struct , time ,os , math , numpy
from gg_conv import Conveyor
import threading


v_x = 0
v_y = 0

robot_ip        = '10.10.0.14'       #UR3 .14  UR5 .26
robot_port      = 30003              ####RTDE
gripper_port    = 63352
vs_ip           = '10.10.1.10'
vs_port         = 2024

joint_speed = 0.1

def robot_connection() :

        global r
        
        ####Establish connection to controller
        r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r.connect((robot_ip, robot_port))
        r_recv = r.recv(1024)
        if r_recv :
                print('Connected to Robot RTDE....SUCCESSFULLY!')
                #print (r_recv)
        else :
                print('Connected to Robot RTDE...FAILED!')


def gripper_connection() :
   global g
   #Socket communication
   
   g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   g.connect((robot_ip, gripper_port))
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


def vs_connection():

        ####Establish connection to vision system
        global v
        v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        v.connect((vs_ip, vs_port))
        if v.connect :
                print ('Connected to Vision system ....SUCCESSFULLY!')
        v_data = ''


def grip_control(c):
        if c == 0 :
                g.send(b'SET POS 0\n')
        elif c == 255 :
                g.send(b'SET POS 255\n')
        g_recv = str(g.recv(10), 'UTF-8')
        g.send(b'GET POS \n')
        g_recv = str(g.recv(10), 'UTF-8')
        print ('Gripper Pos =    ' + g_recv)
 

def robot_home() :
        ##vs ref pos
        print('Robot start moveing')
        moveX  = 0.06583
        moveY  = -0.31616
        moveZ  = 0.01625
        moveRx = 2.191
        moveRy = 2.238
        moveRz = 0

        cmd_move = str.encode('movel(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        #r.send(b'movel(p[0.2,-0.35,0.1,2.253,-2.271,0],0.5,0.25,0,0)\n')
        print (cmd_move)
        r.send(cmd_move)
        time.sleep(1)

def gripper_move(x,y,rz, mode=0):
        
        global moveX, moveY, moveZ, moveRx, moveRy, moveRz

        #Home values
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
               moveZ = offsetZ

        cmd_move = str.encode('movel(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        r.send(cmd_move)
        time.sleep(1)
        return
 

def vs_recv():

        detect_status=0
        angle_status=0
        v_x = 0
        v_y = 0
        v_rz = 0
        
        v_data = ''
        v_coor = [0,0,0,0,0]
              
        
        while  v_coor == [0,0,0,0,0] :
                while v_data == '':
                        v.send (b'start!')
                        v_data = v.recv(64)
               
                coor_str = str(v_data, 'UTF-8')
                a = coor_str.split("[")
                b = a[1].split("]")
                coor_int = (b[0].split(","))
                detect_status=int(coor_int[0])
                angle_status=int(coor_int[1])
                if(detect_status==1):
                        v_x    = float(coor_int[3])
                        offset = float(coor_int[2])
                        v_y    = offset
                if(angle_status==1):
                        v_rz   = float(coor_int[4])

                v_coor = [detect_status,angle_status,v_x,v_y,v_rz]
                print ('v_coor  ======   ' + str(v_coor))
                v_data = ''

        return v_coor

def conveyor_task():
    conveyor = Conveyor()
    conveyor.conveyor_control()

def Initialize():
        robot_connection()
        gripper_connection()
        #conv_connection()
        vs_connection()
        #convey start
        robot_home()
        # Start conveyor as a thread
        conveyor_thread = threading.Thread(target=conveyor_task)
        conveyor_thread.start()

def activating():
        while True:
                v_x = 0
                v_y = 0
                v_rz = 0  
                status_detect=0
                status_angle=0 
                delay = 0.5  

                time.sleep(delay)
                print("Waiting for object detection")
                while(status_detect!=1 or status_angle!=1):
                 status_detect,status_angle,v_x, v_y, v_rz = vs_recv()  

                print(v_x, v_y, v_rz)

                gripper_move(x=v_x, y=v_y, rz=0, mode=0) # Move gripper to top of box
                time.sleep(delay)
                gripper_move(x=v_x, y=v_y, rz=0, mode=1) # Move gripper down
                time.sleep(delay)
                grip_control(255)
                time.sleep(delay)
                robot_home()
                time.sleep(delay)
                gripper_move(x=v_x, y=v_y, rz=0, mode=2)
                time.sleep(delay)
                grip_control(0)
                time.sleep(delay)
                robot_home()

              
def main():
        Initialize()
        activating()

        


if __name__ == '__main__':
    import sys
    main()

