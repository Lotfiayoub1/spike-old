#!/usr/bin/env python
import roslib
import rospy, os, sys
import time

rospy.init_node('node_play_sound', anonymous=True)
rospy.loginfo("node_play_sound")

soundAssets = '/home/pi/catkin_ws/src/spike/src/sons/'
nomWav = 'robot.wav'

attente = 1 # seconds

while (True):
		os.system("mplayer " + soundAssets + nomWav)
		time.sleep(attente)


