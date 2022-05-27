#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Point
    
if __name__ == '__main__':
    rospy.init_node('offset_publisher')
    offset_pub = rospy.Publisher("/mrn_movo/offset", Point, queue_size=1, latch=True)
    offset = Point()
    offset.x = 0.25
    offset.y = 0.25
    offset.z = 0
    # while not rospy.is_shutdown():
    offset_pub.publish(offset)
    rospy.spin()