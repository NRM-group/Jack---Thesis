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

add_message_files(
  FILES
  ChestCompensationRequest.msg
  ChestCompensationResponse.msg
)

add_service_files(
  FILES
  Get_IK.srv
  Get_Chest_Compensation.srv
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
  src/mrn_movo/PointCloudVisualisation.py
  src/mrn_movo/state_machine.py
  src/mrn_movo/csv_output.py
  src/mrn_movo/op_movo_publishers/op_chest_approxtime.py
  src/mrn_movo/op_movo_publishers/op_wrist_left_approxtime.py
  src/mrn_movo/op_movo_publishers/op_wrist_right_approxtime.py
  src/mrn_movo/op_movo_publishers/op_elbow_left_approxtime.py
  src/mrn_movo/op_movo_publishers/op_elbow_right_approxtime.py
  src/mrn_movo/op_movo_publishers/op_shoulder_left_approxtime.py
  src/mrn_movo/op_movo_publishers/op_shoulder_right_approxtime.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

