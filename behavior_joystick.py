#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import String
from sensor_msgs.msg import Joy


rospy.init_node('behavior_tg_spike', anonymous=True)
rospy.loginfo("Behavior_tg_spike")

mode_normal = 1
mode_creation_map = 2
mode = mode_creation_map

pointA_x = 0.0
pointA_y = 0.0
pointB_x = 1.0
pointB_y = -3.0

global vitesse
if mode == mode_creation_map:
        vitesse = 0.3
else:
        vitesse = 0.6

pub = rospy.Publisher('/Rosaria/cmd_vel', Twist, queue_size = 10)
goal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 10)
conversation = rospy.Publisher('topic_attention_conversation', String, queue_size = 10)

#rate = rospy.Rate(5) # hz
global msg
msg = Twist()
msg.linear.x = 0.0
msg.linear.y = 0.0
msg.linear.z = 0.0
msg.angular.x = 0.0
msg.angular.y = 0.0
msg.angular.z = 0.0

global a, b
a = PoseStamped()
b = PoseStamped()


def callbackJoy(data):
        #rospy.loginfo(rospy.get_caller_id() + " recu!")
	# Saisie joystick

        if data.buttons[0] != 0:    # A
                rospy.loginfo("Aller au point A")
                a.pose.position.x = pointA_x
                a.pose.position.y = pointA_y
                rospy.loginfo(a)
        	goal.publish(a)

        if data.buttons[1] != 0:    # B
                rospy.loginfo("Aller au point B")
                b.pose.position.x = pointB_x
                b.pose.position.y = pointB_y
                rospy.loginfo(b)
           	goal.publish(b)

        if data.buttons[2] != 0:    # X
            	rospy.loginfo("Attention")
           	conversation.publish("ATTENTION")

        if data.buttons[3] != 0:    # Y 
            	rospy.loginfo("Salutation")
           	conversation.publish("BONJOUR")

        if data.buttons[5] != 0: # RB
                msg.linear.x = data.axes[4] * vitesse
                msg.angular.z = data.axes[3] * vitesse
                pub.publish(msg)


rospy.Subscriber("/joy", Joy, callbackJoy)

rospy.spin()

    
