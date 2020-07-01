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
    self.total_number = rospy.get_param('/total_robotnumber')
    self.robot_list = rospy.get_param('/robot_list')
    self.curt_pos = PoseArray()

    self.pub_array = rospy.Publisher('rel_polar_vector', PoseArray, queue_size=10)

  def get_init_pos(self):
    self.curt_pos.poses[:]=[]
    for target in self.robot_list:
      if target['name'] == self.my_name:
        self.curt_pos.poses.append(0)
      else:
        self.curt_pos.poses.append(self.get_tf_pos(target['name']))

  def print_curtpos(self):
    for target in self.robot_list:
      print(target['name'])
      print(self.curt_pos.poses[target['id']])
    print("init print ended")

  def get_tf_pos(self, target_name):
    try:
      self.listener.clear()
      pos = Pose()
      tfnow = rospy.Time(0)
      self.listener.waitForTransform("{}/base_footprint".format(self.my_name), target_name + "/base_footprint", tfnow, rospy.Duration(10.0))
      (trans,rot) = self.listener.lookupTransform("{}/base_footprint".format(self.my_name), target_name + "/base_footprint", tfnow)
      pos.position.x = trans[0]
      pos.position.y = trans[1]

      return pos

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
      print(error)

  def send_each_pos(self):
    self.pub_array.publish(self.curt_pos)

  # def trace(self, pre_pos):
  #   head_diameter = 0.15 / 2
  #   flag = np.zeros(360)
  #   for rect in range(360):
  #     if ((self.scan_data.x[rect] - pre_pos.position.x) ** 2 + (self.scan_data.y[rect] - pre_pos.position.y) ** 2) < (head_diameter ** 2):
  #       flag[rect] = 1
  #     else:
  #       flag[rect] = 0
  #     if self.scan_data.distance[rect] == float("inf"):
  #       self.scan_data.x[rect] = 0
  #       self.scan_data.y[rect] = 0

  #   count = sum(flag[:])

  #   if count > 3:
  #     self.curt_pos.position.x = sum(self.scan_data.x[:] * flag[:]) / count
  #     self.curt_pos.position.y = sum(self.scan_data.y[:] * flag[:]) / count
  #     # print("No." + str(FTC.my_number) + " to No." + str(robot_info) + "is Local coordinates now.")
  #     print("use Local coordinates now.")
  #   else:
  #     self.curt_pos = self.get_tf_pos()
  #     print("use Global coordinates now.")

  #   return self.curt_pos

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

  print("My number is " + robot_info.my_name)

  #try to set initpos 3times
  for i in range(3):
    robot_info.get_init_pos()
  robot_info.print_curtpos()

  while not rospy.is_shutdown():
    # for target in robot_info.robot_list:
    #   if target['name'] == robot_info.my_name:
    #     continue
    #   else:
    #     scan_data.trace(target, curt_pos.poses[target['id']])

    print(robot_info.get_tf_pos('tb3_1'))

if __name__ == '__main__':
  try:
    rospy.init_node('listen_tf', anonymous=True)

    main()

  except rospy.ROSInterruptException:
    pass
