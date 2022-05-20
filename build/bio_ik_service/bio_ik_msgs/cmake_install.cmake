# Install script for directory: /home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/bio_ik_msgs/msg" TYPE FILE FILES
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/AvoidJointLimitsGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/BalanceGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/CenterJointsGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/ConeGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/DirectionGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/IKRequest.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/IKResponse.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/JointVariableGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/LineGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/LookAtGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/MaxDistanceGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/MinDistanceGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/MinimalDisplacementGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/OrientationGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/PoseGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/PositionGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/SideGoal.msg"
    "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/msg/TouchGoal.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/bio_ik_msgs/srv" TYPE FILE FILES "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/srv/GetIK.srv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/bio_ik_msgs/cmake" TYPE FILE FILES "/home/medrobotics/jack_ws/src/build/bio_ik_service/bio_ik_msgs/catkin_generated/installspace/bio_ik_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/medrobotics/jack_ws/src/build/devel/include/bio_ik_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/medrobotics/jack_ws/src/build/devel/share/roseus/ros/bio_ik_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/medrobotics/jack_ws/src/build/devel/share/common-lisp/ros/bio_ik_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/medrobotics/jack_ws/src/build/devel/share/gennodejs/ros/bio_ik_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/medrobotics/jack_ws/src/build/devel/lib/python3/dist-packages/bio_ik_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/medrobotics/jack_ws/src/build/devel/lib/python3/dist-packages/bio_ik_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/medrobotics/jack_ws/src/build/bio_ik_service/bio_ik_msgs/catkin_generated/installspace/bio_ik_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/bio_ik_msgs/cmake" TYPE FILE FILES "/home/medrobotics/jack_ws/src/build/bio_ik_service/bio_ik_msgs/catkin_generated/installspace/bio_ik_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/bio_ik_msgs/cmake" TYPE FILE FILES
    "/home/medrobotics/jack_ws/src/build/bio_ik_service/bio_ik_msgs/catkin_generated/installspace/bio_ik_msgsConfig.cmake"
    "/home/medrobotics/jack_ws/src/build/bio_ik_service/bio_ik_msgs/catkin_generated/installspace/bio_ik_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/bio_ik_msgs" TYPE FILE FILES "/home/medrobotics/jack_ws/src/bio_ik_service/bio_ik_msgs/package.xml")
endif()

