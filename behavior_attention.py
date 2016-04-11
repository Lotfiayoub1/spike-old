#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
#import subprocess
import fuzzy.storage.fcl.Reader
from std_msgs.msg import String

rospy.init_node('node_attention', anonymous=True)
rospy.loginfo("Behavior_attention")

verbose = True

if verbose:
	rospy.loginfo("Initialisation des topics")

# Communication avec Behavior_joue_son
topic_joue_son = rospy.Publisher('topic_joue_son', String, queue_size=10)
# Communication avec Behavior_humeur (visage)
topic_humeur = rospy.Publisher('topic_humeur', String, queue_size=10)
topic_pensee = rospy.Publisher('topic_pensee', String, queue_size=10)
# Communication avec Behavior_idle 
topic_idle = rospy.Publisher('topic_idle', String, queue_size=10)


# Chargement du fichier .fcl - Fuzzy Control Language qui contient la logique floue 
if verbose:
	rospy.loginfo("Chargement du fichier .FCL - Logique floue")

fuzzyLogicSystem = fuzzy.storage.fcl.Reader.Reader().load_from_file("/home/ubuntu/catkin_ws/src/spike/src/spike/fcl/attention.fcl")

fuzzy_logic_input = {
	"Senseur_Deplacement": 0.0,
	"Senseur_Vision": 0.0,
	"Senseur_Ecoute": 0.0,
	"Senseur_LRF": 0.0,
	"Senseur_Batterie": 0.0,
	"TempsDepuisDerniereAction": 0.0,
	"DerniereRepliqueConversation": 0.0,
	"Humeur_Actuel": 0.0
	}

fuzzy_logic_output  = {
	"Attention": 0.0,
	"Humeur": 0.0,
	"Energie": 0.0
	}


etatHumeur = "Neutre"
etatPensee = "Neutre"


while True:
	if verbose:
		rospy.loginfo("Boucle attention")

	fuzzy_logic_input["Senseur_Deplacement"] = 0.0
	fuzzy_logic_input["Senseur_Vision"] = 0.0
	fuzzy_logic_input["Senseur_Ecoute"] = 0.0
	fuzzy_logic_input["Senseur_LRF"] = 0.0
	fuzzy_logic_input["Senseur_Batterie"] = 0.0
	fuzzy_logic_input["TempsDepuisDerniereAction"] = 0.0
	fuzzy_logic_input["DerniereRepliqueConversation"] = 10.0
	fuzzy_logic_input["Humeur_Actuel"] = 5.0

	time.sleep(10)

	# Ecoute les messages des nodes
	
	# Traitement temporaire pour tester humeur
	if etatPensee == "Neutre":
		etatPensee = "Reflexion"
	else:
		etatPensee = "Neutre"
	if etatHumeur == "Neutre":
		etatHumeur = "Joyeux"
	else:
		etatHumeur = "Neutre"

	# Selectionne le behavior qui aura l'attention avec le system de logique flou. 
	# Selectionne egalement l'humeur
	fuzzyLogicSystem.calculate(fuzzy_logic_input, fuzzy_logic_output)

	attention = fuzzy_logic_output["Attention"]
	humeur = fuzzy_logic_output["Humeur"]
	energie = fuzzy_logic_output["Energie"]

	if verbose:
		rospy.loginfo("Attention defuzzyfiee: " + str(attention))
	if verbose:
		rospy.loginfo("Humeur  defuzzyfiee: " + str(humeur))
	if verbose:
		rospy.loginfo("Energie  defuzzyfiee: " + str(energie))	

	# Execute le node prioritaire
	topic_humeur.publish(etatHumeur)
	topic_pensee.publish(etatPensee)
	topic_idle.publish("null")

	if verbose:
		print "Node Attention: Execution behavior prioritaire..."
