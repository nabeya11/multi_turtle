#!/usr/bin/env python
import rospy
import numpy as np
import math
import tf
import tf2_ros
from sensor_msgs.msg import LaserScan

class RobotInfo:
  def __init__(self):
    self.total_number = rospy.get_param('total_number')
    self.my_number = rospy.get_param('my_number')

class ScanData:
  def __init__(self):
    self.distance = np.zeros(360)
    self.arg = np.arange(360.0) / 180 * np.pi
    self.x = np.zeros(360)
    self.y = np.zeros(360)
    rospy.Subscriber('scan', LaserScan, self._scan_callback)

  def _scan_callback(self, get_data):
    self.distance = np.array(get_data.ranges)
    self.x = get_data.ranges * np.cos(self.arg)
    self.y = get_data.ranges * np.sin(self.arg)

def send_each_pos():
  pub_array = rospy.Publisher('rel_polar_vector', PoseArray, queue_size=10)
  send_array = PoseArray()

  for robotnum in robot_total_number:
    independent_pose = Pose()
    independent_pose.position.x = 0
    independent_pose.position.y = 0
    send_array.poses.append(independent_pose)

  pub_array.publish(send_array)

def get_tf_pos(robot_info, robot_num, listener):
  try:
    listener.clear()
    tfnow = rospy.Time(0)
    listener.waitForTransform("tb3_%d/base_footprint" % robot_info.my_number, "tb3_%d/base_footprint" % robot_num, tfnow, rospy.Duration(10.0))
    (trans,rot) = listener.lookupTransform("tb3_0/base_footprint", "tb3_1/base_footprint", tfnow)
    return trans[0], trans[1]

  except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
    print(error)


def main_loop():
  robot_info=RobotInfo()
  scan_data = ScanData()
  listener = tf.TransformListener()

  while not rospy.is_shutdown():
    print(get_tf_pos(robot_info, 1, listener))

if __name__ == '__main__':
  try:
    rospy.init_node('listen_tf', anonymous=True)

    main_loop()

  except rospy.ROSInterruptException:
    pass
