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
        # g.send(b'SET POS 255\n')
        # time.sleep(1)
        # g.send(b'SET POS 0\n')
        # time.sleep(1)
        # g.send(b'SET POS 255\n')
        # time.sleep(1)
        g_recv = str(g.recv(10), 'UTF-8')
        g.send(b'GET POS \n')
        g_recv = str(g.recv(10), 'UTF-8')
        print ('Gripper Pos =    ' + g_recv)

        

        
def robot_moveTCPmode(x,y,rz) :

        global moveX, moveY, moveZ, moveRx, moveRy, moveRz
        print('Robot start moveing')

        moveX  = x /100 
        moveY  = y /100
        moveZ  = 0 
        moveRx = 0 
        moveRy = 0 
        #moveRz = rz / 1000
        moveRz = 0
        
        cmd_move = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        print (cmd_move)
        print (type(cmd_move))
        r.send(cmd_move)
        time.sleep(1)
 

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

def robot_moveTCPmode(x,y,rz, mode=0) :

        global moveX, moveY, moveZ, moveRx, moveRy, moveRz
        print('Robot starts moving')

        moveX  = x /100 + 0.056
        moveY  = - 0.331 # y /100 - 0.331
        if mode == 0:
            moveZ  = 0 + 0.12
        elif mode == 1:
            moveZ = - 0.23 + 0.12 # -0.235
        elif mode == 2:
            moveZ = - 0.1 + 0.12
        moveRx = 0 + 2.233
        moveRy = 0 + 2.257
        #moveRz = rz / 1000
        moveRz = 0 - 0.039
       
        cmd_move = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        #cmd_move = str.encode('movel(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        print (cmd_move)
        print (type(cmd_move))
        r.send(cmd_move)
        time.sleep(1)

def gripper_move(x,y,rz, mode=0):
        
        global moveX, moveY, moveZ, moveRx, moveRy, moveRz

        moveX  = 0.06583
        moveY  = -0.31616
        moveZ  = 0.01625
        moveRx = 2.191
        moveRy = 2.238
        moveRz = 0


        # moveX  = x /1000 + 0.06583
        # moveY  = - 0.31616 # y /100 - 0.331

        # if mode == 0:
        #         moveZ  = 0 + 0.12
        # elif mode == 1:
        #         moveZ = - 0.23 + 0.12 # -0.235
        # elif mode == 2:
        #         moveZ = - 0.1 + 0.12
        # moveRx = 0 + 2.233
        # moveRy = 0 + 2.257
        # #moveRz = rz / 1000
        # # moveRz = 0 - 0.039
        if mode == 0:
               moveZ = (- 0.187)
               moveX = 0.253
        elif mode == 1:
               moveZ = (- 0.250)
               moveX = 0.253
        elif mode == 2:
               moveZ = (- 0.250)

        cmd_move = str.encode('movel(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        print (cmd_move)
        print (type(cmd_move))
        r.send(cmd_move)
        time.sleep(1)
        return
 

def vs_recv():

        v_x = 0
        v_y = 0
        v_rz = 0
        
        v_data = ''
        v_coor = [0,0,0]
              
        
        while  v_coor == [0,0,0] :
                while v_data == '':
                        
                        print ('send start to cvs')
                        v.send (b'start!')
                        v_data = v.recv(20)
               
                coor_str = str(v_data, 'UTF-8')
                print ('str v_data =   ' + coor_str)
                a = coor_str.split("[")
                b = a[1].split("]")
                coor_int = (b[0].split(","))
                print(coor_int)
                status= int(coor_int[0])
                v_x    = float(coor_int[1])
                offset = float(coor_int[2])
                v_y    = offset
                v_rz   = float(coor_int[3])

                print ('v_x =  ' + str(v_x))
                print ('v_y =  ' + str(v_y))
                print ('v_rz =  ' + str(v_rz))

                v_coor = [status,v_x,v_y,v_rz]
                print ('v_coor  ======   ' + str(v_coor))
                # if math.isnan(v_coor[0]) or math.isnan(v_coor[1]) :
                #         print ('v_coor == nan')
                #         v_data = ''
                #         v_coor = [0,0,0]

        return v_coor
              
def main():
        robot_connection()
        gripper_connection()
        #conv_connection()
        vs_connection()
        grip_control(0)
        #convey()
        v_x = 0
        v_y = 0
        v_rz = 0   
        delay = 0.5  

        robot_home()
        time.sleep(delay)
        #status,v_x, v_y, v_rz = vs_recv() # cm, cm, deg     

        #print(v_x, v_y, v_rz)

        # gripper_move(x=v_x, y=v_y, rz=0, mode=0) # Move gripper to top of box
        # time.sleep(delay)
        # gripper_move(x=v_x, y=v_y, rz=0, mode=1) # Move gripper down
        # time.sleep(delay)
        # grip_control(255)
        # time.sleep(delay)
        # robot_home()
        # time.sleep(delay)
        # gripper_move(x=v_x, y=v_y, rz=0, mode=2)
        # time.sleep(delay)
        # grip_control(0)
        # time.sleep(delay)
        # robot_home()
        # time.sleep(delay)
        # gripper_move(x=v_x, y=v_y, rz=0, mode=1) # Move gripper down
        # time.sleep(delay)
        # grip_control(0)
        # time.sleep(delay)
        # robot_home()



        #r.send(b'movel(p[-0.1176,-0.2903,0.00,3.141,-0.037,0],0.5,0.5,0,0)\n')
        # while 0 :
                
        #         xx = input('x =>   ' )
        #         if xx == '1' :
                        
        #                 xint = float(xx)
        #                 cmd = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+str(xint)+',0,0,0,0,0]),1,0.25,0,0)\n')
        #                 #cmd_move = str.encode(cmd)
        #                 r.send(cmd)

        #         elif xx == '2' :
        #                 cnt_pick = 0
        #                 while 1 :
        #                         r_offset = vs_recv()
        #                         print ('r_offset  =  ' + str(r_offset))
                                
        #                         if  1:
        #                                 print ('robot moving')
        #                                 x_m = -r_offset[1]/10000
        #                                 offset = r_offset[0]/10000
        #                                 y_m    = -offset
        #                                 z_rad = '{:0.2f}'.format(r_offset[2]*0.01745)
        #                                 #cmd = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+ str(x_m) +','+ str(y_m)+',0,0,0,'+str(z_rad)+']),1,0.5,0,0)\n')
        #                                 cmd = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+ str(x_m) +','+ str(y_m)+',0,0,0,0]),1,0.8,0,0)\n')
        #                                 print (str(cmd))
        #                                 r.send(cmd)

        #                         if x_m < 0.003 and x_m > -0.003 and y_m <0.003 and y_m > -0.003  :
        #                                 cnt_pick += 1
        #                         else :
        #                                 cnt_pick = 0
        #                         if cnt_pick == 5 :
        #                                 print ('robot start picking')
                                        
        #                                 cmd = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+ str(x_m) +','+ str(y_m)+',0,0,0,0]),1,0.8,0,0)\n')
        #                                 print (str(cmd))
        #                                 r.send(cmd)
                                        
                                 

                
        # while 0:
        #         r.send(b'movel(pose_add(get_actual_tcp_pose(),p[-0.05,0,0,0,0,0]),1,0.25,0,0)\n')
        #cmd = str.encode('movel(pose_add(get_actual_tcp_pose(),p['+ str(v_list[0]/100) +','+ str(v_list[1]/100)+',-0.1,0,0,0]),1,0.25,0,0)\n')
        #print (str(cmd))
        #r.send(cmd)

        


if __name__ == '__main__':
    import sys
    main()

