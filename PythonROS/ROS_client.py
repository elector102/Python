#!/usr/bin/env python
#import roslib #roslib.load_manifest('actionlib_turtlebot')
import rospy
import actionlib
#import opendoors.msg
from geometry_msgs.msg import Pose
import actionlib_turtlebot.msg

def node():
    gripper_client = actionlib.SimpleActionClient('ros_action',actionlib_turtlebot.msg.ROSAction)
    rospy.loginfo("waiting for server")
    gripper_client.wait_for_server()

    goal_pose = actionlib_turtlebot.msg.ROSGoal()

    pose = Pose()
    pose.position.x = 2
    pose.position.y = 0.7
    pose.position.z = 0
    pose.orientation.x = 0
    pose.orientation.y = 0
    pose.orientation.z = 0
    pose.orientation.w = 0
    goal_pose.pose =  pose

    rospy.loginfo("waiting for result")
    gripper_client.send_goal_and_wait(goal_pose)

if __name__ == '__main__':
    rospy.init_node('ros_action')
    node()