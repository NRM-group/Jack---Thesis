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
import numpy as np

import gtts
from playsound import playsound

if __name__=="__main__":
    a = np.array([[True],
                  [True],
                  [False],
                  [False]])
    
    b = np.array([[True],
                  [False],
                  [True],
                  [False]])
    
    print(np.logical_and(a,b))