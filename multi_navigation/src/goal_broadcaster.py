#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped

if __name__ == '__main__':
    try:
        rospy.init_node('tb3_goal_broadcaster')
        tb3_name = rospy.get_param('tb3_name')
        r = rospy.Rate(60)

        # ブロードキャスタ、Transform
        br = tf2_ros.StaticTransformBroadcaster()
        t = TransformStamped()
        # Transform の時刻情報、Base となる座標系、world を Base とする座標系
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "map"
        t.child_frame_id = tb3_name + "/goal"

        # 6D pose (位置 translation、姿勢 rotation)
        t.transform.translation.z = 0
        t.transform.rotation.x = 0
        t.transform.rotation.y = 0
        t.transform.rotation.z = 0
        t.transform.rotation.w = 1

        print("Let's move your robot")
        while not rospy.is_shutdown():
            #Receiveing the user's input
            print(tb3_name)
            try:
                t.transform.translation.x = input("Input position x:")
                t.transform.translation.y = input("Input position y:")
            except:
                break
            else:
                br.sendTransform(t)
            #Loop to move the turtle in an specified distance
                r.sleep()
    except rospy.ROSInterruptException: pass
