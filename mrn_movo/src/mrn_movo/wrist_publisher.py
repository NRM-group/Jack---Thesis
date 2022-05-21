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



rospy.init_node('wrist_publisher', anonymous=True)
rospy.wait_for_service("/bio_ik/get_bio_ik")
get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)

# Publish Positions to Move To
left_arm_ik_pub = rospy.Publisher('/mrn_movo/left_arm/IK_openpose', JointState, queue_size=1, latch=True)

# Publish Transformed OpenPose Keypoints
wrist_right_op_pub = rospy.Publisher('mrn_vision/openpose/movo/wrist_right', Point, queue_size=1)

robot_state = None

def left_arm_ik(x, y, z):
    
    request = bio_ik_msgs.msg.IKRequest()

    request.group_name = "whole_body_left"

    request.timeout.secs = 1

    request.approximate = True
    
    global robot_state
    request.robot_state = robot_state
    # request.robot_state = rospy.wait_for_message('/mrn_movo/left_arm/IK', moveit_msgs.msg.RobotState)
    
    # request.minimal_displacement_goals = 0.8

    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_finger1_finger_tip_link"
    request.pose_goals[-1].pose.position.x = x
    request.pose_goals[-1].pose.position.y = y
    request.pose_goals[-1].pose.position.z = z
    request.pose_goals[-1].pose.orientation.x = 0.5
    request.pose_goals[-1].pose.orientation.y = -0.5
    request.pose_goals[-1].pose.orientation.z = 0.5
    request.pose_goals[-1].pose.orientation.w = 0.5

    response = get_bio_ik(request).ik_response
    left_arm_ik_pub.publish(response.solution.joint_state)
    
def left_arm_ik_initial(x, y, z):
    
    request = bio_ik_msgs.msg.IKRequest()

    request.group_name = "whole_body_left"

    request.timeout.secs = 1

    request.approximate = True

    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_finger1_finger_tip_link"
    request.pose_goals[-1].pose.position.x = x
    request.pose_goals[-1].pose.position.y = y
    request.pose_goals[-1].pose.position.z = z
    request.pose_goals[-1].pose.orientation.x = 0.5
    request.pose_goals[-1].pose.orientation.y = -0.5
    request.pose_goals[-1].pose.orientation.z = 0.5
    request.pose_goals[-1].pose.orientation.w = 0.5

    response = get_bio_ik(request).ik_response
    left_arm_ik_pub.publish(response.solution.joint_state)
    global robot_state
    robot_state = response.solution    
    
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

def wrist_op_transform_to_odom():
    theta_pan = head_listener().position[0]
    theta_tilt = head_listener().position[1]
    torso_height = linearAct_listener().position[0]
    op_xyz = op_wrist_listener().point
    odom = odom_listener()
    wrist_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt, odom)
    op_wrist_point = Point()
    op_wrist_point.x = wrist_point[0]
    op_wrist_point.y = wrist_point[1]
    op_wrist_point.z = wrist_point[2]
    wrist_right_op_pub.publish(op_wrist_point)
    return wrist_point
    
    
            
if __name__ == '__main__':
    left_arm_ik_initial(0.8, 0.35, 0.75)
    # print(robot_state)
    # left_arm_ik_initial(0.8, 0.75, 0.75)
    # print(robot_state)
    # left_arm_ik_initial(0.8, 0.35, 1.25)
    # print(robot_state)
    # left_arm_ik_initial(0.8, 0.75, 1.25)
    # print(robot_state)
    
    
    while(True):
        wrist_point = wrist_op_transform_to_odom()
        left_arm_ik(wrist_point[0], wrist_point[1], wrist_point[2])
        
        
