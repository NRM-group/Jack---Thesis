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

rospy.init_node("bio_ik_movo")

rospy.wait_for_service("/bio_ik/get_bio_ik")
get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)
pub = rospy.Publisher('/mrn_movo/left_arm/IK', JointState, queue_size=1)

def left_arm_ik_initial(x, y, z):

    request = bio_ik_msgs.msg.IKRequest()

    request.group_name = "whole_body"

    request.timeout.secs = 1

    request.approximate = True
    
    # request.RobotState = 

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
    print('Joint Angles: ' + np.array2string(left_arm_joint_angles_deg, separator=', '))
    print(response.solution.joint_state.position[0])
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
    # # rospy.spin()
    
def left_arm_ik(x, y, z):
    
    request = bio_ik_msgs.msg.IKRequest()

    request.group_name = "whole_body"

    request.timeout.secs = 1

    request.approximate = True
    
    # request.RobotState = 

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
    print('Joint Angles: ' + np.array2string(left_arm_joint_angles_deg, separator=', '))
    print(response.solution.joint_state.position[0])
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
    # # rospy.spin()

if __name__ == '__main__':
    print('Postion 1:', 0.8, 0.3, 1)
    left_arm_ik(0.8, 0.5, 1)
    
