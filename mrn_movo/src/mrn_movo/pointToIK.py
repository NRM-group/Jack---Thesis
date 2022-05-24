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



rospy.init_node('mrn_movo_openpose_to_ik', anonymous=True)
rospy.wait_for_service("/bio_ik/get_bio_ik")
get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)

# Publish Positions to Move To
left_arm_ik_pub = rospy.Publisher('/mrn_movo/left_arm/IK_move_to', JointState, queue_size=1, latch=True)

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
    global robot_state
    robot_state = response.solution      
    
            
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
        wrist_point = rospy.wait_for_message('/mrn_movo/left_arm/move_to', Point)
        left_arm_ik(wrist_point.x, wrist_point.y, wrist_point.z)
        
        
