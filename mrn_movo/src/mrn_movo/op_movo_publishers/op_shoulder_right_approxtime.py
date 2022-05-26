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

def shoulder_right_op_transform(shoulder_right_pos, head_joints, linearAct_joints):
    # print(shoulder_right_pos)
    theta_pan = head_joints.position[0]
    theta_tilt = head_joints.position[1]
    torso_height = linearAct_joints.position[0]
    op_xyz = shoulder_right_pos.point
    shoulder_right_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_shoulder_right_point = PointStamped()
    op_shoulder_right_point.point.x = shoulder_right_point[0]
    op_shoulder_right_point.point.y = shoulder_right_point[1]
    op_shoulder_right_point.point.z = shoulder_right_point[2]
    op_shoulder_right_point.header.stamp = rospy.Time.now()
    op_shoulder_right_point.header.frame_id = "base_link"
    shoulder_right_op_pub.publish(op_shoulder_right_point)
    return shoulder_right_point  
    
            
if __name__ == '__main__':
    rospy.init_node('op_movo_shoulder_right', anonymous=True)

    # # Publish Transformed OpenPose Keypoints
    shoulder_right_op_pub =     rospy.Publisher('mrn_vision/openpose/movo/shoulder_right', PointStamped, queue_size=1)
    shoulder_right_pos_sub =    message_filters.Subscriber("/mrn_vision/openpose/body/shoulder_right", PointStamped)
    head_joints_sub =           message_filters.Subscriber('/movo/head/joint_states', JointState)
    linearAct_joints_sub =      message_filters.Subscriber('/movo/linear_actuator/joint_states', JointState)
    
    ts = message_filters.ApproximateTimeSynchronizer([shoulder_right_pos_sub, head_joints_sub, linearAct_joints_sub], 10, 0.1)    
    ts.registerCallback(shoulder_right_op_transform)
    
    rospy.spin()