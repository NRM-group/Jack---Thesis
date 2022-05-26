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

def wrist_right_op_transform(wrist_right_pos, head_joints, linearAct_joints):
    # print(wrist_right_pos)
    theta_pan = head_joints.position[0]
    theta_tilt = head_joints.position[1]
    torso_height = linearAct_joints.position[0]
    op_xyz = wrist_right_pos.point
    wrist_right_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_wrist_right_point = PointStamped()
    op_wrist_right_point.point.x = wrist_right_point[0]
    op_wrist_right_point.point.y = wrist_right_point[1]
    op_wrist_right_point.point.z = wrist_right_point[2]
    op_wrist_right_point.header.stamp = rospy.Time.now()
    op_wrist_right_point.header.frame_id = "base_link"
    wrist_right_op_pub.publish(op_wrist_right_point)
    return wrist_right_point  
    
            
if __name__ == '__main__':
    rospy.init_node('op_movo_wrist_right', anonymous=True)

    # # Publish Transformed OpenPose Keypoints
    wrist_right_op_pub =    rospy.Publisher('mrn_vision/openpose/movo/wrist_right', PointStamped, queue_size=1)
    wrist_right_pos_sub =   message_filters.Subscriber("/mrn_vision/openpose/body/wrist_right", PointStamped)
    head_joints_sub =       message_filters.Subscriber('/movo/head/joint_states', JointState)
    linearAct_joints_sub =  message_filters.Subscriber('/movo/linear_actuator/joint_states', JointState)
    
    ts = message_filters.ApproximateTimeSynchronizer([wrist_right_pos_sub, head_joints_sub, linearAct_joints_sub], 10, 0.1)    
    ts.registerCallback(wrist_right_op_transform)
    
    rospy.spin()