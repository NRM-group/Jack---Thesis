#!/usr/bin/env python3

from __future__ import print_function
import rospy

import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
import trajectory_msgs.msg
import geometry_msgs.msg
from sensor_msgs.msg import JointState
import numpy as np
import time

start = time.time()


rospy.init_node("mrn_movo_bio_ik_left_side")

rospy.wait_for_service("/bio_ik/get_bio_ik")
get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)
pub = rospy.Publisher('/mrn_movo/left_arm/state', moveit_msgs.msg.RobotState, queue_size=1, latch=True)

def left_arm_ik(x, y, z):
    
    request = bio_ik_msgs.msg.IKRequest()

    request.group_name = "left_side"

    request.timeout.secs = 1

    request.approximate = True
    
    global robot_state
    request.robot_state = robot_state.solution

    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_base_link"
    request.pose_goals[-1].pose.position.x = x
    request.pose_goals[-1].pose.position.y = y
    request.pose_goals[-1].pose.position.z = z
    request.pose_goals[-1].pose.orientation.x = 0.0
    request.pose_goals[-1].pose.orientation.y = -0.707
    request.pose_goals[-1].pose.orientation.z = 0.0
    request.pose_goals[-1].pose.orientation.w = 0.707

    response = get_bio_ik(request).ik_response
    print(response)
    
def left_arm_ik_initial(x, y, z):
    request = bio_ik_msgs.msg.IKRequest()
    request.group_name = "left_side"
    request.timeout.secs = 1
    request.approximate = True
    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_base_link"
    request.pose_goals[-1].pose.position.x = 0.8
    request.pose_goals[-1].pose.position.y = 0.35
    request.pose_goals[-1].pose.position.z = 0.75
    request.pose_goals[-1].pose.orientation.x = 0.0
    request.pose_goals[-1].pose.orientation.y = -0.707
    request.pose_goals[-1].pose.orientation.z = 0.0
    request.pose_goals[-1].pose.orientation.w = 0.707

    response = get_bio_ik(request).ik_response
    global robot_state
    robot_state = response
    print(response)
    

if __name__ == '__main__':
    print('Postion 1:', 0.8, 0.35, 0.75)
    left_arm_ik_initial(0.8, 0.35, 0.75)
    print('Postion 2:', 0.8, 0.35, 0.75)
    left_arm_ik(0.8, 0.7, 1)

