#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import roslib
import rospy
import numpy
from geometry_msgs.msg import Twist

global twist_avoid
global twist_comp
global cnt
twist_avoid=Twist()
twist_comp=Twist()

def destination_subscriber():
    rospy.init_node('comp_vel_publisher',anonymous=True)
    rospy.Subscriber('destination_component', Twist, vel_publisher)
    rospy.Subscriber('avoidance_component', Twist, avoidcallback)
    compvel_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(60.0)
    zerovel = Twist()
    zerovel.linear.x = 0.0
    zerovel.angular.z = 0.0

    global cnt
    cnt=0

    global twist_avoid
    global twist_comp


    while not rospy.is_shutdown():
        if(cnt>6):
            compvel_publisher.publish(zerovel)
        else:
            if numpy.sign(twist_avoid.linear.x) != numpy.sign(twist_comp.linear.x):
                twist_comp.linear.x *= 1.0 - abs(twist_avoid.linear.x)
                twist_comp.angular.z += twist_avoid.angular.z
            # print twist_avoid
            # print(twist_avoid.linear.x)
            compvel_publisher.publish(twist_comp)

            cnt = cnt + 1

        rate.sleep()

def avoidcallback(avoid):
    global twist_avoid
    twist_avoid = avoid

def vel_publisher(dest):
    global cnt
    global twist_comp
    twist_comp = dest
    cnt = 0

if __name__ == '__main__':
    try:
        destination_subscriber()
    except rospy.ROSInterruptException: pass
