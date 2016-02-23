#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
from espeak import espeak
import festival

rospy.init_node('node_aiml', anonymous=True)
rospy.loginfo("node_play_aiml")

# L'objet Kernel est l'interface public pour l'interpreteur AIML. 
#k = aiml.Kernel()

# Chargement de d'un fichier de contenu
# startup.xml charge tous les fichiers de contenu .aiml

# Version anglaise
#k.learn("/home/pi/catkin_ws/src/spike/src/aiml/en/startup.xml")

# Version francaise
#k.learn("/home/pi/catkin_ws/src/spike/src/aiml/fr/startup.xml")


#k.respond("load aiml b")

#espeak.synth("Hello world!")
festival.say("Hello World")

#while True: print k.respond(raw_input("> "))


