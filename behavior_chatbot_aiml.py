#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
from std_msgs.msg import String

rospy.init_node('node_chatbot_aiml', anonymous=True)
rospy.loginfo("Behavior_chatbot_aiml")

verbose = True

francais = 1
anglais = 2

modeClavier = 1
modeVocal = 2

langue = anglais
mode = modeVocal

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


if mode == modeClavier:
	presentation = False
	while True:
		entree = raw_input("Vous> ")
		reponse = k.respond(entree)
		if len(reponse) == 0:
			reponse = k.respond("SPIKE NE SAIT PAS")	
		print "Spike> " + reponse

if mode == modeVocal:
	if verbose:
		rospy.loginfo("Definition du callback pour les appel aux fichiers AIML.")
	
	def callbackIdle(data):
		if verbose:
			rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
		patternAIML = data.data
		templateAIML = k.respond(patternAIML)
		if verbose:
			rospy.loginfo("Reponse du chatbot: " + templateAIML)
		topic_idle_aiml_template.publish(templateAIML)

	def callbackParle(data):
		if verbose:
			rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
		patternAIML = data.data
		templateAIML = k.respond(patternAIML)
		if verbose:
			rospy.loginfo("Reponse du chatbot: " + templateAIML)
		topic_parle.publish(templateAIML)

	# On souscrit de behavior_attention
	rospy.Subscriber("topic_attention_conversation", String, callbackParle)
	# On souscrit au idle_aiml_pattern
	rospy.Subscriber("topic_idle_aiml_pattern", String, callbackParle)
	# On publie a behavior_parle
	topic_parle = rospy.Publisher('topic_parle', String, queue_size=10)
	# On publie a behavior_idle
	topic_idle_aiml_template = rospy.Publisher('topic_idle_aiml_template', String, queue_size=10)

	if verbose:
		rospy.loginfo("En attente des topics...")	

	# Puisqu'on attend un signal, il ne faut pas quitter
	# L'instruction suivante permet de rester dans le programme
	rospy.spin()
