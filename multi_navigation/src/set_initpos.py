#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

if __name__ == '__main__':
  try:
    rospy.init_node('set_initpos', anonymous=True)

    robot_list = rospy.get_param('robot_list')

    print("follow are the names of robot which is set initpos")
    for robot_info in robot_list:
      if robot_info['enable']:
        print(robot_info['name'])
        pub = rospy.Publisher(robot_info['name']+'/initialpose', PoseWithCovarianceStamped, queue_size=0, latch=True)
        initpos = PoseWithCovarianceStamped()

        initpos.header.stamp = rospy.Time.now()
        initpos.header.frame_id = 'map'
        initpos.pose.pose.position.x = robot_info['init_pos'][0]
        initpos.pose.pose.position.y = robot_info['init_pos'][1]
        initpos.pose.pose.orientation.z = robot_info['init_pos'][2]
        initpos.pose.pose.orientation.w = 1
        # initpos.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]

        pub.publish(initpos)

    print("Finished settting all initial position")
    rospy.spin()

  except rospy.ROSInterruptException:
    pass
