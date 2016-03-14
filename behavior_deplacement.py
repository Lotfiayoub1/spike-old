#!/usr/bin/env python
import roslib
import rospy, os, sys
import time

rospy.init_node('node_deplacement', anonymous=True)
rospy.loginfo("Behavior_deplacement")

modeTest = 1
modeRobot = 2
mode = modeTest

while True:
	if mode == modeRobot:
		# modeRobot
		# Bloque sur l'attente de la réponse 
	else:
		# modeTest
		# je ne sais pas encore ce qu'il y aura ici		

