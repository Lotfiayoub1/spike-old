#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import random
from std_msgs.msg import String

rospy.init_node('node_idle', anonymous=True)
rospy.loginfo("Behavior_idle")

verbose = True


if verbose:
	rospy.loginfo("Initialisation des topics")

topic_idle_parle = rospy.Publisher('topic_idle_parle', String, queue_size=10)
topic_idle_son = rospy.Publisher('topic_idle_son', String, queue_size=10)
topic_idle_aiml_pattern = rospy.Publisher('topic_idle_aiml_pattern', String, queue_size=10)

def callbackAIML(data):
	if verbose:
		rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
	templateAIML = data.data
	topic_idle_parle.publish(templateAIML)

rospy.Subscriber("topic_idle_aiml_template", String, callbackAIML)

if verbose:
	rospy.loginfo("Message que Spike est pret.")
time.sleep(2)
topic_idle_aiml_pattern.publish("SPIKE PRET")


while True:
	# Quand il ne se passe rien:
	# Il peut appeler chat bot pour se trouver une replique d'ennui. 	
	# Ou il joue un son.

	time.sleep(10)

	# Tire un nombre aleatoire (bornes incluses)
	nb = random.randint(0, 9)

	if nb <= 2:	
		# 2 fois sur 10, il va dire qu'il s'ennuie.
		if verbose:
			rospy.loginfo("demande ce qu'il faut dire au chatbot quand on s'ennuie")
		topic_idle_aiml_pattern.publish("SPIKE ENNUI")
	else:
		# 8 fois sur 10, il va produire un son. 
		if verbose:
			rospy.loginfo("Envoie message au behavior_joue_son")
		topic_idle_son.publish("EtatEveil")

	

