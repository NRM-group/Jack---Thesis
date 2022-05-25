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

def odom_listener():
    odom = rospy.wait_for_message('/movo/odometry/local_filtered', Odometry)
    return odom.pose.pose

def chest_op_transform_to_odom():
    theta_pan = head_listener().position[0]
    theta_tilt = head_listener().position[1]
    torso_height = linearAct_listener().position[0]
    odom = odom_listener()
    wrist_right =       transformFromPoint(op_wrist_right_listener(), torso_height, theta_pan, theta_tilt, odom)
    wrist_right =       np.reshape(wrist_right,3)
    wrist_left =        transformFromPoint(op_wrist_left_listener(), torso_height, theta_pan, theta_tilt, odom)
    wrist_left =        np.reshape(wrist_left,3)
    elbow_right =       transformFromPoint(op_elbow_right_listener(), torso_height, theta_pan, theta_tilt, odom)
    elbow_right =        np.reshape(elbow_right,3)
    elbow_left =        transformFromPoint(op_elbow_left_listener(), torso_height, theta_pan, theta_tilt, odom)
    elbow_left =        np.reshape(elbow_left,3)
    shoulder_right =    transformFromPoint(op_shoulder_right_listener(), torso_height, theta_pan, theta_tilt, odom)
    shoulder_right =    np.reshape(shoulder_right,3)
    shoulder_left =     transformFromPoint(op_shoulder_left_listener(), torso_height, theta_pan, theta_tilt, odom)
    shoulder_left =     np.reshape(shoulder_left,3)
    chest =             transformFromPoint(op_chest_listener(), torso_height, theta_pan, theta_tilt, odom)
    chest =             np.reshape(chest,3)
    head =              transformFromPoint(op_head_listener(), torso_height, theta_pan, theta_tilt, odom)
    head =              np.reshape(head,3)
    keypoints = np.concatenate((head, chest, shoulder_right, elbow_right, wrist_right, shoulder_left, elbow_left, wrist_left), axis=0)
    print(keypoints)
    global output_keypoints
    print(output_keypoints)
    output_keypoints = np.vstack((output_keypoints, keypoints))
    return output_keypoints
    
def end_recording():
    np.savetxt("test.csv", output_keypoints, delimiter=",")
    
if __name__=="__main__":
    rospy.init_node('mrn_movo_output_openpose', anonymous=True)
    output_keypoints = np.empty([1,24])
    rospy.on_shutdown(end_recording)
    
    while True:
        output_keypoints = chest_op_transform_to_odom()
    
    
    
    