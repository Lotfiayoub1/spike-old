#!/usr/bin/python
import rospy
from std_msgs.msg import String  # On importe le format du message.
 
# Enregistrement du noeud ROS a ROSCORE. 
rospy.init_node('actuateur', anonymous=True)



infoAutour = "";

def varGlobalSet():
	global infoAutour;

varGlobalSet();
	
# Declaration du topic "chatter".  On va publier des string.  Max de 10 dans la queue.  Les plus anciennes s'eliminent.

pub_actu_reponseactiondeplacement = rospy.Publisher('topic_actu_reponseactiondeplacement', String, queue_size=10)
pub_actu_reussi_avancer = rospy.Publisher('topic_actu_reussi_avancer', String, queue_size=10)



def callback_actiondeplacement(data):
	# On vient de recevoir quelque chose sur le topic.  On l'affiche et on le traite.
	print("Info recu")
	rospy.loginfo(rospy.get_caller_id() + "I heard %s from Hamon", data.data)
	if infoAutour != "":
		if data.data == "N":
			
			#N-> obstacle
			if infoAutour[0] == "0":
				reponseAvancer = "F %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
				
			#N-> pas obstacle
			if infoAutour[0] == "1":
				avancerDirection = "N %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
			
			#N-> fin
			if infoAutour[0] == "2":
				avancerDirection = "N %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
			
		if data.data == "E":
			
			#E-> obstacle
			if infoAutour[1] == "0":
				reponseAvancer = "F %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
				
			#E-> pas obstacle
			if infoAutour[1] == "1":
				avancerDirection = "E %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
			
			#E-> fin
			if infoAutour[1] == "2":
				avancerDirection = "E %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
		
		if data.data == "S": 
			
			#S-> obstacle
			if infoAutour[2] == "0":
				reponseAvancer = "F %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
				
			#S-> pas obstacle
			if infoAutour[2] == "1":
				avancerDirection = "S %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
			
			#S-> fin
			if infoAutour[2] == "2":
				avancerDirection = "S %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
		
		if data.data == "O":
			
			#O-> obstacle
			if infoAutour[3] == "0":
				reponseAvancer = "F %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
				
			#O-> pas obstacle
			if infoAutour[3] == "1":
				avancerDirection = "O %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)
			
			#O-> fin
			if infoAutour[3] == "2":
				avancerDirection = "O %s"
				rospy.loginfo(avancerDirection)
				pub_actu_reussi_avancer.publish(avancerDirection)
				
				reponseAvancer = "T %s"
				rospy.loginfo(reponseAvancer)
				pub_actu_reponseactiondeplacement.publish(reponseAvancer)



# On defini une fonction callback.  Elle va s'appeler a toutes les fois que le topic recoit quelque chose. 
def callback_informationautour(data):
	# On vient de recevoir quelque chose sur le topic.  On l'affiche et on le traite.
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s from GUI", data.data)

	infoAutour = data.data;


rospy.Subscriber('topic_ia_actiondeplacement', String, callback_actiondeplacement)
rospy.Subscriber('pub_sonar_informationautour', String, callback_informationautour)

print("Actuateurs prets")

# On boucle a l'infini.  Seul le callback sera appele sur reception d'un message. 
rospy.spin()






