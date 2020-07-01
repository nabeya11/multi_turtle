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
    self.total_number = rospy.get_param('/total_robotnumber')
    self.my_name = rospy.get_param('tb3_name')
    self.robot_list = rospy.get_param('/robot_list')

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

  pub_array.publish(send_array)

def get_tf_pos(my_name, target_name, listener):
  try:
    listener.clear()
    pos = Pose()
    tfnow = rospy.Time(0)
    listener.waitForTransform("{}/base_footprint".format(my_name), target_name + "/base_footprint", tfnow, rospy.Duration(10.0))
    (trans,rot) = listener.lookupTransform("{}/base_footprint".format(my_name), target_name + "/base_footprint", tfnow)
    pos.position.x = trans[0]
    pos.position.y = trans[1]

    return pos

  except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
    print(error)

# def trace():
#   for robot_info in RobotInfo.robot_list:
#     if robot_info['name'] == RobotInfo.my_name:
#       continue
#     else:
#       for rect in range(360):
#         if ((FTC.scandata[rect, 2] - FTC.local_pos[robot_info, 0]) ** 2 + (FTC.scandata[rect, 3] - FTC.local_pos[robot_info, 1]) ** 2) < (FTC.head_diameter ** 2):
#           FTC.flag[rect, robot_info] = 1
#         else:
#           FTC.flag[rect, robot_info] = 0
#         if FTC.scandata[rect, 0] == float("inf"):
#           FTC.scandata[rect, 2] = 0
#           FTC.scandata[rect, 3] = 0
#       count = sum(FTC.flag[:, robot_info])
#       if count > 3:
#         FTC.local_pos[robot_info, 0] = sum(FTC.scandata[:, 2] * FTC.flag[:, robot_info]) / count
#         FTC.local_pos[robot_info, 1] = sum(FTC.scandata[:, 3] * FTC.flag[:, robot_info]) / count
#         print("No." + str(FTC.my_number) + " to No." + str(robot_info) + "is Local coordinates now.")
#       else:
#         FTC.local_pos[robot_info, :] = FTC.tf_pos[robot_info, :]
#         print("No." + str(FTC.my_number) + " to No." + str(robot_info) + "is Global coordinates now.")


def main():
  robot_info = RobotInfo()
  scan_data = ScanData()
  listener = tf.TransformListener()

  print("My number is " + robot_info.my_name)

  #set initpos 3times
  curt_pos = PoseArray()
  for i in range(3):
    curt_pos.poses[:]=[]
    for robot in robot_info.robot_list:
      if robot['name'] == robot_info.my_name:
        curt_pos.poses.append(0)
      else:
        curt_pos.poses.append(get_tf_pos(robot_info.my_name, robot['name'], listener))

      print(robot['id'], curt_pos.poses[robot['id']])

  while not rospy.is_shutdown():
    print(get_tf_pos(robot_info.my_name, 'tb3_1', listener))

if __name__ == '__main__':
  try:
    rospy.init_node('listen_tf', anonymous=True)

    main()

  except rospy.ROSInterruptException:
    pass
