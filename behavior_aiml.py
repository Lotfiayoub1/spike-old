#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_aiml', anonymous=True)
rospy.loginfo("node_play_aiml")

rospy.loginfo("Behavior_aiml")
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

soundhandle.say('Testing the new A P I.')
rospy.sleep(3)

voix = soundhandle.voiceSound("Testing the new A P I.")
voix.repeat()
rospy.sleep(3)
voix.stop()

langue = 1

# L'objet Kernel est l'interface public pour l'interpreteur AIML. 
k = aiml.Kernel()

# Chargement de d'un fichier de contenu
# startup.xml charge tous les fichiers de contenu .aiml

if langue = 1:
	# Version anglaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/en/startup.xml")
	k.respond("LOAD AIML ENGLISH")
else:
	# Version francaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/fr/startup.xml") 
	k.respond("LOAD AIML FRENCH")

while True: print k.respond(raw_input("Spike chat BOT> "))


