#!/usr/bin/python
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
 # -*- coding: ascii -*-
import random
import rospy 
from std_msgs.msg import String
from random import randint

# Enregistrement du noeud ROS a ROSCORE. 
rospy.init_node('sonar', anonymous=True)

# Declaration du topic "chatter".  On va publier des string.  Max de 10 dans la queue.  Les plus anciennes s'eliminent.
pub = rospy.Publisher("pub_sonar_informationautour", String, queue_size=10)
 
def obstacleDevant(objetDevant):
    print(objetDevant)
    surrounding = ""
    for i in range(0, 4):
        if (objetDevant[i] == "M") or (objetDevant[i] == "N"):
            surrounding += "0"
        elif objetDevant[i] == "F":
            surrounding += "2"
        else:
            monRandom = random.randint(0,4)
            if monRandom == 0:
                surrounding += "0"
            else:
                surrounding += "1"
    return surrounding

# On defini une fonction callback.  Elle va s'appeler a toutes les fois que le topic recoit quelque chose. 
def callback(data):
    obstaclesAutour = obstacleDevant(data.data)
    # Affiche la chaine a la console (debuggage) 
    rospy.loginfo("Jecris " + obstaclesAutour + " a EZIC")
    # Publication de la chaine sur le topic. 
    pub.publish(obstaclesAutour)

# On souscrit au topic nomme "pub_geosphere_gettoutautour".  On va recevoir des string.  La fonction qui va le traiter se nomme callback.
rospy.Subscriber("pub_geosphere_gettoutautour", String, callback)

# On boucle a l'infini.  Seul le callback sera appele sur reception d'un message. 
print('Running')
rospy.spin()

