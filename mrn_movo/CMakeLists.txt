cmake_minimum_required(VERSION 3.0.2)
project(mrn_movo)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  geometry_msgs
  sensor_msgs
)

catkin_python_setup()

add_service_files(
  FILES
  Get_IK.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  sensor_msgs
)

catkin_package(
 INCLUDE_DIRS include
#  LIBRARIES mrn_movo
 CATKIN_DEPENDS roscpp rospy std_msgs sensor_msgs geometry_msgs message_runtime
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS 
  src/mrn_movo/wrist_publisher.py
  src/mrn_movo/chest_publisher.py
  src/mrn_movo/pointToIK.py
  src/mrn_movo/baseToKinect.py
  src/mrn_movo/get_bio_ik_movo.py
  src/mrn_movo/PointCloudVisualisation.py
  src/mrn_movo/state_machine.py
  src/mrn_movo/get_ik_left_arm_server.py
  src/mrn_movo/get_ik_left_arm_client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

