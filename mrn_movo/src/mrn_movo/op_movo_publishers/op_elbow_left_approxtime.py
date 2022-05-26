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

def left_elbow_op_transform(left_elbow_pos, head_joints, linearAct_joints):
    # print(left_elbow_pos)
    theta_pan = head_joints.position[0]
    theta_tilt = head_joints.position[1]
    torso_height = linearAct_joints.position[0]
    op_xyz = left_elbow_pos.point
    left_elbow_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_left_elbow_point = PointStamped()
    op_left_elbow_point.point.x = left_elbow_point[0]
    op_left_elbow_point.point.y = left_elbow_point[1]
    op_left_elbow_point.point.z = left_elbow_point[2]
    op_left_elbow_point.header.stamp = rospy.Time.now()
    op_left_elbow_point.header.frame_id = "base_link"
    left_elbow_op_pub.publish(op_left_elbow_point)
    return left_elbow_point  
    
            
if __name__ == '__main__':
    rospy.init_node('op_movo_left_elbow', anonymous=True)

    # # Publish Transformed OpenPose Keypoints
    left_elbow_op_pub =     rospy.Publisher('mrn_vision/openpose/movo/left_elbow', PointStamped, queue_size=1)
    left_elbow_pos_sub =    message_filters.Subscriber("/mrn_vision/openpose/body/elbow_left", PointStamped)
    head_joints_sub =       message_filters.Subscriber('/movo/head/joint_states', JointState)
    linearAct_joints_sub =  message_filters.Subscriber('/movo/linear_actuator/joint_states', JointState)
    
    ts = message_filters.ApproximateTimeSynchronizer([left_elbow_pos_sub, head_joints_sub, linearAct_joints_sub], 10, 0.1)    
    ts.registerCallback(left_elbow_op_transform)
    
    rospy.spin()