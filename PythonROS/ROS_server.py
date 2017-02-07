#!/usr/bin/env python
import roslib
#roslib.load_manifest('actionlibs_turtlebot')
import rospy
import actionlib
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from turtlesim.msg import Pose
import actionlib_turtlebot.msg
import math
PI = 3.14159265
class Turtlebot():
    # create messages that are used to publish feedback/result
    _feedback = actionlib_turtlebot.msg.ROSFeedback()
    _result = actionlib_turtlebot.msg.ROSResult()
    
    def __init__(self):
        self.velocity = Twist()
        self.current_pose = Pose()
        self.current_objective = None
        self.current_theta_objective = None
        self.objective_list = None
        self.objective_finish = False
        self.pub_velocity = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =1)
        self.sub_pose = rospy.Subscriber('/turtle1/pose', Pose, self.velocity_callback)
        rospy.init_node('ros_action', anonymous = True)
        self.rate = rospy.Rate(100) # 50hz
        rospy.loginfo("Start node")
        self.current_objective_theta = 0
        self.pause = False
        self._action_name = "ros_action"
        self._as = actionlib.SimpleActionServer(self._action_name, actionlib_turtlebot.msg.ROSAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        
    def turtlebot(self):
        while not rospy.is_shutdown():
            selfpub_velocity.publish(velocity)
            rate.sleep()

    def velocity_callback(self, data):
        self.current_pose = data
        if not self.current_objective == None:
            #rospy.loginfo("3## current objective: {}".format(self.current_objective))
            #rospy.loginfo("3##objective list: {}".format(self.objective_list))
            #rospy.loginfo("3##new objective list len: {}".format(len(self.objective_list)))
            #rospy.loginfo("theta current pose : {}".format(self.current_pose.theta))
            #rospy.loginfo("theta current objective(vel) : {}".format(self.current_objective_theta))
            if (abs(self.current_pose.theta - self.current_objective_theta) > 0.01):
                #rospy.loginfo(" Set angular velocity")
                self.velocity.linear.x = 0
                self.velocity.angular.z = 1
            elif ((abs(self.current_pose.x - self.current_objective.x) > 0.1) or (abs(self.current_pose.y - self.current_objective.y) > 0.1)):
                #rospy.loginfo(" Set lineal velocity")
                self.velocity.linear.x = 1
                self.velocity.angular.z = 0
            else :
                self.velocity.linear.x = 0
                self.velocity.angular.z = 0
                self.new_objective()
                #rospy.loginfo("Objective reached")
        else:
            self.velocity.linear.x = 0
            self.velocity.angular.z = 0
            rospy.loginfo("##objective list: {}".format(self.objective_list))
            rospy.loginfo("##new objective list len: {}".format(len(self.objective_list)))
            if not self.objective_list == None and not len(self.objective_list)== 0:
                self.new_objective()
                
        
    def new_objective(self):
        if not len(self.objective_list) == 0:
            rospy.loginfo(" New objective")
            self.current_objective = self.objective_list[0]
            self.objective_list.pop(0)
            rospy.loginfo("current objective: {}".format(self.current_objective))
            rospy.loginfo("objective list: {}".format(self.objective_list))
            rospy.loginfo("new objective list len: {}".format(len(self.objective_list)))
            self.new_theta_objective()
        else:
            rospy.loginfo("STAR finished")
            self.objective_finish = True
    
    def set_new_objectives_list(self, objective_list):
        self.objective_list = objective_list
        self.list_count = 0
        self.new_objective()
        self.objective_finish = False
#        for pose in self.objective_list: # new, to probe
#            d_x = pose.x - pose_d.x
#            d_y = pose.y - pose_d.y
#
#            theta_aux = fabs(atan2(d_y, d_x))
#            if (d_y < 0 ) :
#                self.pose.theta = (2 * PI) - theta_aux
#            else:
#                self.pose.theta = theta_aux
                
    def new_theta_objective(self):# old, for test
        d_x = self.current_objective.x - self.current_pose.x
        d_y = self.current_objective.y - self.current_pose.y
    
        theta_aux = abs(math.atan2(d_y, d_x))
        if (d_y < 0 ) :
            self.current_objective_theta = (2 * PI) - theta_aux
        else:
            self.current_objective_theta = theta_aux
        #rospy.loginfo("new theta current objective : {}".format(self.current_objective_theta))


    def start(self):
        if self.objective_list == None:
            rospy.loginfo("You did not load the objectives")
        elif not self.pause:
            while not rospy.is_shutdown():
                rospy.loginfo("entro al while")
                #rospy.loginfo("velocidad lineal = {} ; velocidad angular = {} ".format(self.velocity.linear.x, self.velocity.angular.z))
                self._feedback.current_pose.position.x = self.current_pose.x
                self._feedback.current_pose.position.y = self.current_pose.y
                self._as.publish_feedback(self._feedback)
                self.pub_velocity.publish(self.velocity)
                self.rate.sleep()
                if self._as.is_preempt_requested():
                    rospy.loginfo('%s: Preempted' % self._action_name)
                    self._as.set_preempted()
                    continue
                if self.objective_finish == True:
                    self._result.finish_pose = self._feedback.current_pose
                    rospy.loginfo('%s: Succeeded' % self._action_name)
                    self._as.set_succeeded(self._result)
                    return
    
    def pause(self):
        self.pause = not self.pause
        pass
    
    def execute_cb(self, goal):
        
        goal_pose = Pose()
        goal_pose.x = goal.pose.position.x
        goal_pose.y = goal.pose.position.y
        way = []
        way.append(goal_pose)
        rospy.loginfo("Start to draw goal :".format(goal.pose))
        self.set_new_objectives_list(way)
        #while not (len(self.objective_list) == 0) and not (rospy.is_shutdown()):
        
        rospy.loginfo("while objective list len : {}".format(len(self.objective_list)))
        #rospy.loginfo("velocidad lineal = {} ; velocidad angular = {} ".format(self.velocity.linear.x, self.velocity.angular.z))
#        self._feedback.current_pose.position.x = self.current_pose.x
#        self._feedback.current_pose.position.y = self.current_pose.y
#        self._as.publish_feedback(self._feedback)
        #self.pub_velocity.publish(self.velocity)
        self.rate.sleep()
        # check that preempt has not been requested by the client
#        if self._as.is_preempt_requested():
#            rospy.loginfo('%s: Preempted' % self._action_name)
#            self._as.set_preempted()
#            success = False
#            break
        self.start()
#        if success:
#            rospy.loginfo(' Algo raro!')
#        self._result.finish_pose = self._feedback.current_pose
#        rospy.loginfo('%s: Succeeded' % self._action_name)
#        self._as.set_succeeded(self._result)
        pass

def compute_star(radio, pose, corner_number):
    cx = pose.x - radio
    cy = pose.y
    px = pose.x + radio
    py = pose.y
    theta = 2*PI/corner_number
    beta = math.atan2(py - cy, px - cx)
    POLIGONO = []
    STAR = []
    for i in range(0, corner_number):
        aux = Pose()
        x = radio * math.cos(i * theta)
        y = radio * math.sin(i * theta)
        
        # Rotate the polygon 
        xPrime = x * math.cos(beta) - y * math.sin(beta)
        yPrime = x * math.sin(beta) + y * math.cos(beta)
        
        # Translate the polygon to it's original position
        xPrime += cx
        yPrime += cy
        aux.x = xPrime
        aux.y = yPrime
        POLIGONO.append(aux)
    i = 0
    list_count = 0
    rospy.loginfo("len poligono : {}".format(len(POLIGONO)))
    while not list_count == len(POLIGONO):
        rospy.loginfo("pasada : {}".format(i))
        STAR.append(POLIGONO[i])
        #POLIGON.pop[i]
        
        list_count += 1
        i += 2
        if i  >= len(POLIGONO):
            if len(POLIGONO)%2 ==0:
                i -= len(POLIGONO)-1
            else:
                i -= len(POLIGONO)
    rospy.loginfo("len poligono : {}".format(len(STAR)))
    STAR.append(POLIGONO[0])
    return STAR

if __name__ == '__main__':
    try:
        turtle = Turtlebot()
#        pose = turtle.current_pose
#        way = []
#        way.append(pose)
#        rospy.loginfo("Start to draw")
#        turtle.set_new_objectives_list(STAR)
        #turtle.start()
    except rospy.ROSInterruptException:
        print('error ')
