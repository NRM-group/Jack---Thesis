#!/usr/bin/python3

import numpy as np
from math import *     
import rospy        

def TransformMatrix(input):
    x_r = input[0]
    y_r = input[1]
    z_r = input[2]
    y = input[3]
    b = input[4]
    a = input[5]
    transMat = np.array([[cos(a)*cos(b), cos(a)*sin(b)*sin(y)-sin(a)*cos(y), cos(a)*sin(b)*cos(y)+sin(a)*sin(y), x_r],
                         [sin(a)*cos(b), sin(a)*sin(b)*sin(y)+cos(a)*cos(y), sin(a)*sin(b)*cos(y)-cos(a)*sin(y), y_r],
                         [      -sin(b),                      cos(b)*sin(y),                      cos(b)*cos(y), z_r],
                         [            0,                                  0,                                  0,   1]])
    return transMat

def T_base_kinect(torso_height, theta_pan, theta_tilt, odom):
    base_link =                     np.array([0, 0, 0, 0, 0, 0])
    base_chassis_link =             np.array([0, 0, 0.0762, 0, 0, 0])
    linear_actuator_fixed_link =    np.array([0, 0, 0, 0, 0, 0])
    linear_actuator_link =          np.array([0.07714, 0, 0.39397+torso_height, 0, 0, 0])
    pan_base_link =                 np.array([0.19735, 0, 0.34499, 0, 0, 0])
    pan_link =                      np.array([0, 0, 0.05525, np.pi, 0, -theta_pan])
    if theta_tilt > 0:
        tilt_link =                 np.array([0, 0.026, -0.09075, np.pi/2, np.pi/2-theta_tilt, np.pi])
    elif theta_tilt < 0:
        tilt_link =                 np.array([0, 0.026, -0.09075, -np.pi/2, np.pi/2+theta_tilt, 0])
    else:
        tilt_link =                 np.array([0, 0.026, -0.09075, -np.pi/2, np.pi/2, 0])
    kinect2_link =                  np.array([0.05825, -0.010588, -0.026, -np.pi/2, 0, -np.pi/2])                    
    kinect2_ir_link =               np.array([0.0245, -0.03325, 0.04201, 0, 0, 0])                    
    kinect2_ir_optical_frame =      np.array([0, 0, 0, -np.pi/2, 0, -np.pi/2])                    
    kinect2_rgb_link =              np.array([0, -0.06175, 0, 0, 0, 0])                    
    kinect2_rgb_optical_frame =     np.array([0, 0, 0, -np.pi/2, 0, -np.pi/2]) 

    odom_rot =                      q_to_R(odom.orientation)
    T_odom =                        rot_to_T(odom_rot, odom.position)
    T_base_link =                   TransformMatrix(base_link)
    T_base_chassis_link =           TransformMatrix(base_chassis_link)
    T_linear_actuator_fixed_link =  TransformMatrix(linear_actuator_fixed_link)
    T_linear_actuator_link =        TransformMatrix(linear_actuator_link)
    T_pan_base_link =               TransformMatrix(pan_base_link)
    T_pan_link =                    TransformMatrix(pan_link)
    T_tilt_link =                   TransformMatrix(tilt_link)
    T_kinect2_link =                TransformMatrix(kinect2_link)
    T_kinect2_ir_link =             TransformMatrix(kinect2_ir_link)
    T_kinect2_ir_optical_frame =    TransformMatrix(kinect2_ir_optical_frame)
    T_kinect2_rgb_link =            TransformMatrix(kinect2_rgb_link)
    T_kinect2_rgb_optical_frame =   TransformMatrix(kinect2_rgb_optical_frame)

    # worldToRGBFrame = T_odom@T_base_link@T_base_chassis_link@T_linear_actuator_fixed_link@T_linear_actuator_link@T_pan_base_link@T_pan_link@T_tilt_link@T_kinect2_link@T_kinect2_ir_link@T_kinect2_rgb_link@T_kinect2_rgb_optical_frame
    # worldToIRFrame = T_odom@T_base_link@T_base_chassis_link@T_linear_actuator_fixed_link@T_linear_actuator_link@T_pan_base_link@T_pan_link@T_tilt_link@T_kinect2_link@T_kinect2_ir_link@T_kinect2_ir_optical_frame
    worldToIRFrame = T_base_link@T_base_chassis_link@T_linear_actuator_fixed_link@T_linear_actuator_link@T_pan_base_link@T_pan_link@T_tilt_link@T_kinect2_link@T_kinect2_ir_link@T_kinect2_ir_optical_frame
    return(worldToIRFrame)

def transform_from_csv(torso_height, theta_pan, theta_tilt):
    my_data = np.genfromtxt(r'/home/medrobotics/jack_ws/src/movo_scripts/data_20220510.csv', delimiter=',')
    x = my_data[:,0]
    y = my_data[:,1]
    z = my_data[:,2]

    output = []
    for i in range(1, np.size(x)):
        pose = np.array([[x[i]],
                        [y[i]],
                        [z[i]],
                        [1]])
        transformed = T_base_kinect(torso_height, theta_pan, theta_tilt)@pose
        t = np.transpose(transformed[0:3])
        output.append(t)
        
    output = np.array(output)
    np.savetxt("data_transformed.csv", output[:,0,:], delimiter=",", fmt='%10.5f')
    
def transformFromPoint(point, torso_height, theta_pan, theta_tilt, odom):
    x = point.x
    y = point.y
    z = point.z
    
    pose = np.array([[x],
                    [y],
                    [z],
                    [1]])
    # print(odom)
    transformed = T_base_kinect(torso_height, theta_pan, theta_tilt, odom)@pose
    # output = np.transpose(transformed[0:3])
    output = transformed[0:3]
    return output
    
def q_to_R(orientation):
    w = orientation.w
    x = orientation.x
    y = orientation.y
    z = orientation.z
    
    rot = np.array([[1-2*(y**2+z**2),       2*(x*y-z*w),     2*(x*y+y*w)],
                    [    2*(x*y+z*w), 1-2*(x**2 + z**2),     2*(y*z-x*w)],
                    [    2*(x*z-y*w),       2*(y*z+x*w), 1-2*(x**2+y**2)]])
    return rot

def rot_to_T(rot, p):
    T = np.array([[rot[0,0], rot[0,1], rot[0,2], p.x],
                  [rot[1,0], rot[1,1], rot[1,2], p.y],
                  [rot[2,0], rot[2,1], rot[2,2], p.z],
                         [0,        0,        0,    1]])
    return T    
    
if __name__ == '__main__':
    rot_to_T(q_to_R(1,0,0,0), [1,2,3])
