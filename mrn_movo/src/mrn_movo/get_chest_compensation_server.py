#!/usr/bin/env python3

from __future__ import print_function
import re

from mrn_movo.srv import Get_Chest_Compensation
from mrn_movo.msg import ChestCompensationRequest
from mrn_movo.msg import ChestCompensationResponse
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
from geometry_msgs.msg import Point, PointStamped
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from mrn_movo.baseToKinect import transformFromPoint
import numpy as np
import rospy

def chest_adapt(req):
    # movo_op_chest = chest_op_transform(req.chest_compensation.chest_position)
    movo_op_chest = chest_op_transform()
    delta_chest = movo_op_chest[0] - req.chest_compensation.dist_chest.data
    delta_chest_adjusted = delta_chest + odom_listener().position.x
    if abs(delta_chest) > req.chest_compensation.threshold.data:
        response = ChestCompensationResponse()
        response.move_distance.data = delta_chest_adjusted
        return response
    # return chest_move_to
    
    
def op_wrist_listener():
    wrist_pos = rospy.wait_for_message("/mrn_vision/openpose/body/wrist_right", PointStamped)
    return wrist_pos

def op_chest_listener():
    chest_pos = rospy.wait_for_message("/mrn_vision/openpose/body/chest", PointStamped)
    return chest_pos

def head_listener():
    head_joints = rospy.wait_for_message('/movo/head/joint_states', JointState)
    return head_joints
            
def linearAct_listener():
    linearAct_joints = rospy.wait_for_message('/movo/linear_actuator/joint_states', JointState)
    return linearAct_joints

def odom_listener():
    odom = rospy.wait_for_message('/movo/odometry/local_filtered', Odometry)
    return odom.pose.pose

def chest_op_transform():
    theta_pan = head_listener().position[0]
    theta_tilt = head_listener().position[1]
    torso_height = linearAct_listener().position[0]
    op_xyz = op_chest_listener().point
    chest_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_chest_point = Point()
    op_chest_point.x = chest_point[0]
    op_chest_point.y = chest_point[1]
    op_chest_point.z = chest_point[2]
    return chest_point  
            
def chest_compensation_server():
    rospy.init_node('chest_compensation_server')
    s = rospy.Service('chest_compensation', Get_Chest_Compensation, chest_adapt)
    print("Ready to get provide Chest Compensation")
    rospy.spin()

if __name__=="__main__":
    print("Executing Chest Compensation Server")
    chest_compensation_server()
    
    