#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import math
import numpy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from multi_navigation.msg import polar_message

global tb3_name

def relative_subscriber():
    global tb3_name
    rospy.init_node('avoid_collision' , anonymous=True)
    tb3_name = rospy.get_param('tb3_name')
    rospy.Subscriber('rel_polar_vector' , PoseArray , avoid_publisher)
    rospy.spin()

def avoid_publisher(posearray):
    global tb3_name
    vel_avoid_publisher = rospy.Publisher('avoidance_component',Twist,queue_size = 10)
    # rate = rospy.Rate(5)

    #一番近いやつだけ避ける
    rlist = [10] * len(posearray.poses)
    thetalist = [0] * len(posearray.poses)
    for i in range(len(posearray.poses) ):
        if tb3_name != "tb3_%d" % i:
            rlist[i] = math.sqrt(posearray.poses[i].position.x ** 2 + posearray.poses[i].position.y ** 2)
            thetalist[i] = math.atan2(posearray.poses[i].position.y , posearray.poses[i].position.x )
    r = min(rlist)
    theta = thetalist[rlist.index(r)]

    # r = math.sqrt(pose.position.x ** 2 + pose.position.y ** 2)
    # theta = math.atan2(pose.position.y , pose.position.x )
    vel_msg = Twist()
    radius = 0.7
    x_limit = 0.05
    rot_limit = 0.6
    if r < radius :
        vel_msg.linear.x = -x_limit * (radius - r)  * math.cos(theta)
        if r == 0:
            vel_msg.angular.z = 0
        else:
            vel_msg.angular.z = rot_limit * math.cos(theta) / r
            vel_msg.angular.z *= -numpy.sign(math.sin(theta))
    else:
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
    vel_avoid_publisher.publish(vel_msg)

    # rospy.loginfo("end send\n\r" )
if __name__ == '__main__':
    try:
        #Testing our function
        relative_subscriber()
    except rospy.ROSInterruptException: pass
