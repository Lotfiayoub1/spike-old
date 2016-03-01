#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_aiml', anonymous=True)
rospy.loginfo("node_play_aiml")

rospy.loginfo("Init son")
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

rospy.loginfo("Dire hello world")
soundhandle.say('Hello world!')
rospy.sleep(3)


# L'objet Kernel est l'interface public pour l'interpreteur AIML. 
#k = aiml.Kernel()

# Chargement de d'un fichier de contenu
# startup.xml charge tous les fichiers de contenu .aiml

# Version anglaise
#k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/en/startup.xml")

# Version francaise
#k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/fr/startup.xml")


#k.respond("load aiml b")

#while True: print k.respond(raw_input("> "))


