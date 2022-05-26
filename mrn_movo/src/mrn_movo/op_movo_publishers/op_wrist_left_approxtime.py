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

def wrist_left_op_transform(wrist_left_pos, head_joints, linearAct_joints):
    # print(wrist_left_pos)
    theta_pan = head_joints.position[0]
    theta_tilt = head_joints.position[1]
    torso_height = linearAct_joints.position[0]
    op_xyz = wrist_left_pos.point
    wrist_left_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_wrist_left_point = PointStamped()
    op_wrist_left_point.point.x = wrist_left_point[0]
    op_wrist_left_point.point.y = wrist_left_point[1]
    op_wrist_left_point.point.z = wrist_left_point[2]
    op_wrist_left_point.header.stamp = rospy.Time.now()
    op_wrist_left_point.header.frame_id = "base_link"
    wrist_left_op_pub.publish(op_wrist_left_point)
    return wrist_left_point  
    
            
if __name__ == '__main__':
    rospy.init_node('op_movo_wrist_left', anonymous=True)

    # # Publish Transformed OpenPose Keypoints
    wrist_left_op_pub = rospy.Publisher('mrn_vision/openpose/movo/wrist_left', PointStamped, queue_size=1)
    wrist_left_pos_sub =         message_filters.Subscriber("/mrn_vision/openpose/body/wrist_left", PointStamped)
    head_joints_sub =       message_filters.Subscriber('/movo/head/joint_states', JointState)
    linearAct_joints_sub =  message_filters.Subscriber('/movo/linear_actuator/joint_states', JointState)
    
    ts = message_filters.ApproximateTimeSynchronizer([wrist_left_pos_sub, head_joints_sub, linearAct_joints_sub], 10, 0.1)    
    ts.registerCallback(wrist_left_op_transform)
    
    rospy.spin()