execute_process(COMMAND "/home/medrobotics/jack_ws/src/build/mrn_movo/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/medrobotics/jack_ws/src/build/mrn_movo/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
