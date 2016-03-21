#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import wave
from std_msgs.msg import String

#from sound_play.msg import SoundRequest
#from sound_play.libsoundplay import SoundClient

rospy.init_node('node_parle', anonymous=True)
rospy.loginfo("Behavior_parle")

verbose = True

francais = 1
anglais = 2

modeTest = 1
modeRecoitRequetes = 2
mode = modeRecoitRequetes

entree = ""

langue = francais

def parle(entree):
	if verbose:
		rospy.loginfo("callback: Message recu: " + entree
)
	if len(entree) > 0: 
		texte = 'espeak "' + entree + '" -v french -s 150 -p 20' 
		if verbose:
			rospy.loginfo(texte)
		os.system(texte)
		entree = ""

if mode == modeTest:
	while True:
		# modeTest
		entree = raw_input("Texte a prononcer> ")
		parle(entree)

if mode == modeRecoitRequetes:

	def callbackIdle(data):
		if verbose:
			rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
		entree = data.data
		parle(entree)

	if verbose:
		rospy.loginfo("Enregistrement des callbacks")
	rospy.Subscriber("topic_idle_parle", String, callbackIdle)
	
	if verbose:
		rospy.loginfo("spin sur les callbacks...")	
	rospy.spin()

