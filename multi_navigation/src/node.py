#!/usr/bin/python
# coding: utf-8
import rospy

if __name__ == '__main__':
  rospy.init_node('node')
  sense = rospy.get_param('~myparam')
  rate = rospy.Rate(1)
  while not rospy.is_shutdown():
    rospy.loginfo('msg: %s' % sense)
    rate.sleep()
