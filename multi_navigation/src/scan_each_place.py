#!/usr/bin/env python
import rospy
import sys
import numpy as np
import math
import tf
# import tf2_ros
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from tf2_msgs.msg import TFMessage
from beginner.msg import polar_message
# np.set_printoptions(threshold=sys.maxsize)

class FTC:
  my_number = -1
  my_number_ref = {"tb3_0":0, "tb3_1":1}
  total_number_of_robots = len(my_number_ref)
  cd = np.zeros((total_number_of_robots, 3)) #  my_number, dist(m), rect(rad)
  sd = np.zeros((360, 4)) # scan_dist, scan_rect, scan_x, scan_y
  # sd[:, 1] = math.radians(np.arange(360.0))
  sd[:, 1] = np.arange(360.0) / 180 * np.pi
  flag = np.zeros((360, total_number_of_robots))
  head_diameter = 0.15 / 2 # r = 7.5 cm

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

def get_the_global_coordinates(i):
  listener = tf.TransformListener()
  # listener = tf.TransformListener()FTC.listener.waitForTransform("tb3_%d/base_footprint" % FTC.my_number, "tb3_%d/base_footprint" % i, rospy.Time.now(), rospy.Duration(4.0))
  # tfBuffer = tf2_ros.Buffer()
  # listener = tf2_ros.TransformListener(tfBuffer)
  try:
    listener.waitForTransform("tb3_%d/base_footprint" % FTC.my_number, "tb3_%d/base_footprint" % i, rospy.Time(), rospy.Duration(4.0))
    (trans,rot) = listener.lookupTransform("tb3_%d/base_footprint" % FTC.my_number, "tb3_%d/base_footprint" % i, rospy.Time(0))
    dist = (trans[0] ** 2 + trans[1] ** 2) ** 0.5
    rect = math.atan2(trans[1], trans[0])
    return i, dist, rect

  except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as error:
    print(error)
    return i, FTC.cd[i, 1], FTC.cd[i, 2]

# def limit_angle(dist, rect):
#   limit_angle = []
#   angle = np.round(math.degrees(rect))
#   angle_range = np.ceil(math.degrees(math.asin(FTC.head_diameter / dist)))
#   return limit_angle

def callback(data):
  FTC.sd[:, 0] = np.array(data.ranges)
  FTC.sd[:, 2] = FTC.sd[:, 0] * np.cos(FTC.sd[:, 1])
  FTC.sd[:, 3] = FTC.sd[:, 0] * np.sin(FTC.sd[:, 1])
  for j in range(FTC.total_number_of_robots):
    if j == FTC.my_number:
      continue
    else:
      for i in range(360):
        if (((FTC.sd[i, 2] - FTC.cd[j, 1] * np.cos(FTC.cd[j, 2])) ** 2 + (FTC.sd[i, 3] - FTC.cd[j, 1] * np.sin(FTC.cd[j, 2])) ** 2) < FTC.head_diameter ** 2):
          FTC.flag[i, j] = 1
        else:
          FTC.flag[i, j] = 0
      count = sum(FTC.flag[:, j])
      if count > 3:
        x_ = sum(FTC.sd[:, 2] * FTC.flag[:, j]) / count
        y_ = sum(FTC.sd[:, 3] * FTC.flag[:, j]) / count
        FTC.cd[j, 1] = (x_ ** 2 + y_ ** 2) ** 0.5
        FTC.cd[j, 2] = math.atan2(y_, x_)
      else:
        FTC.cd[j, 0], FTC.cd[j, 1], FTC.cd[j, 2] = get_the_global_coordinates(j)
        print("No." + str(FTC.my_number) + " to No." + str(j) + "is Global coordinates now.")
  # print(j, FTC.cd[j, 1], FTC.cd[j, 2] / np.pi * 180)
  # print(0, FTC.cd[0, 1], FTC.cd[0, 2] / np.pi * 180)

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
  for i in range(FTC.total_number_of_robots):
    b = Pose()
    b.position.x = FTC.cd[i, 1] * np.cos(FTC.cd[i, 2])
    b.position.y = FTC.cd[i, 1] * np.sin(FTC.cd[i, 2])
    a.append(b)
  FTC.array_array.poses = a
  FTC.pub_array.publish(FTC.array_array)

if __name__ == '__main__':
  try:
    rospy.init_node('find_the_robot', anonymous=True)
    turtlename = rospy.get_param('~turtlename')
    # turtlename = "tb3_0"
    FTC.my_number = FTC.my_number_ref[turtlename]
    for i in range(FTC.total_number_of_robots):
      if i == FTC.my_number:
        FTC.cd[i, 0] = FTC.my_number
      else:
        FTC.cd[i, 0], FTC.cd[i, 1], FTC.cd[i, 2] = get_the_global_coordinates(i)
    # rospy.Subscriber('/%s/scan' % turtlename, LaserScan, callback)
    rospy.Subscriber('scan', LaserScan, callback)
    rospy.spin()
  except rospy.ROSInterruptException:
    pass
