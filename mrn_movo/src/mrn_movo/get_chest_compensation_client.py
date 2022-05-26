#!/usr/bin/env python3

from __future__ import print_function

from requests import request

from mrn_movo.srv import Get_Chest_Compensation
from geometry_msgs.msg import Point
from std_msgs.msg import Float64
from mrn_movo.msg import ChestCompensationRequest

import rospy

def get_chest_compensation_client(request1):
    print("Connecting to Chest Compensation Server")
    rospy.wait_for_service('chest_compensation')
    print("Connected to Chest Compensation Server")
    try:
        get_chest_compensation = rospy.ServiceProxy('chest_compensation', Get_Chest_Compensation)
        resp1 = get_chest_compensation(request1)
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    
if __name__ == "__main__":
    request1 = ChestCompensationRequest()
    # request1.chest_position.x = 1.5
    # request1.chest_position.y = 0.4
    # request1.chest_position.z = 1
    request1.dist_chest.data = 1.2
    request1.threshold.data = 0.1
    print(request1)
    point = get_chest_compensation_client(request1)
    print(point)
    
    