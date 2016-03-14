#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_joue_sonanonymous=True)
rospy.loginfo("Behavior_joue_son")

modeJoueEnBoucle = 1
modeRecoitSignal = 2

mode = modeJoueEnBoucle

rospy.loginfo("Init son")
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

soundAssets = '/home/ubuntu/catkin_ws/src/spike/src/spike/sons/'

# TODO: Mettre les sons dans un tableau.
nomWav = 'robot.wav'

attente = 5 # seconds
while (True):
	if modeJoueEnBoucle: 
		#os.system("mplayer " + soundAssets + nomWav)
		soundhandle.stopAll()
		soundhandle.playWave(soundAssets + nomWav)
		time.sleep(attente)
	else:
		soundhandle.stopAll()
		soundhandle.playWave(soundAssets + nomWav)
		time.sleep(attente)



