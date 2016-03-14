#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml

rospy.init_node('node_chatbot_aiml', anonymous=True)
rospy.loginfo("Behavior_chatbot_aiml")

francais = 1
anglais = 2

modeClavier = 1
modeVocal = 2

langue = francais
mode = modeClavier

# L'objet Kernel est l'interface public pour l'interpreteur AIML. 
k = aiml.Kernel()

# Chargement de d'un fichier de contenu
# startup.xml charge tous les fichiers de contenu .aiml

if langue == anglais:
	# Version anglaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/en/startup.xml")
	k.respond("LOAD AIML ENGLISH")
else:
	# Version francaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/fr/startup.xml") 
	k.respond("LOAD AIML FRENCH")

while True:
	if mode == modeClavier:
		# Mode clavier (test)
		entree = raw_input("Spike chat BOT> ")
		reponse = k.respond(entree)
	else: 
		# Mode vocal (robot) 
		#entree = texte recu de la reconnaissance vocale. 
		reponse = k.respond(entree)

