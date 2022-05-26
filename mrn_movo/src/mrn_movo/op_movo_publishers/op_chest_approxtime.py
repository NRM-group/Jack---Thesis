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

def chest_op_transform(chest_pos, head_joints, linearAct_joints):
    # print(chest_pos)
    theta_pan = head_joints.position[0]
    theta_tilt = head_joints.position[1]
    torso_height = linearAct_joints.position[0]
    op_xyz = chest_pos.point
    chest_point = transformFromPoint(op_xyz, torso_height, theta_pan, theta_tilt)
    op_chest_point = PointStamped()
    op_chest_point.point.x = chest_point[0]
    op_chest_point.point.y = chest_point[1]
    op_chest_point.point.z = chest_point[2]
    op_chest_point.header.stamp = rospy.Time.now()
    op_chest_point.header.frame_id = "base_link"
    chest_op_pub.publish(op_chest_point)
    return chest_point  
    
            
if __name__ == '__main__':
    rospy.init_node('op_movo_chest', anonymous=True)

    # # Publish Transformed OpenPose Keypoints
    chest_op_pub =          rospy.Publisher('mrn_vision/openpose/movo/chest', PointStamped, queue_size=1)
    chest_pos_sub =         message_filters.Subscriber("/mrn_vision/openpose/body/chest", PointStamped)
    head_joints_sub =       message_filters.Subscriber('/movo/head/joint_states', JointState)
    linearAct_joints_sub =  message_filters.Subscriber('/movo/linear_actuator/joint_states', JointState)
    
    ts = message_filters.ApproximateTimeSynchronizer([chest_pos_sub, head_joints_sub, linearAct_joints_sub], 10, 0.1)    
    ts.registerCallback(chest_op_transform)
    
    rospy.spin()