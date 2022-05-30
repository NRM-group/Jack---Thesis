#!/usr/bin/env python3

from __future__ import print_function
import re

from mrn_movo.srv import KinovaMoveService
from mrn_movo.msg import KinovaMoveResponse
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
from geometry_msgs.msg import Point, PointStamped
from sensor_msgs.msg import JointState
import trajectory_msgs.msg
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64, Bool
import time
import rospy
from moveit_msgs.msg import RobotState
import message_filters

def kinova_movo_service(req):
    time_now = rospy.Time.now()
    offset = req.offset.point
    point = req.chest_position.point
    odom = req.odometry.pose.pose.position
    dist_chest_x = 0.8 - offset.x                           # Distance from base_link to chest x
    delta_chest_x = point.x - dist_chest_x
    
    delta_chest_adjusted = Point()
    delta_chest_adjusted.x  = delta_chest_x + odom.x
    
    threshold_x = 0.2                                       # Threshold for change in x chest compensation
    
    base_move = Point()
    head_look_at = PointStamped()
    
    global robot_state
    joint_state = robot_state.joint_state
    
    head_look_at.point.x = point.x + offset.x
    head_look_at.point.y = point.y + offset.y
    head_look_at.point.z = point.z + offset.z
    head_look_at.header.stamp = time_now
    
    # If delta_chest is less than the threshold, use the Kinova MOVO arms to compensate for the chest movement
    if abs(delta_chest_x) > threshold_x:
        delta_chest_adjusted = Point()
        delta_chest_adjusted.x  = delta_chest_x + odom.x
        if abs(delta_chest_adjusted.x) < 0.5:
            # base_move.publish(delta_chest_adjusted)
            base_move.x = delta_chest_adjusted.x
            
    else:
        point.x = point.x + offset.x
        point.y = point.y + offset.y
        point.z = point.z + offset.z 
            
        # Filter any unexpected values
        if point.x > 0 and point.y > 0 and point.z > 0:
            # print(point)
            request = bio_ik_msgs.msg.IKRequest()
            request.group_name = "whole_body_left"
            request.timeout.secs = 1
            request.approximate = True
            request.robot_state = robot_state
            request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
            request.pose_goals[-1].link_name = "left_gripper_base_link"
            request.pose_goals[-1].pose.position.x = point.x
            request.pose_goals[-1].pose.position.y = point.y
            request.pose_goals[-1].pose.position.z = point.z
            request.pose_goals[-1].pose.orientation.x = 0.0
            request.pose_goals[-1].pose.orientation.y = -0.707
            request.pose_goals[-1].pose.orientation.z = 0.0
            request.pose_goals[-1].pose.orientation.w = 0.707
            response = get_bio_ik(request).ik_response
            print(response.solution_fitness)
            joint_state = response.solution.joint_state
            joint_state.header.stamp = time_now
            # pub.publish(response.solution.joint_state)
            
            display = moveit_msgs.msg.DisplayTrajectory()
            display.trajectory_start = response.solution
            display.trajectory.append(moveit_msgs.msg.RobotTrajectory())
            display.trajectory[0].joint_trajectory.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
            display.trajectory[0].joint_trajectory.points[-1].time_from_start.secs = 0
            display.trajectory[0].joint_trajectory.points.append(trajectory_msgs.msg.JointTrajectoryPoint())
            display.trajectory[0].joint_trajectory.points[-1].time_from_start.secs = 1
            display_publisher = rospy.Publisher("/move_group/display_planned_path", moveit_msgs.msg.DisplayTrajectory, latch=True, queue_size=10)
            display_publisher.publish(display)
            
            robot_state = response.solution
            
            
    KinovaMoveResponse.base_move = base_move
    KinovaMoveResponse.ik_joint_state = joint_state  
    KinovaMoveResponse.head_look = head_look_at            
    return KinovaMoveResponse
    

def left_arm_ik_initial():
    request = bio_ik_msgs.msg.IKRequest()
    request.group_name = "whole_body_left"
    request.timeout.secs = 1
    request.approximate = True
    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_base_link"
    request.pose_goals[-1].pose.position.x = 0.8
    request.pose_goals[-1].pose.position.y = 0.4
    request.pose_goals[-1].pose.position.z = 1.0
    request.pose_goals[-1].pose.orientation.x = 0.0
    request.pose_goals[-1].pose.orientation.y = -0.707
    request.pose_goals[-1].pose.orientation.z = 0.0
    request.pose_goals[-1].pose.orientation.w = 0.707
    response = get_bio_ik(request).ik_response
    global robot_state
    robot_state = response.solution               

def send_movement_server():
    rospy.init_node("send_movement_server")
    global robot_state
    robot_state = RobotState()
    left_arm_ik_initial()
    s = rospy.Service("send_movement", KinovaMoveService, kinova_movo_service)
    print("Ready to provide movement solutions")
    rospy.spin()
    
if __name__ == "__main__":
    rospy.wait_for_service("/bio_ik/get_bio_ik")
    get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)
    send_movement_server()