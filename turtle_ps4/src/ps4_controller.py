#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest
# hint: some imports are missing
from m2_ps4.msg import Ps4Data
from std_srvs.srv import Empty
old_data = Ps4Data()
k=3
req = SetPenRequest()
default = SetPenRequest()
default.r = 0
default.g = 0
default.b = 0
req.r = 0
req.g = 0
req.b = 0

def callback(data):
    global old_data,k
    
    t=Twist()
    # you should publish the velocity here!
    
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # 
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...
    if data.dpad_y != old_data.dpad_y:
    	if data.dpad_y >0 and k<5:
    		k+=1
    	elif data.dpad_y <0 and k>1:
    		k-=1
    t.linear.x = data.hat_ly * k
    t.angular.z = data.hat_rx * k
    
    if data.triangle==True:
        req.r=0
        req.g=255
        req.b=0
    elif data.circle==True:
        req.r=255
        req.g=0
        req.b=0
    elif data.cross==True:
        req.r=0
        req.g=0
        req.b=255
    elif data.square==True:
        req.r=128
        req.g=0
        req.b=128
    else:
        req.r=0
        req.g=0
        req.b=0
    if req != default:
        srv_col(req)
    
    if data.ps==True and old_data.ps==False:
        srv_clr()
    
    pub.publish(t)
    old_data = data

if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    pub = rospy.Publisher("turtle1/cmd_vel",Twist,queue_size = 1)# publisher object goes here... hint: the topic type is Twist
    rospy.Subscriber("input/ps4_data",Ps4Data,callback)# subscriber object goes here
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy('turtle1/set_pen',SetPen)
    srv_clr = rospy.ServiceProxy('/clear',Empty)
    # service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...

    rospy.spin()
