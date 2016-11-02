#!/usr/bin/python
# Miguel Ducharme - Nicolas Hamon
# Cegep de Victoriaville 2016
import rospy
from std_msgs.msg import String
import random

miseAJour = True
peutSeDeplacer = "F"
directionDerniereDemande = "N"

# On defini une fonction callback.  Elle va s'appeler a toutes les fois que le topic recoit quelque chose.
def callback_reponseactiondeplacement(data):
    # On vient de recevoir quelque chose sur le topic.  On l'affiche et on le traite.
    peutSeDeplacer = data.data
    miseAJour = True

def callback_position(data):
    # On vient de recevoir quelque chose sur le topic.  On l'affiche et on le traite.
    position = data.data
    miseAJour = True

def set_global_maj():
    global position
    global miseAJour
    global peutSeDeplacer
    global directionDerniereDemande

# Setter nos globals
set_global_maj()

# Enregistrement du noeud ROS a ROSCORE.
rospy.init_node('ia_deplacement', anonymous=True)

# Declaration du topic chatter.  On va publier des string.  Max de 10 dans la queue.  Les plus anciennes s'eliminent.
pub_position = rospy.Publisher('topic_position', String, queue_size=10)

#pub_ia_demanderdeplacementpossible = rospy.Publisher('topic_ia_demanderdeplacementpossible', String, queue_size=10)

pub_ia_actiondeplacement = rospy.Publisher('topic_ia_actiondeplacement', String, queue_size=10)

pub_ia_ecrireconsole = rospy.Publisher('topic_ia_ecrireconsole', String, queue_size=10)
print("Not Running")
# On souscrit au topic nomme "chatter".  On va recevoir des string.  La fonction qui va le traiter se nomme callback.
rospy.Subscriber("topic_actu_reponseactiondeplacement", String, callback_reponseactiondeplacement)
while True:
    #S il  y a une mise a jour des informations.
    if miseAJour:
        print("Mise a jour...")
        miseAJour = False

        # Ici on fait notre intelligence
        print(peutSeDeplacer)
        if peutSeDeplacer == "T":
            if directionDerniereDemande == "N":
                pub_ia_ecrireconsole.Publish("Le robot s'est deplace au Nord")
            elif directionDerniereDemande == "E":
                pub_ia_ecrireconsole.Publish("Le robot s'est deplace a l'Est")
            elif directionDerniereDemande == "S":
                pub_ia_ecrireconsole.Publish("Le robot s'est deplace au Sud")
            elif directionDerniereDemande == "O":
                pub_ia_ecrireconsole.Publish("Le robot s'est deplace a l'Ouest")
            else:
                pub_ia_ecrireconsole.Publish("Une erreur s'est produite")
        else:
            random = random.randint(1,4)
            print(random)

            if random == 1:
                print("On demande aux actuateurs d aller au Nord")
                pub_ia_actiondeplacement.publish("N")
                directionDerniereDemande = "N"
            elif random == 2:
                print("On demande aux actuateurs d aller a l Est")
                pub_ia_actiondeplacement.publish("E")
                directionDerniereDemande = "E"
            elif random == 3:
                print("On demande aux actuateurs d aller au Sud")
                pub_ia_actiondeplacement.publish("S")
                directionDerniereDemande = "S"
            elif random == 4:
                print("On demande aux actuateurs d aller a l Ouest")
                pub_ia_actiondeplacement.publish("O")
                directionDerniereDemande = "O"
            else:
                pub_ia_ecrireconsole.Publish("Une erreur s'est produite")
