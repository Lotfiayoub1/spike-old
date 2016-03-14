#!/usr/bin/env python
import roslib
import rospy, os, sys
import time

rospy.init_node('node_attention', anonymous=True)
rospy.loginfo("Behavior_attention")

modeVerbose = 1
modeSilencieux = 2
mode = modeVerbose

# TODO: Faire un tableau de behaviors
# Est-ce la bonne façon de démarrer un noeud? 
# Il faut un handle dessus. 
# Faire un tableau de structure
# Struct Behaviors
#	Nom du behavior
#	Nom du fichier
# 	Handle
#	Priorité
# Avec un Dict, possiblement. 

# Démarrer les noeuds dans une boucle. 
os.system("rosrun spike behavior_chatbot_aiml.py")
os.system("rosrun spike behavior_deplacement.py")
os.system("rosrun spike behavior_ecoute.py")
os.system("rosrun spike behavior_humeur.py")
os.system("rosrun spike behavior_joue_son.py")
os.system("rosrun spike behavior_parle.py")
os.system("rosrun spike behavior_idle.py")

while True:
	if mode == modeVerbose:
		print "Attention" 
	# Boucle sur tous les behaviors et retourne le prioritaire.
	# Execute le prioritaire. 

	if mode == modeVerbose:
		print "Execution du behavior... Priorité X."