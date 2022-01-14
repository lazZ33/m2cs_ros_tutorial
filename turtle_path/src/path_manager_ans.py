#!/usr/bin/env python3

import rospy

from math import pi, fmod, sin, cos, sqrt

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

from turtlesim.srv import *

from turtle_path.srv import *




cur_pos = Pose()




def cb_pose(data): # get the current position from subscribing the turtle position

    global cur_pos

    cur_pos = data




def cb_walk(req):

    rate = rospy.Rate(100) # 100Hz control loop

    

    if (req.distance < 0):

        return False

    else:

        # calculate the projected (x, y) after walking the distance

        x_coor = cur_pos.x + req.distance*cos(cur_pos.theta)

        y_coor = cur_pos.y + req.distance*sin(cur_pos.theta)

        

        # return false if target coordinate is outside the boundary

        if x_coor > 11 or x_coor < 0 or y_coor > 11 or y_coor < 0:

            return False 




    linear_vel = 1

    

    # Number of counts of looping    

    count = 100 * req.distance / linear_vel

    i = 0




    while (i < count): # control loop

        i += 1

        vel = Twist()

        vel.linear.x = linear_vel

        pub.publish(vel)

        rate.sleep()




    # publish a velocity 0 at the end, to ensure the turtle really stops

    vel = Twist() 

    pub.publish(vel)

    return True



def cb_orientation(req):

    rate = rospy.Rate(100)

    

    # Given 2 angles in the range -PI -> PI around a coordinate, what is the value of the smallest of the 2 angles between them?

    # Reference: https://stackoverflow.com/questions/1878907/how-can-i-find-the-difference-between-two-angles

 

    # signed smallest distance between two angles:

    ang_dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi




    ang_vel_const = 0.6 # constant turning speed of turtle

    

    flag = 1  # indicate the turning direction of turtle: positive for anti-clowise

    if ang_dist < 0:

        flag = -1

    

    count = 100 * flag * ang_dist / ang_vel_const

    i = 0

    while (i < count): 

        i += 1

        ang_vel = Twist()

        ang_vel.angular.z = ang_vel_const * flag

        pub.publish(ang_vel)

        rate.sleep()




    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops

    pub.publish(vel)




    return True




if __name__ == '__main__':

    rospy.init_node('path_manager_ans')




    # publisher of the turtle velocity

    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)

    # subscriber of the turtle position, callback to cb_pose

    sub = rospy.Subscriber('/turtle1/pose',Pose,cb_pose)




    # /set_orientation and /walk_distance services:

    cb_orientation = rospy.Service('set_orientation', SetOrientation, cb_orientation)  

    cb_walk = rospy.Service('walk_distance', WalkDistance, cb_walk)  




    rospy.spin()



