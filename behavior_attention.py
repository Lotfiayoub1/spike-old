#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import subprocess
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


# Demarrer les noeuds dans une boucle. 
if verbose:
	rospy.loginfo("Demarrage des noeuds")

#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_joue_son.py')
#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_chatbot_aiml.py')
#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_parle.py')
#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_idle.py')
#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_deplacement.py')
#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_ecoute.py')
#os.spawnl(os.P_NOWAIT, 'rosrun spike behavior_humeur.py')

etatHumeur = "Neutre"
etatPensee = "Neutre"


while True:
	if verbose:
		rospy.loginfo("Boucle attention")

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
	
	# Execute le node prioritaire
	topic_joue_son.publish("EtatEveil")
	topic_humeur.publish(etatHumeur)
	topic_pensee.publish(etatPensee)

	if verbose:
		print "Node Attention: Execution behavior X"
