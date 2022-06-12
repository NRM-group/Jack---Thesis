# Kinova MOVO Reachable Workspace Assessment Repository

Thesis Project by Jack Cameron McNamara

Student Number: 45321377

Project Commencement: July 2021

# Project Title

3D Reachable Workspace Assessment Via Robotic Instruction

# Project Description

The project aims to assess the 3D reachable workspace of a stroke patient through robotic instruction and computer vision.

# Installation

## Prerequisites

* Ubuntu 20.04 LTS (Required)
* ROS Noetic (Required)
* Build and install [OpenCV](https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html) from source
* Install [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) and [cuDDNN](https://developer.nvidia.com/rdp/cudnn-download)
* Install [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose#installation) from source

## Installation

Create and anter a catkin workspace
```
mkdir ~/catkin_ws && cd ~/catkin_ws
```
Create a source directory within catkin workspace
```
mkdir ./src && src ./src
```
Clone this repository
```
git clone https://github.com/jackmcnamarauq/thesis.git
```
Enter root of catkin workspace and run catkin_make
```
cd ~/catkin_ws
catkin_make
```
Install [Bio_IK](https://github.com/TAMS-Group/bio_ik) and [Bio_IK_Service](https://github.com/TAMS-Group/bio_ik_service)

Follow the [Kinova steps](https://github.com/Kinovarobotics/kinova-movo/wiki/2.-How-Tos#establish-communication-between-remote-development-pc-and-movo) for establishing communication between a remote development PC and MOVO

## Running the protocol

Open three terminals

Terminal 1:

SSH into the MOVO2 compute and launch the workspace_assessment file

```
ssh movo@movo2
roslaunch mrn_movo workspace_assessment 
```

Terminal 2:

Set the ROS_MASTER_URI to MOVO2 and launch the movo_moveit_config demo

```
cd ~/catkin_ws
source ./devel/setup.bash
export ROS_MASTER_URI=http://MOVO2:11311
roslaunch movo_moveit_config demo.launch
```
Terminal 3:

Set the ROS_MASTER_URI to MOVO2 and launch the mrn_movo.launch file

```
cd ~/catkin_ws
source ./devel/setup.bash
export ROS_MASTER_URI=http://MOVO2:11311
roslaunch mrn_movo mrn_movo.launch
```

