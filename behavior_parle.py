#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import wave


from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_parle', anonymous=True)
rospy.loginfo("Behavior_parle")

francais = 1
anglais = 2

modeTest = 1
modeChatBot = 2
mode = modeTest

langue = francais

while True:
	if mode == modeChatBot:
		# modeChatBot
		# Bloque sur l'attente de la reponse 
	else:
		# modeTest
		entree = raw_input("Test a prononcer> ")

	texte = 'espeak "' + entree + '" -v french -s 150 -p 20' 
	print texte
	os.system(texte)

