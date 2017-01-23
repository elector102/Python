#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
#from turtlesim import Pose
from turtlesim.msg import Pose
import math
PI = 3.14159265
class Turtlebot():
    def __init__(self):
        self.velocity = Twist()
        self.current_pose = Pose()
        self.current_objective = None
        self.current_theta_objective = None
        self.objective_list = None
        self.pub_velocity = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =1)
        self.sub_pose = rospy.Subscriber('/turtle1/pose', Pose, self.velocity_callback)
        rospy.init_node('ROS_node', anonymous = True)
        self.rate = rospy.Rate(100) # 50hz
        rospy.loginfo("Start node")
        self.current_objective_theta = 0
        self.pause = False
        
    def turtlebot(self):
        while not rospy.is_shutdown():
            selfpub_velocity.publish(velocity)
            rate.sleep()

    def velocity_callback(self, data):
        self.current_pose = data
        if not self.current_objective == None:
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
            if not self.objective_list == None:
                self.new_objective()
                
        
    def new_objective(self):
        if not len(self.objective_list) == 0:
            rospy.loginfo(" New objective")
            self.current_objective = self.objective_list[0]
            self.objective_list.pop(0)
            rospy.loginfo("current objective: {}".format(self.current_objective))
            rospy.loginfo("objective list: {}".format(self.objective_list))
            self.new_theta_objective()
        else:
            rospy.loginfo("STAR finished")
    
    def set_new_objectives_list(self, objective_list):
        self.objective_list = objective_list
        self.list_count = 0
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
            while not (len(self.objective_list) == 0 and  rospy.is_shutdown()):
                #rospy.loginfo("publish velocity")
                #rospy.loginfo("velocidad lineal = {} ; velocidad angular = {} ".format(self.velocity.linear.x, self.velocity.angular.z))
                self.pub_velocity.publish(self.velocity)
                self.rate.sleep()
        pass
    
    def pause(self):
        self.pause = not self.pause
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
        pose = turtle.current_pose
        STAR = compute_star(2, pose, 5)
        for i in range(0, len(STAR)):
            print('position in x: {} im y: {} in pose {}'.format(STAR[i].x, STAR[i].y, i))
        rospy.loginfo("Start to draw")
        turtle.set_new_objectives_list(STAR)
        turtle.start()
    except rospy.ROSInterruptException:
        print('error ')
        break