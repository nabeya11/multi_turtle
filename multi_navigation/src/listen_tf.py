#!/usr/bin/env python
import rospy
import tf
import tf2_ros


def main_loop():
  listener = tf.TransformListener()

  while not rospy.is_shutdown():
    try:
      listener.clear()
      tfnow = rospy.Time(0)
      listener.waitForTransform("tb3_0/base_footprint", "tb3_1/base_footprint", tfnow, rospy.Duration(10.0))
      (trans,rot) = listener.lookupTransform("tb3_0/base_footprint", "tb3_1/base_footprint", tfnow)
      print(trans[0], trans[1])

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as error:
      print(error)

if __name__ == '__main__':
  try:
    rospy.init_node('listen_tf', anonymous=True)

    main_loop()

  except rospy.ROSInterruptException:
    pass
