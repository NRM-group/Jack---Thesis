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
import csv
import time
import numpy as np

def write_to_csv(chest, wrist_left, wrist_right, elbow_left, elbow_right, shoulder_left, shoulder_right):   
    t = time.time()
    wrist_right =       [wrist_right.point.x, wrist_right.point.y, wrist_right.point.z]
    wrist_left =        [wrist_left.point.x, wrist_left.point.y, wrist_left.point.z]
    elbow_right =       [elbow_right.point.x, elbow_right.point.y, elbow_right.point.z]
    elbow_left =        [elbow_left.point.x, elbow_left.point.y, elbow_left.point.z]
    shoulder_right =    [shoulder_right.point.x, shoulder_right.point.y, shoulder_right.point.z]
    shoulder_left =     [shoulder_left.point.x, shoulder_left.point.y, shoulder_left.point.z]
    chest =             [chest.point.x, chest.point.y, chest.point.z]
    
    keypoints = np.hstack((chest, shoulder_right, elbow_right, wrist_right, shoulder_left, elbow_left, wrist_left, t))
    keypoints = np.reshape(keypoints, (1,22))
    print(keypoints)
    
    global values
    values = np.append(values, keypoints, axis=0)
    
    

if __name__== '__main__':
    rospy.init_node('openpose_writetocsv')
    chest_pos_sub =             message_filters.Subscriber("/mrn_vision/openpose/movo/chest", PointStamped)
    wrist_left_pos_sub =        message_filters.Subscriber("/mrn_vision/openpose/movo/wrist_left", PointStamped)
    wrist_right_pos_sub =       message_filters.Subscriber("/mrn_vision/openpose/movo/wrist_right", PointStamped)
    elbow_left_pos_sub =        message_filters.Subscriber("/mrn_vision/openpose/movo/elbow_left", PointStamped)
    elbow_right_pos_sub =       message_filters.Subscriber("/mrn_vision/openpose/movo/elbow_right", PointStamped)
    shoulder_left_pos_sub =     message_filters.Subscriber("/mrn_vision/openpose/movo/shoulder_left", PointStamped)
    shoulder_right_pos_sub =    message_filters.Subscriber("/mrn_vision/openpose/movo/shoulder_right", PointStamped)
    
    global values
    values = np.empty([1,22])
    
    ts = message_filters.ApproximateTimeSynchronizer([chest_pos_sub, wrist_left_pos_sub, wrist_right_pos_sub, elbow_left_pos_sub, elbow_right_pos_sub, shoulder_left_pos_sub, shoulder_right_pos_sub], 10, 0.2)    
    ts.registerCallback(write_to_csv)
    rospy.spin()
    
    np.savetxt('/home/medrobotics/jack_ws/src/mrn_movo/data/test_jack_2.csv', values, delimiter=',')