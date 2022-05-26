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



rospy.init_node('mrn_movo_op_chest', anonymous=True)

# Publish Positions to Move To
chest_move_pub = rospy.Publisher('/mrn_movo/base/move_to', Float64, queue_size=1, latch=True)

robot_state = None
    
def chest_adapt(movo_op_chest_x,y,z, dist_chest, threshold):
    delta_chest = movo_op_chest_x - dist_chest
    delta_chest_adjusted = delta_chest + odom_listener().position.x
    if abs(delta_chest) > threshold:
        chest_move_pub.publish(delta_chest_adjusted)
    # return chest_move_to
    
            
if __name__ == '__main__':
    
    chest_adapt(chest_point[0], chest_point[1], chest_point[2], 1.2, 0.2)     