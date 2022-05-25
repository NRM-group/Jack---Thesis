#!/usr/bin/env python3

from __future__ import print_function
import re

from mrn_movo.srv import Get_IK
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState

import rospy

def left_arm_ik(req):
    print("Requesting IK Solution for Position [%s, %s, %s]"%(req.point.x, req.point.y, req.point.z))
    request = bio_ik_msgs.msg.IKRequest()
    request.group_name = "left_side"
    request.timeout.secs = 1
    request.approximate = True
    request.robot_state = rospy.wait_for_message('/mrn_movo/left_arm/state', moveit_msgs.msg.RobotState)
    request.pose_goals.append(bio_ik_msgs.msg.PoseGoal())
    request.pose_goals[-1].link_name = "left_gripper_base_link"
    request.pose_goals[-1].pose.position.x = req.point.x
    request.pose_goals[-1].pose.position.y = req.point.y
    request.pose_goals[-1].pose.position.z = req.point.z
    request.pose_goals[-1].pose.orientation.x = 0.0
    request.pose_goals[-1].pose.orientation.y = -0.707
    request.pose_goals[-1].pose.orientation.z = 0.0
    request.pose_goals[-1].pose.orientation.w = 0.707
    print("Request Ready")
    response = get_bio_ik(request).ik_response
    pub.publish(response.solution)
    return response.solution.joint_state

def left_arm_ik_initial():
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
    # print(response)
    pub.publish(response.solution)
            
def left_arm_ik_server():
    rospy.init_node('left_arm_ik_server')
    left_arm_ik_initial()
    s = rospy.Service('left_arm_ik', Get_IK, left_arm_ik)
    print("Ready to get provide IK Solution")
    rospy.spin()

if __name__=="__main__":
    rospy.wait_for_service("/bio_ik/get_bio_ik")
    print("Connected to Bio_IK Service")
    get_bio_ik = rospy.ServiceProxy("/bio_ik/get_bio_ik", bio_ik_msgs.srv.GetIK)
    pub = rospy.Publisher('/mrn_movo/left_arm/state', moveit_msgs.msg.RobotState, queue_size=1, latch=True)
    print("Executing Left Arm IK Server")
    left_arm_ik_server()
    
    