#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import tf
import tf2_ros
from geometry_msgs.msg import Pose

if __name__ == '__main__':
  try:
    rospy.init_node('absolute_pos', anonymous=True)
    r = rospy.Rate(60)
    listener = tf.TransformListener()
    abs_pos = Pose()
    pub = list()

    robot_list = rospy.get_param('robot_list')

    for robot_info in robot_list:
      if robot_info['enable']:
        pub.append(rospy.Publisher(robot_info['name']+'/absolute_pos', Pose, queue_size=0, latch=True))
      else:
        pub.append(0)

    while not rospy.is_shutdown():
      for robot_info in robot_list:
        if robot_info['enable']:
          try:
            listener.waitForTransform("/map", robot_info['name'] + "/base_footprint", rospy.Time(0), rospy.Duration(10.0))
            (trans,rot) = listener.lookupTransform("/map", robot_info['name'] + "/base_footprint", rospy.Time(0))
            abs_pos.position.x = trans[0]
            abs_pos.position.y = trans[1]
            e = tf.transformations.euler_from_quaternion(rot)
            abs_pos.orientation.z = e[2]
            print(robot_info['name'])
            print(abs_pos.orientation.z)

          except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
            print(error)

          pub[robot_info['id']].publish(abs_pos)

      r.sleep()

  except rospy.ROSInterruptException:
    pass
