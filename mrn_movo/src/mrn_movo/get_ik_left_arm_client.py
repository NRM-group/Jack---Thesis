#!/usr/bin/env python3

from __future__ import print_function

from mrn_movo.srv import Get_IK
import bio_ik_msgs
import bio_ik_msgs.msg
import bio_ik_msgs.srv
import moveit_msgs.msg
from geometry_msgs.msg import Point

import rospy

def get_ik_left_arm_client(point):
    print("Connecting to Left Arm IK Server")
    rospy.wait_for_service('left_arm_ik')
    print("Connected to Left Arm IK Server")
    try:
        get_ik_left_arm = rospy.ServiceProxy('left_arm_ik', Get_IK)
        resp1 = get_ik_left_arm(point)
        return resp1.joint_state
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    
if __name__ == "__main__":
    point = Point()
    point.x = 0.8
    point.y = 0.4
    point.z = 1
    print("Requesting IK for Point [%s, %s, %s]"%(point.x, point.y, point.z))
    point = get_ik_left_arm_client(point)
    print(point)
    
    