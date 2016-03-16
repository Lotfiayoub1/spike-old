#!/usr/bin/env python
import roslib
import rospy, os, sys
import time

rospy.init_node('node_idle', anonymous=True)
rospy.loginfo("Behavior_idle")

while True:
	# Quand il ne se passe rien:
	# Il peut appler chat bot "SPIKE ENNUI" 	
	# Ou il joue un son.
	

