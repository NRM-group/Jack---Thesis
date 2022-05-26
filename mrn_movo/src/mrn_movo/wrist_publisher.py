#!/usr/bin/env python3

from __future__ import print_function
import re

from mrn_movo.srv import Get_IK
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
from geometry_msgs.msg import Point, PointStamped
from sensor_msgs.msg import JointState
import trajectory_msgs.msg
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64

import rospy

def left_arm_ik(pointstamped):
    point = pointstamped.point
    
    # Test the distance from the Kinova's base_link frame origin and the OP_movo chest position
    dist_chest_x = 1.2                                      # Distance from base_link to chest x
    dist_chest_y = 0                                        # Distance from base_link to chest x
    delta_chest_x = point.x - dist_chest_x
    delta_chest_y = point.y - dist_chest_y
    
    odom = rospy.wait_for_message('/movo/odometry/local_filtered', Odometry).pose.pose.position
    
    delta_chest_adjusted = Point()
    delta_chest_adjusted.x  = delta_chest_x + odom.x
    delta_chest_adjusted.y  = delta_chest_y + odom.y
    
    threshold_x = 0.2                                       # Threshold for change in x chest compensation
    threshold_y = 0.2                                       # Threshold for change in y chest compensation
    
    # If delta_chest is less than the threshold, use the Kinova MOVO arms to compensate for the chest movement
    if abs(delta_chest_x) > threshold_x and abs(delta_chest_y) < threshold_y:
        delta_chest_adjusted = Point()
        delta_chest_adjusted.x  = delta_chest_x + odom.x
        delta_chest_adjusted.y  = 0
        base_move.publish(delta_chest_adjusted)
    elif abs(delta_chest_x) < threshold_x and abs(delta_chest_y) > threshold_y:
        delta_chest_adjusted = Point()
        delta_chest_adjusted.x  = 0
        delta_chest_adjusted.y  = delta_chest_y + odom.y
        base_move.publish(delta_chest_adjusted)        
    elif abs(delta_chest_x) > threshold_x and abs(delta_chest_y) > threshold_y:
        delta_chest_adjusted = Point()
        delta_chest_adjusted.x  = delta_chest_x + odom.x
        delta_chest_adjusted.y  = delta_chest_y + odom.y
        base_move.publish(delta_chest_adjusted)
    else:    
        point.x = point.x - 0.25
        point.y = point.y + 0.25
        
        # Filter any unexpected values
        if point.x > 0 and point.y > 0 and point.z > 0:
            # print(point)
            request = bio_ik_msgs.msg.IKRequest()
            request.group_name = "whole_body_left"
            request.timeout.secs = 1
            request.approximate = True
            global robot_state
            request.robot_state = robot_state
            request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
            request.pose_goals[-1].link_name = "left_gripper_finger1_finger_tip_link"
            request.pose_goals[-1].pose.position.x = point.x
            request.pose_goals[-1].pose.position.y = point.y
            request.pose_goals[-1].pose.position.z = point.z
            request.pose_goals[-1].pose.orientation.x = 0.5
            request.pose_goals[-1].pose.orientation.y = -0.5
            request.pose_goals[-1].pose.orientation.z = 0.5
            request.pose_goals[-1].pose.orientation.w = 0.5
            response = get_bio_ik(request).ik_response
            joint_state = response.solution.joint_state
            joint_state.header.stamp = rospy.Time.now()
            pub.publish(response.solution.joint_state)
            
            display = moveit_msgs.msg.DisplayTrajectory()
            display.trajectory_start = response.solution
            display.trajectory.append(moveit_msgs.msg.RobotTrajectory())
            display.trajectory[0].joint_trajectory.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
            display.trajectory[0].joint_trajectory.points[-1].time_from_start.secs = 0
            display.trajectory[0].joint_trajectory.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
            display.trajectory[0].joint_trajectory.points[-1].time_from_start.secs = 1
            display_publisher = rospy.Publisher("/move_group/display_planned_path", moveit_msgs.msg.DisplayTrajectory, latch=True, queue_size=10)
            display_publisher.publish(display)

def left_arm_ik_initial():
    request = bio_ik_msgs.msg.IKRequest()
    request.group_name = "whole_body_left"
    request.timeout.secs = 1
    request.approximate = True
    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_finger1_finger_tip_link"
    request.pose_goals[-1].pose.position.x = 0.8
    request.pose_goals[-1].pose.position.y = 0.4
    request.pose_goals[-1].pose.position.z = 1.0
    request.pose_goals[-1].pose.orientation.x = 0.5
    request.pose_goals[-1].pose.orientation.y = -0.5
    request.pose_goals[-1].pose.orientation.z = 0.5
    request.pose_goals[-1].pose.orientation.w = 0.5
    response = get_bio_ik(request).ik_response
    global robot_state
    robot_state = response.solution     
            

if __name__=="__main__":
    rospy.init_node('left_arm_ik_chest')
    rospy.wait_for_service("/bio_ik/get_bio_ik")
    get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)
    pub = rospy.Publisher('/mrn_movo/left_arm/state', JointState, queue_size=1, latch=True)
    base_move = rospy.Publisher('/mrn_movo/base/move', Point, queue_size=1)
    left_arm_ik_initial()
    rospy.Subscriber('/mrn_vision/openpose/movo/chest', PointStamped, left_arm_ik, queue_size=1)
    rospy.spin()
    
    
    