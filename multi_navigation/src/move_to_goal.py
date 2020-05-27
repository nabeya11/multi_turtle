#!/usr/bin/env python
import rospy
import math
import tf
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    rospy.init_node('move_to_goal')
    tb3_name = rospy.get_param('tb3_name')

    listener = tf.TransformListener()
    cmd = Twist()

    # velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    velocity_publisher = rospy.Publisher('destination_component', Twist, queue_size=10)

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/' + tb3_name + '/base_footprint','/' + tb3_name + '/goal', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        # cmd.linear.x = 0.15 * math.sqrt(math.sqrt(trans[0] ** 2 + trans[1] ** 2))
        # if cmd.linear.x > 0.15:
        #     cmd.linear.x = 0.15
        # cmd.angular.z = 0.5 * math.atan2(trans[1], trans[0])

        cmd.linear.x = 0.4 * trans[0]
        if cmd.linear.x > 0.15:
            cmd.linear.x = 0.15

        if trans[0] > 0:
            cmd.angular.z = 1.4 * trans[1]
        else:
            cmd.angular.z = -1.4 * trans[1]

        velocity_publisher.publish(cmd)
        

        rate.sleep()
        