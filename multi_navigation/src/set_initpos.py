#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import PoseStamped

if __name__ == '__main__':
  try:
    rospy.init_node('set_initpos', anonymous=True)

    total_number = rospy.get_param('total_robotnumber')
    robot_list = rospy.get_param('robot_list')

    print(robot_list[0]['name'])

  except rospy.ROSInterruptException:
    pass
