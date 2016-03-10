#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_play_sound', anonymous=True)
rospy.loginfo("node_play_sound")

rospy.loginfo("Init son")
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

soundAssets = '/home/ubuntu/catkin_ws/src/spike/src/spike/sons/'
nomWav = 'robot.wav'


attente = 5 # seconds
while (True):
		#os.system("mplayer " + soundAssets + nomWav)
		soundhandle.stopAll()
		soundhandle.playWave(soundAssets + nomWav)
		time.sleep(attente)



