#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

rospy.init_node('node_joue_son', anonymous=True)
rospy.loginfo("Behavior_joue_son")

verbose = True

modeJoueEnBoucle = 1
modeRecoitSignal = 2

mode = modeRecoitSignal

if verbose:
	rospy.loginfo("Init son")
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()
if verbose: 
	rospy.loginfo("Son initialise!")

soundAssets = '/home/ubuntu/catkin_ws/src/spike/src/spike/sons/'

# TODO: Mettre les sons dans un tableau.
nomWav = 'robot.wav'

attente = 5 # seconds
if mode == modeJoueEnBoucle:
	while True:
		if verbose: 
			rospy.loginfo("Joue un son.")
		#os.system("mplayer " + soundAssets + nomWav)
		soundhandle.stopAll()
		soundhandle.playWave(soundAssets + nomWav)
		time.sleep(attente)

if mode == modeRecoitSignal:
	def callback(data):
		if verbose:
			rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
		etat = data.data
		if etat == "EtatEveil":
			soundhandle.stopAll()
			soundhandle.playWave(soundAssets + nomWav)
			time.sleep(attente)
	
	# On s'inscrit au topic
	rospy.Subscriber("topic_joue_son", String, callback)

	# Puisqu'on attend un signal, il ne faut pas quitter
	# L'instruction suivante permet de rester dans le programme
	rospy.spin()
