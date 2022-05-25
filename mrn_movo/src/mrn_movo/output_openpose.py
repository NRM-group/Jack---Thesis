#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState, Image
from geometry_msgs.msg import (
    PointStamped,
    Point
)
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs
import trajectory_msgs
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
import numpy as np  
from mrn_movo.baseToKinect import transformFromPoint
import time
import csv





def op_wrist_right_listener():
    wrist_pos = rospy.wait_for_message("/mrn_vision/openpose/body/wrist_right", PointStamped)
    return wrist_pos.point

def op_wrist_left_listener():
    wrist_pos = rospy.wait_for_message("/mrn_vision/openpose/body/wrist_left", PointStamped)
    return wrist_pos.point

def op_elbow_right_listener():
    elbow_pos = rospy.wait_for_message("/mrn_vision/openpose/body/elbow_right", PointStamped)
    return elbow_pos.point

def op_elbow_left_listener():
    elbow_pos = rospy.wait_for_message("/mrn_vision/openpose/body/elbow_left", PointStamped)
    return elbow_pos.point

def op_shoulder_right_listener():
    shoulder_pos = rospy.wait_for_message("/mrn_vision/openpose/body/shoulder_right", PointStamped)
    return shoulder_pos.point

def op_shoulder_left_listener():
    shoulder_pos = rospy.wait_for_message("/mrn_vision/openpose/body/shoulder_left", PointStamped)
    return shoulder_pos.point

def op_chest_listener():
    chest_pos = rospy.wait_for_message("/mrn_vision/openpose/body/chest", PointStamped)
    return chest_pos.point

def op_head_listener():
    head_pos = rospy.wait_for_message("/mrn_vision/openpose/body/head", PointStamped)
    return head_pos.point

def head_listener():
    head_joints = rospy.wait_for_message('/movo/head/joint_states', JointState)
    return head_joints
            
def linearAct_listener():
    linearAct_joints = rospy.wait_for_message('/movo/linear_actuator/joint_states', JointState)
    return linearAct_joints

def chest_op_transform_to_odom():
    t = time.time()
    theta_pan = head_listener().position[0]
    theta_tilt = head_listener().position[1]
    torso_height = linearAct_listener().position[0]
    wrist_right =       op_wrist_right_listener()
    wrist_right =       [wrist_right.x, wrist_right.y, wrist_right.z]
    wrist_left =        op_wrist_left_listener()
    wrist_left =        [wrist_left.x, wrist_left.y, wrist_left.z]
    elbow_right =       op_elbow_right_listener()
    elbow_right =       [elbow_right.x, elbow_right.y, elbow_right.z]
    elbow_left =        op_elbow_left_listener()
    elbow_left =        [elbow_left.x, elbow_left.y, elbow_left.z]
    shoulder_right =    op_shoulder_right_listener()
    shoulder_right =    [shoulder_right.x, shoulder_right.y, shoulder_right.z]
    shoulder_left =     op_shoulder_left_listener()
    shoulder_left =     [shoulder_left.x, shoulder_left.y, shoulder_left.z]
    chest =             op_chest_listener()
    chest =             [chest.x, chest.y, chest.z]
    head =              op_head_listener()
    head =              [head.x, head.y, head.z]
    keypoints = np.hstack((head, chest, shoulder_right, elbow_right, wrist_right, shoulder_left, elbow_left, wrist_left, theta_pan, theta_tilt, torso_height, t))
    print(keypoints.shape)
    keypoints = np.reshape(keypoints, (1,28))
    print(keypoints.shape)
    return keypoints
    
if __name__=="__main__":
    rospy.init_node('mrn_movo_output_openpose', anonymous=True)
    output_keypoints = np.empty([1,28])
    while True:
        output_keypoints = np.append(output_keypoints, chest_op_transform_to_odom(), axis=0)
        print(output_keypoints)
        np.savetxt("test.csv", output_keypoints, delimiter=",")
    
    
    
    