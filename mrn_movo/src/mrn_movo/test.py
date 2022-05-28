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
import message_filters
import math

def body_lengths(chest, wrist_right, elbow_right, shoulder_right):
    chest = [chest.point.x, chest.point.y, chest.point.z]
    wrist_right =       [wrist_right.point.x, wrist_right.point.y, wrist_right.point.z]
    # wrist_left =    [wrist_left.point.x,  wrist_left.point.y,  wrist_left.point.z]
    elbow_right =       [elbow_right.point.x, elbow_right.point.y, elbow_right.point.z]
    # elbow_left =    [elbow_left.point.x,  elbow_left.point.y,  elbow_left.point.z]
    shoulder_right =    [shoulder_right.point.x, shoulder_right.point.y, shoulder_right.point.z]
    # shoulder_left =    [shoulder_left.point.x,  shoulder_left.point.y,  shoulder_left.point.z]
    
    # shoulder_width =                    math.dist(shoulder_left, shoulder_right)
    chest_to_right_shoulder =           math.dist(chest, shoulder_right)
    right_shoulder_to_right_elbow =     math.dist(shoulder_right, elbow_right)
    right_elbow_to_right_wrist =        math.dist(elbow_right, wrist_right)
    arm_length =                        right_shoulder_to_right_elbow + right_elbow_to_right_wrist
    
    # print(shoulder_width)
    print("Chest to Shoulder: %s"%chest_to_right_shoulder)
    print("Shoulder to elbow: %s"%right_shoulder_to_right_elbow)
    print("Elbow to wrist: %s"%right_elbow_to_right_wrist)
    print("Arm Length: %s"%arm_length)
    

if __name__=="__main__":
    rospy.init_node("body_measurement")
    print("start")
    chest_pos_sub =           message_filters.Subscriber("/mrn_vision/openpose/movo/chest", PointStamped)
    wrist_right_pos_sub =     message_filters.Subscriber("/mrn_vision/openpose/movo/wrist_right", PointStamped)
    wrist_left_pos_sub =      message_filters.Subscriber("/mrn_vision/openpose/movo/wrist_left", PointStamped)
    elbow_right_pos_sub =     message_filters.Subscriber("/mrn_vision/openpose/movo/elbow_right", PointStamped)
    elbow_left_pos_sub =      message_filters.Subscriber("/mrn_vision/openpose/movo/elbow_left", PointStamped)
    shoulder_left_pos_sub =   message_filters.Subscriber("/mrn_vision/openpose/movo/shoulder_left", PointStamped)
    shoulder_right_pos_sub =  message_filters.Subscriber("/mrn_vision/openpose/movo/shoulder_right", PointStamped)
    print("subscribed")
    ts = message_filters.ApproximateTimeSynchronizer([chest_pos_sub, wrist_right_pos_sub,elbow_right_pos_sub, shoulder_right_pos_sub, ], 50, 0.1)    
    ts.registerCallback(body_lengths)
    
    rospy.spin()