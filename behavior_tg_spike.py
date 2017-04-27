#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist, String
from sensor_msgs.msg import Joy

rospy.init_node('behavior_tg_spike', anonymous=True)
pub = rospy.Publisher('/Rosaria/cmd_vel', Twist, queue_size = 10)
conversation = rospy.Publisher('topic_attention_conversation', String, queue_size = 10)
#rate = rospy.Rate(5) # hz
global msg
msg = Twist()


def callback(data):
	rospy.loginfo(rospy.get_caller_id() + " recu!")
	# Saisie joystick
	msg.linear.x = 0.0
	msg.linear.y = 0.0
	msg.linear.z = 0.0
	msg.angular.x = 0.0
	msg.angular.y = 0.0
	msg.angular.z = 0.0

        multiplicateur = 1.5

        msg.linear.x = data.axes[4] * multiplicateur
        msg.angular.z = data.axes[3] * multiplicateur

        if data.buttons[0] != 0:    # A: Bonjour
        	rospy.loginfo("Salutations!")
        	conversation.publish("BONJOUR")
        if data.buttons[1] != 0:    # B: Presentation
                rospy.loginfo("Presentation")
           	conversation.publish("PRESENTATION")

        #if data.buttons[0] != 0:    # A: Recule
        #        rospy.loginfo("Recule")
        #        msg.linear.x = -vitesse
        #if data.buttons[2] != 0:    # X: Gauche
        #        rospy.loginfo("Gauche")
        #        msg.angular.x = vitesse
        #if data.buttons[1] != 0:    # B: Droite
        #        rospy.loginfo("Droite")
        #        msg.angular.x = -vitesse
        pub.publish(msg)
        #time.sleep(3)

rospy.Subscriber("/joy", Joy, callback)

rospy.spin()

    
