#!/usr/bin/env python
import rospy
import sys
import numpy as np
import math
import tf
import tf2_ros
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from tf2_msgs.msg import TFMessage
from beginner.msg import polar_message

class FTC:
  my_number = -1
  my_number_ref = {"tb3_0":0, "tb3_1":1}
  total_number_of_robots = len(my_number_ref)
  local_pos = np.zeros((total_number_of_robots, 3)) #  my_number, dist(m), rect(rad)
  scandata = np.zeros((360, 4)) # scan_dist, scan_rect, scan_x, scan_y
  scandata[:, 1] = np.arange(360.0) / 180 * np.pi
  flag = np.zeros((360, total_number_of_robots))
  head_diameter = 0.15 / 2 # r = 7.5 cm

  tf_pos = np.zeros((total_number_of_robots, 3)) #  my_number, dist(m), rect(rad)

  # [1] send 1 topic
  # pub1 = rospy.Publisher('rel_polar_vector', Pose, queue_size=10)
  # array1 = Pose()

  # [2] send many topic
  # array = [0] * total_number_of_robots
  # pub = [0] * total_number_of_robots
  # for i in range(total_number_of_robots):
  #   array[i] = Pose()
  #   pub[i] = rospy.Publisher('/rel_polar_vector/%d/' % i , Pose, queue_size=10)

  # [3] PoseArray
  pub_array = rospy.Publisher('rel_polar_vector', PoseArray, queue_size=10)
  array_array = PoseArray()

def get_global_coordinates(robot_num):
  listener = tf.TransformListener()
  try:
    listener.waitForTransform("tb3_%d/base_footprint" % FTC.my_number, "tb3_%d/base_footprint" % robot_num, rospy.Time(), rospy.Duration(1.0))
    (trans,rot) = listener.lookupTransform("tb3_%d/base_footprint" % FTC.my_number, "tb3_%d/base_footprint" % robot_num, rospy.Time(0))
    dist = (trans[0] ** 2 + trans[1] ** 2) ** 0.5
    rect = math.atan2(trans[1], trans[0])
    return robot_num, dist, rect

  except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
    print(error)
    return FTC.local_pos[robot_num, 0], FTC.local_pos[robot_num, 1], FTC.local_pos[robot_num, 2]

def callback(data):
  FTC.scandata[:, 0] = np.array(data.ranges)
  FTC.scandata[:, 2] = FTC.scandata[:, 0] * np.cos(FTC.scandata[:, 1])
  FTC.scandata[:, 3] = FTC.scandata[:, 0] * np.sin(FTC.scandata[:, 1])
  for robot_num in range(FTC.total_number_of_robots):
    if robot_num == FTC.my_number:
      continue
    else:
      for i in range(360):
        if (((FTC.scandata[i, 2] - FTC.local_pos[robot_num, 1] * np.cos(FTC.local_pos[robot_num, 2])) ** 2 + (FTC.scandata[i, 3] - FTC.local_pos[robot_num, 1] * np.sin(FTC.local_pos[robot_num, 2])) ** 2) < FTC.head_diameter ** 2):
          FTC.flag[i, robot_num] = 1
        else:
          FTC.flag[i, robot_num] = 0
      count = sum(FTC.flag[:, robot_num])
      if count > 3:
        x_ = sum(FTC.scandata[:, 2] * FTC.flag[:, robot_num]) / count
        y_ = sum(FTC.scandata[:, 3] * FTC.flag[:, robot_num]) / count
        FTC.local_pos[robot_num, 1] = (x_ ** 2 + y_ ** 2) ** 0.5
        FTC.local_pos[robot_num, 2] = math.atan2(y_, x_)
        print("No." + str(FTC.my_number) + " to No." + str(robot_num) + "is Local coordinates now.")
      else:
        FTC.local_pos[robot_num, :] = FTC.tf_pos[robot_num, :]
        print("No." + str(FTC.my_number) + " to No." + str(robot_num) + "is Global coordinates now.")

  # [1] 1 topic
  # FTC.array1.position.x = sys.float_info.max
  # FTC.array1.position.y = sys.float_info.max
  # for i in range(FTC.total_number_of_robots):
  #   if i != FTC.my_number:
  #     if FTC.cd[i, 1] < ((FTC.array1.position.x ** 2 + FTC.array1.position.y ** 2) ** 0.5):
  #       FTC.array1.position.x = FTC.cd[i, 1] * np.cos(FTC.cd[i, 2])
  #       FTC.array1.position.y = FTC.cd[i, 1] * np.sin(FTC.cd[i, 2])
  # FTC.pub1.publish(FTC.array1)

  # [2] send many topic
  # for i in range(FTC.total_number_of_robots):
  #   FTC.array[i].position.x = FTC.cd[i, 1] * np.cos(FTC.cd[i, 2])
  #   FTC.array[i].position.y = FTC.cd[i, 1] * np.sin(FTC.cd[i, 2])
  #   FTC.pub[i].publish(FTC.array[i])

  # [3] PoseArray
  FTC.array_array.header.seq = FTC.my_number
  FTC.array_array.header.frame_id = 'tb3_%d' % FTC.my_number
  a = []
  for robot_num in range(FTC.total_number_of_robots):
    b = Pose()
    b.position.x = FTC.local_pos[robot_num, 1] * np.cos(FTC.local_pos[robot_num, 2])
    b.position.y = FTC.local_pos[robot_num, 1] * np.sin(FTC.local_pos[robot_num, 2])
    a.append(b)
  FTC.array_array.poses = a
  FTC.pub_array.publish(FTC.array_array)

def main_loop():
  rate = rospy.Rate(10.0)

  while not rospy.is_shutdown():
    for robot_num in range(FTC.total_number_of_robots):
      #listen tf_position and keep
      FTC.tf_pos[robot_num, 0], FTC.tf_pos[robot_num, 1], FTC.tf_pos[robot_num, 2] = get_global_coordinates(robot_num)

    rate.sleep()

if __name__ == '__main__':
  try:
    rospy.init_node('detect_robots', anonymous=True)
    turtlename = rospy.get_param('~turtlename')
    FTC.my_number = FTC.my_number_ref[turtlename]
    #set initial position
    for robot_num in range(FTC.total_number_of_robots):
      if robot_num == FTC.my_number:
        FTC.local_pos[robot_num, 0] = FTC.my_number
      else:
        FTC.local_pos[robot_num, 0], FTC.local_pos[robot_num, 1], FTC.local_pos[robot_num, 2] = get_global_coordinates(robot_num)

    #set subscribe callback
    # rospy.Subscriber('scan', LaserScan, callback)

    main_loop()

  except rospy.ROSInterruptException:
    pass