#!/usr/bin/env python
import rospy
import numpy as np
import math
import tf
import tf2_ros
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray

class RobotInfo:
  def __init__(self):
    # my info
    self.my_name = rospy.get_param('tb3_name')
    self.listener = tf.TransformListener()
    self.scan_data = ScanData()

    # others' info
    self.robot_list = rospy.get_param('/robot_list')
    self.curt_pos = PoseArray()
    self.curt_pos.header.frame_id = self.my_name

    self.pub_array = rospy.Publisher('rel_polar_vector', PoseArray, queue_size=10)

  def get_init_pos(self):
    self.curt_pos.poses[:]=[]
    for target in self.robot_list:
      if target['name'] == self.my_name or not target['enable']:
        self.curt_pos.poses.append(Pose())
      else:
        self.curt_pos.poses.append(self.get_tf_pos(target['name']))

  def print_curtpos(self):
    for target in self.robot_list:
      if target['enable']:
        print(target['name'])
        print(self.curt_pos.poses[target['id']].position)

  def send_each_pos(self):
    self.curt_pos.header.seq = rospy.Time.now()
    self.pub_array.publish(self.curt_pos)

  def get_tf_pos(self, target_name):
    try:
      pos = Pose()
      tfnow = rospy.Time(0)
      self.listener.waitForTransform(self.my_name + "/base_footprint", target_name + "/base_footprint", tfnow, rospy.Duration(10.0))
      (trans,rot) = self.listener.lookupTransform(self.my_name + "/base_footprint", target_name + "/base_footprint", tfnow)
      pos.position.x = trans[0]
      pos.position.y = trans[1]

      return pos

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
      print(error)

  def each_trace(self, target):
    head_diameter = 0.3 / 2
    flag = np.zeros(360)
    pre_pos = self.curt_pos.poses[target['id']]
    estimate_pos = Pose()
    for rect in range(360):
      if ((self.scan_data.x[rect] - pre_pos.position.x) ** 2 + (self.scan_data.y[rect] - pre_pos.position.y) ** 2) < (head_diameter ** 2):
        flag[rect] = 1
      else:
        flag[rect] = 0
      if self.scan_data.distance[rect] == float("inf"):
        self.scan_data.x[rect] = 0
        self.scan_data.y[rect] = 0

    count = sum(flag[:])

    if count > 3:
      estimate_pos.position.x = sum(self.scan_data.x[:] * flag[:]) / count
      estimate_pos.position.y = sum(self.scan_data.y[:] * flag[:]) / count
      print("use Local")
    else:
      estimate_pos = self.get_tf_pos(target['name'])
      print("use Global")

    return estimate_pos

  def trace(self):
    for target in self.robot_list:
      if target['enable']:
        if target['name'] == self.my_name:
          continue
        else:
          self.curt_pos.poses[target['id']] = self.each_trace(target)
        self.send_each_pos()

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


def main():
  robot_info = RobotInfo()
  r = rospy.Rate(60)

  print("My number is " + robot_info.my_name)

  #try to set initpos 3times
  for i in range(3):
    robot_info.get_init_pos()
  robot_info.print_curtpos()
  print("init print ended")

  while not rospy.is_shutdown():
    robot_info.trace()
    robot_info.print_curtpos()

    r.sleep()
    # print(robot_info.get_tf_pos('tb3_1'))

if __name__ == '__main__':
  try:
    rospy.init_node('listen_tf', anonymous=True)

    main()

  except rospy.ROSInterruptException:
    pass
