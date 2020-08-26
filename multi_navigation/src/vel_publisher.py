#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import roslib
import rospy
import numpy
from geometry_msgs.msg import Twist

global twist_avoidance
twist_avoidance=Twist()

def destination_subscriber():
    rospy.init_node('comp_vel_publisher',anonymous=True)
    rospy.Subscriber('destination_component', Twist, vel_publisher)
    rospy.Subscriber('avoidance_component', Twist, avoidcallback)
    rospy.spin()

def avoidcallback(avoid):
    global twist_avoidance
    twist_avoidance = avoid

def vel_publisher(comp):
    global twist_avoidance
    compvel_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    if numpy.sign(twist_avoidance.linear.x) != numpy.sign(comp.linear.x):
        comp.linear.x *= 1.0 - abs(twist_avoidance.linear.x)
        comp.angular.z += twist_avoidance.angular.z
    print twist_avoidance
    # print(twist_avoidance.linear.x)
    compvel_publisher.publish(comp)

if __name__ == '__main__':
    try:
        destination_subscriber()
    except rospy.ROSInterruptException: pass
