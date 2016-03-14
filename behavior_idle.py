#!/usr/bin/env python
import roslib
import rospy, os, sys
import time

rospy.init_node('node_idle', anonymous=True)
rospy.loginfo("Behavior_idle")

while True:
	# Quand il ne se passe rien:
	# Il appelle le chat bot "SPIKE ENNUI" (après 10 minute 	# d'inactivité	
	# Il joue un son, à une certaine fréquence. 
	

