#!/usr/bin/env python3

from platform import machine
from sklearn.metrics import euclidean_distances
import rospy
import time
from listener import left_arm_ik, left_arm_op_transform
from scipy.spatial import distance
from transitions import Machine
import smach
import smach_ros
import numpy as np

class start(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['start'])
        self.counter = 0
        
    def execute(self, userdata):
        try:
            input("Press enter to start")
        except SyntaxError:
            pass
        return 'start'
        
class move_arm_p1(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['arm_moving', 'arm_moved'])
        
    def execute(self, userdata):
        rospy.loginfo('Moving Arm to Box 1')
        start_time = time.time()
        left_arm_ik(points[0,:][0], points[0,:][1], points[0,:][2])
        if time.time() < start_time + 10:
            return 'arm_moving'
        else:
            return 'arm_moved'

class test_op(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['pass', 'fail'])
        self.counter = 0
        
    def execute(self, userdata):
        op_xyz = left_arm_op_transform()
        p1 = [1,1,1]
        rospy.loginfo('Testing OpenPose')
        if (distance.euclidean(p1, op_xyz) < 0.1):
            return 'pass'
        else:
            return 'fail'
        
class move_arm_op(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['arm_op_moved'])
        self.counter = 0
        
    def execute(self, userdata):
        op_xyz = left_arm_op_transform()
        left_arm_ik(op_xyz[0], op_xyz[1], op_xyz[2])
        rospy.loginfo('Moving Arm to OpenPose Location')
        return 'arm_op_moved'
                
def main():
    rospy.init_node('mrn_movo_state_machine')
    
    sm = smach.StateMachine(outcomes=['move_arm_op', 'finish'])
    
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('Start', start(), 
                               transitions={'start':'Move Arm'})
        smach.StateMachine.add('Move Arm', move_arm_p1(), 
                               transitions={'arm_moving':'Move Arm',
                                            'arm_moved':'Test OpenPose'})
        smach.StateMachine.add('Test OpenPose', test_op(), 
                               transitions={'fail':'move_arm_op',
                                            'pass':'finish'})
        smach.StateMachine.add('Move Arm To OpenPose', move_arm_op(), 
                               transitions={'arm_op_moved':'test_op'})

    points = np.array([[0.8, 0.4, 1],
                       [0.8, 0.8, 1],
                       [0.8, 0.4, 1.5],
                       [0.8, 0.8, 1.5]])
    # Execute SMACH plan
    outcome = sm.execute()
    
# p1 = [0.8, 0.3, 1]
# op_xyz = left_arm_op_transform()
# print(distance.euclidean(p1, op_xyz))

if __name__ == '__main__':
    main()