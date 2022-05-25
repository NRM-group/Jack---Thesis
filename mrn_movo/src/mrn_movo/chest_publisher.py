#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState, Image
from geometry_msgs.msg import (
    PointStamped,
    Point
)
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from mrn_movo.baseToKinect import transformFromPoint



rospy.init_node('mrn_movo_op_chest', anonymous=True)

# Publish Positions to Move To
chest_move_pub = rospy.Publisher('/mrn_movo/base/move_to', Float64, queue_size=1, latch=True)

# Publish Transformed OpenPose Keypoints
chest_op_pub = rospy.Publisher('mrn_vision/openpose/movo/chest', Point, queue_size=1)

robot_state = None
    
def chest_adapt(movo_op_chest_x,y,z, dist_chest, threshold):
    delta_chest = movo_op_chest_x - dist_chest
    delta_chest_adjusted = delta_chest + odom_listener().position.x
    if abs(delta_chest) > threshold:
        chest_move_pub.publish(delta_chest_adjusted)
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

def chest_op_transform_to_odom():
    theta_pan = head_listener().position[0]
    theta_tilt = head_listener().position[1]
    torso_height = linearAct_listener().position[0]
    op_xyz = op_chest_listener().point
    chest_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_chest_point = Point()
    op_chest_point.x = chest_point[0]
    op_chest_point.y = chest_point[1]
    op_chest_point.z = chest_point[2]
    chest_op_pub.publish(op_chest_point)
    return chest_point  
    
            
if __name__ == '__main__':
    
    while(True):
        chest_point = chest_op_transform_to_odom()
        dist_chest = rospy.wait_for_message("/mrn_movo/chest_compensation/distance", Float64).data
        chest_adapt(chest_point[0], chest_point[1], chest_point[2], dist_chest, 0.2)     