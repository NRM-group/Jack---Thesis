#!/usr/bin/env python3

import rospy
import smach
import numpy as np
import math
from geometry_msgs.msg import Point, PointStamped
from std_msgs.msg import Bool
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
import gtts
from playsound import playsound
import time
from mrn_movo.send_movement_client import send_movement_client


class Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['begin'],
                             input_keys=['offset', 'num'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Starting Test')
        
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
        
        return 'begin'

class MoveArmToOffset(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['Offset Changed', 'all points tested'],
                             input_keys=['offset', 'num'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Move Arm to Offset')
        
        offset_point = Point()
        offset_point.x = userdata.offset[userdata.num, 0]
        offset_point.y = userdata.offset[userdata.num, 1]
        offset_point.z = userdata.offset[userdata.num, 2]
        
        chest_position =    rospy.wait_for_message("mrn_vision/openpose/movo/chest", PointStamped)
        
        odometry =          rospy.wait_for_message("/movo/odometry/local_filtered", Odometry)
        
        if userdata.num < 10:
            response = send_movement_client(chest_position, offset_point, odometry)
            head_look_pub.publish(response.response.head_look)
            ik_pub.publish(response.response.ik_joint_state)
            if response.response.base_move.x != 0:
                base_move.publish(response.response.base_move)
                rospy.wait_for_message("/mrn_movo/base_movement_finished", Bool)
            else:
                rospy.wait_for_message("/mrn_movo/arm_movement_finished", Bool)
            return 'Offset Changed'
        else:
            return 'all points tested'

class MoveArmToAdjustedOffset(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['Offset Changed', 'all points tested'],
                             input_keys=['adjusted_offset', 'num'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Move Arm to Offset')
        
        offset_point = Point()
        offset_point.x = userdata.offset[userdata.num, 0]
        offset_point.y = userdata.offset[userdata.num, 1]
        offset_point.z = userdata.offset[userdata.num, 2]
        
        chest_position =    rospy.wait_for_message("mrn_vision/openpose/movo/chest", PointStamped)
        
        odometry =          rospy.wait_for_message("/movo/odometry/local_filtered", Odometry)
        
        if userdata.num < 10:
            response = send_movement_client(chest_position, offset_point, odometry)
            head_look_pub.publish(response.response.head_look)
            ik_pub.publish(response.response.ik_joint_state)
            if response.response.base_move.x != 0:
                base_move.publish(response.response.base_move)
                rospy.wait_for_message("/mrn_movo/base_movement_finished", Bool)
            else:
                rospy.wait_for_message("/mrn_movo/arm_movement_finished", Bool)
            return 'Offset Changed'
        else:
            return 'all points tested'

class TestOP(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['true', 'false'],
                             input_keys=['offset', 'num'],
                             output_keys=['num', 'offset'])
        
    def execute(self, userdata):
        rospy.loginfo("Testing OP Position at Offset [%s, %s, %s]"%(userdata.offset[userdata.num, 0],userdata.offset[userdata.num, 1],userdata.offset[userdata.num, 2]))
        tts = gtts.gTTS("Please touch my hand")
        tts.save("touchmyhand.mp3")
        playsound("touchmyhand.mp3")
        time.sleep(3)
        wrist_location = rospy.wait_for_message("mrn_vision/openpose/movo/wrist_right", PointStamped)
        wrist_location = wrist_location.point
        chest_location = rospy.wait_for_message("mrn_vision/openpose/movo/chest", PointStamped)
        chest_location = chest_location.point
        offset_point = Point()
        offset_point.x = userdata.offset[userdata.num, 0] + chest_location.x
        offset_point.y = userdata.offset[userdata.num, 1] + chest_location.y
        offset_point.z = userdata.offset[userdata.num, 2] + chest_location.z
        euc_dist = math.sqrt((offset_point.x-wrist_location.x)**2 + (offset_point.y-wrist_location.y)**2 + (offset_point.z-wrist_location.z)**2)
        
        if euc_dist < 0.25:
            tts = gtts.gTTS("Good job")
            tts.save("goodjob.mp3")
            playsound("goodjob.mp3")
            userdata.num += 1
            return 'true'
        else:
            userdata.offset[userdata.num, 0].x = (offset_point.x + wrist_location.x)/2 - chest_location.x
            userdata.offset[userdata.num, 1].y = (offset_point.y + wrist_location.y)/2 - chest_location.y
            userdata.offset[userdata.num, 2].z = (offset_point.z + wrist_location.z)/2 - chest_location.z
            tts = gtts.gTTS("Wait to try again")
            tts.save("tryagain.mp3")
            playsound("tryagain.mp3")
            return 'false'
        
class Finish(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['finish'])

    def execute(self, userdata):
        rospy.loginfo('Test Finished')
        return 'finish'

if __name__ == '__main__':
    
    rospy.init_node('mrn_movo_state_machine', anonymous=True)
    
    # offset_pub = rospy.Publisher("/mrn_movo/offset", Point, queue_size=1, latch=True)
    ik_pub = rospy.Publisher('/mrn_movo/left_arm/state', JointState, queue_size=1, latch=True)
    base_move = rospy.Publisher('/mrn_movo/base/move', Point, queue_size=1)
    head_look_pub = rospy.Publisher('/mrn_movo/head/look_at', PointStamped, queue_size=1, latch=True)
    # Create a SMACH state machine
    sm_workspace = smach.StateMachine(outcomes=['finish'])
    
    # User Data
    sm_workspace.userdata.num = 0
    sm_workspace.userdata.offset = np.array([[-0.25, 0.25, 0],
                                             [-0.25, 0.55, 0],
                                             [-0.25, 0.25, 0.4],
                                             [-0.25, 0.55, 0.4],
                                             [-0.45, 0.35, 0.2],
                                             [-0.65, 0.25, 0],
                                             [-0.65, 0.55, 0],
                                             [-0.65, 0.25, 0.4],
                                             [-0.65, 0.55, 0.4]])
    
    # Open the container
    with sm_workspace:
        
        # Start State
        smach.StateMachine.add('Start', Start(), 
                               transitions={'begin':'Move Arm To Offset'})
            
        # Move Arm to Initial Measurement Point P
        smach.StateMachine.add('Move Arm To Offset', MoveArmToOffset(), 
                            transitions={'Offset Changed':'OP Test',
                                         'all points tested':'Finish'})
        
        smach.StateMachine.add('OP Test', TestOP(),
                               transitions={'true':'Move Arm To Offset',
                                            'false':'Move Arm To Offset'})
            
        # Finish
        smach.StateMachine.add('Finish', Finish())


    # sis = smach_ros.IntrospectionServer('server_name', sm_workspace, '/Point_Test')
    # sis.start()
    # Execute SMACH plan
    outcome = sm_workspace.execute()
    rospy.spin()
    # sis.stop()