#!/usr/bin/python
#Samuel Labrecque | Laurent Drolet | Tommy Vigneault
# Cegep de Victoriaville
# TP #3 -> Geosphere
import sys
import rospy
from std_msgs.msg import String  # On importe le format du message.


rospy.init_node('GeosphereNode', anonymous=True)
#Talkers
pub_geosphere_position = rospy.Publisher('pub_geosphere_position', String, queue_size=10)
pub_geosphere_stringmap = rospy.Publisher('pub_geosphere_stringmap', String, queue_size=10)
pub_geosphere_gettoutautour = rospy.Publisher('pub_geosphere_gettoutautour', String, queue_size=10)

print('Geosphere prete...')

if __name__ == "__main__":
    
    geosphere = [
        ["M", "R", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M"], 
        ["M", "S", "S", "S", "S", "S", "S", "S", "S", "S", "M", "S", "S", "S", "M"],
        ["M", "M", "M", "M", "S", "M", "M", "M", "M", "M", "M", "S", "M", "S", "M"], 
        ["M", "S", "S", "M", "S", "M", "S", "S", "S", "S", "S", "S", "M", "S", "M"],
        ["M", "M", "S", "M", "S", "S", "S", "M", "M", "M", "S", "M", "S", "S", "M"],
        ["M", "M", "S", "S", "S", "M", "M", "S", "S", "S", "S", "M", "S", "M", "M"],
        ["M", "S", "M", "M", "M", "M", "S", "S", "M", "M", "M", "M", "S", "S", "M"],
        ["M", "S", "S", "S", "S", "S", "S", "M", "S", "S", "S", "S", "M", "S", "M"],
        ["M", "M", "S", "M", "S", "M", "S", "M", "M", "M", "M", "S", "M", "S", "M"],
        ["M", "S", "S", "M", "S", "M", "S", "S", "S", "M", "M", "S", "S", "S", "M"],
        ["M", "S", "M", "M", "S", "M", "S", "M", "S", "M", "S", "M", "M", "S", "M"],
        ["M", "S", "S", "M", "S", "M", "S", "M", "S", "S", "S", "S", "M", "S", "M"],
        ["M", "M", "S", "M", "M", "M", "S", "M", "M", "M", "S", "M", "M", "S", "M"],
        ["M", "S", "S", "S", "S", "S", "S", "M", "S", "S", "S", "M", "S", "S", "M"],
        ["M", "M", "M", "M", "M", "M", "M", "M", "F", "M", "M", "M", "M", "M", "M"]
    ]
    x = 0;
    y = 1;
#    for list in geosphere:
#        for letter in list:
#            if letter == "M":
#                sys.stdout.write('#')
#            elif letter == "R":
#                sys.stdout.write('R')
#            else:
#                sys.stdout.write(' ')
#        print
        
    def getToutAutour():
        chaineRetour=""
        if geosphere[x-1][y] != None:
            chaineRetour += geosphere[x-1][y]
        else:
            chaineRetour += "N"
        if geosphere[x][y+1] != None:
            chaineRetour += geosphere[x][y+1]
        else:
            chaineRetour += "E"
        if geosphere[x+1][y] != None:
            chaineRetour += geosphere[x+1][y]
        else:
            chaineRetour += "S"
        if geosphere[x][y-1] != None:
            chaineRetour += geosphere[x][y-1]
        else:
            chaineRetour += "O"
        
        chaineRetour += str(rospy.get_time())
        rospy.loginfo(chaineRetour)
	# Publication de la chaine sur le topic. 
	pub_geosphere_gettoutautour.publish(chaineRetour)
            
    def bougerPointeur(direction):
        if direction == "N":
            x-=1
        elif direction == "E":
            y+=1
        elif direction == "O":
            y-=1
        elif direction == "S":
            x+=1    
            
    def sendStringMap ():
        stringmap=""
        for list in geosphere:
            for letter in list:
                stringmap += letter
            stringmap += ";"

        stringmap += str(rospy.get_time())
        rospy.loginfo(stringmap)
	# Publication de la chaine sur le topic. 
	pub_geosphere_stringmap.publish(stringmap)
    
    def sendPosition():
        position = str(x) + "," +str(y)
        rospy.loginfo(position)
	# Publication de la chaine sur le topic. 
	pub_geosphere_position.publish(position)
    #si on recoit une direction sur le topic on change la position du robot dans le grid    
    def callback(data):
	# On vient de recevoir quelque chose sur le topic.  On l'affiche et on le traite.
	rospy.loginfo(rospy.get_caller_id() + "I heard a deep sound in the jungle : %s", data.data)
        bougerPointeur(data.data)

    # On souscrit au topic nomme "chatter".  On va recevoir des string.  La fonction qui va le traiter se nomme callback.
    rospy.Subscriber("topic_actu_reussi_avancer", String, callback)
    # On boucle a l'infini.  Seul le callback sera appele sur reception d'un message. 

    while True:
        getToutAutour()
        sendStringMap()
        sendPosition()


    
        
