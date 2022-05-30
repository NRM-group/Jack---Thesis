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
import message_filters

def shoulder_left_op_transform(shoulder_left_pos, head_joints, linearAct_joints):
    print(shoulder_left_pos)
    theta_pan = head_joints.position[0]
    theta_tilt = head_joints.position[1]
    torso_height = linearAct_joints.position[0]
    op_xyz = shoulder_left_pos.point
    shoulder_left_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_shoulder_left_point = PointStamped()
    op_shoulder_left_point.point.x = shoulder_left_point[0]
    op_shoulder_left_point.point.y = shoulder_left_point[1]
    op_shoulder_left_point.point.z = shoulder_left_point[2]
    op_shoulder_left_point.header.stamp = rospy.Time.now()
    op_shoulder_left_point.header.frame_id = "base_link"
    shoulder_left_op_pub.publish(op_shoulder_left_point)
    return shoulder_left_point  
    
            
if __name__ == '__main__':
    rospy.init_node('op_movo_shoulder_left', anonymous=True)

    # # Publish Transformed OpenPose Keypoints
    shoulder_left_op_pub =      rospy.Publisher('/mrn_vision/openpose/movo/shoulder_left', PointStamped, queue_size=1)
    shoulder_left_pos_sub =     message_filters.Subscriber("/mrn_vision/openpose/body/shoulder_left", PointStamped)
    head_joints_sub =           message_filters.Subscriber('/movo/head/joint_states', JointState)
    linearAct_joints_sub =      message_filters.Subscriber('/movo/linear_actuator/joint_states', JointState)
    
    ts = message_filters.ApproximateTimeSynchronizer([shoulder_left_pos_sub, head_joints_sub, linearAct_joints_sub], 10, 0.1)    
    ts.registerCallback(shoulder_left_op_transform)
    
    rospy.spin()