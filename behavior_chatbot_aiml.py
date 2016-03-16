#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml

rospy.init_node('node_chatbot_aiml', anonymous=True)
rospy.loginfo("Behavior_chatbot_aiml")

verbose = True

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

if verbose:
	rospy.loginfo("Chargement des fichiers AIML.")

if langue == anglais:
	# Version anglaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/en/startup.xml")
	k.respond("LOAD AIML ENGLISH")
else:
	# Version francaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/fr/startup.xml") 
	k.respond("LOAD AIML FRENCH")
if verbose:
	rospy.loginfo("Fin du chargement des fichiers AIML.")

presentation = False
while True:
	
	if mode == modeClavier:
		# Mode clavier (test)	
		if presentation == False:
			k.respond("SPIKE LOAD VARIABLE ENVIRONNEMENT")
			reponse= k.respond("SPIKE PRESENTATION1")
			print "Spike> " + reponse
			presentation = True
			entree = raw_input("Vous> ")
			reponse = k.respond("SPIKE PRESENTATION2 " + entree)
			print "Spike> " + reponse
		entree = raw_input("Vous> ")
		reponse = k.respond(entree)
		if len(reponse) == 0:
			reponse = k.respond("SPIKE NE SAIT PAS")	
		print "Spike> " + reponse
	else: 
		# Mode vocal (robot) 
		#entree = texte recu de la reconnaissance vocale. 
		reponse = k.respond(entree)

