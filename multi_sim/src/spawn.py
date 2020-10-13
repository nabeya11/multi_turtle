#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import SpawnModel

if __name__ == '__main__':
    rospy.init_node('spawn')
    tb3_name = rospy.get_param('~tb3_name')
    robot_description = rospy.get_param('robot_desc')
    robot_list = rospy.get_param('robot_list')

    init_pose = Pose()
    init_pose.position.x = 3
    init_pose.position.y = 3
    init_pose.orientation.z = 0

    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
    spawn_model_client(
        model_name = 'tb3_name',
        model_xml = open(robot_description, 'r').read(),
        robot_namespace = 'tb3_name',
        initial_pose = init_pose,
        reference_frame='world'
    )
