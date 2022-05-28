#!/usr/bin/env python3

from __future__ import print_function
import re

import rospy
from mrn_movo.srv import KinovaMoveService
from mrn_movo.msg import KinovaMoveResponse
from geometry_msgs.msg import Point, PointStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64, Bool
from nav_msgs.msg import Odometry

def send_movement_client(chest_position, offset, odometry):
    rospy.wait_for_service("send_movement")
    try:
        send_movement = rospy.ServiceProxy("send_movement", KinovaMoveService)
        resp1 = send_movement(chest_position, offset, odometry)
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        
if __name__ == "__main__":
    chest_position = PointStamped()
    chest_position.point.x = 0.8
    chest_position.point.y = 0
    chest_position.point.z = 0.8
    
    offset = Point()
    offset.x = -0.25
    offset.y = 0.25
    offset.z = 0
    
    odometry = Odometry()
    odometry.pose.pose.position.x = 0
    odometry.pose.pose.position.y = 0
    odometry.pose.pose.position.z = 0
    
    print(send_movement_client(chest_position, offset, odometry))