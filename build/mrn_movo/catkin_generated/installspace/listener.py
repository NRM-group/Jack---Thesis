#!/usr/bin/env python3
from requests import head
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState, Image
from geometry_msgs.msg import PointStamped
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
import trajectory_msgs.msg
import message_filters
import cv2 as cv
import time
import numpy as np  
from baseToKinect import transformFromPoint



rospy.init_node('mrn_movo', anonymous=True)
pub = rospy.Publisher('/mrn_movo/left_arm/IK', JointState, queue_size=1)
rospy.wait_for_service("/bio_ik/get_bio_ik")
get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)
    
def left_arm_ik(x, y, z):
    
    request = bio_ik_msgs.msg.IKRequest()

    request.group_name = "left_side"

    request.timeout.secs = 1

    request.approximate = True

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
    left_arm_joint_angles = response.solution.joint_state.position[1:7]
    left_arm_joint_angles_deg = np.around(np.degrees(left_arm_joint_angles), decimals=0)
    print(response.solution.joint_state)
    pub.publish(response.solution.joint_state)
    
    # display = moveit_msgs.msg.DisplayTrajectory()
    # display.trajectory_start = response.solution
    # display.trajectory.append(moveit_msgs.msg.RobotTrajectory())
    # display.trajectory[0].joint_trajectory.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
    # display.trajectory[0].joint_trajectory.points[-1].time_from_start.secs = 0
    # display.trajectory[0].joint_trajectory.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
    # display.trajectory[0].joint_trajectory.points[-1].time_from_start.secs = 1
    # display_publisher = rospy.Publisher("/move_group/display_planned_path", moveit_msgs.msg.DisplayTrajectory, latch=True, queue_size=10)
    # display_publisher.publish(display)
    
    # rospy.spin()

def ik_listener(x,y,z):
    left_arm_ik(x, y, z)
    ik_joints = rospy.wait_for_message("/mrn_movo/left_arm/IK", JointState) 
    return ik_joints
    
def op_listener():
    wrist_pos = rospy.wait_for_message("/mrn_vision/openpose/body/wrist", PointStamped)
    return wrist_pos


            
if __name__ == '__main__':

    print(op_listener())
    print(transformFromPoint(op_listener().point, 0, 0, 0))
    
