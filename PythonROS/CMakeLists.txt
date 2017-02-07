cmake_minimum_required(VERSION 2.8.3)
project(actionlib_turtlebot)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  genmsg
  actionlib_msgs
  actionlib
  nav_msgs
  message_generation
  roscpp
  rospy
  std_msgs
)

add_action_files(DIRECTORY action FILES ROS.action)
generate_messages(DEPENDENCIES actionlib_msgs nav_msgs)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES actionlibs_tutorials
   CATKIN_DEPENDS genmsg actionlib_msgs actionlib roscpp rospy std_msgs nav_msgs
#  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

