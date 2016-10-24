#!/usr/bin/env python
import matplotlib.pyplot as plt
import os
import numpy as np
import rospy
from std_msgs.msg import String
tableau = []
posRobot = []
dessin = False
# Enregistrement du noeud ROS a ROSCORE. 
rospy.init_node('console', anonymous=True)

def callBackPosition(data):
    #print "callBackPosition: " + data.data
    tableau = np.matrix(data) 
    print tableau

def callbackTableau(data):
    #print "callBackTableau: " + data.data
    #posRobot = data
    #global dessin
    #if dessin == True:
    #    plt.clf() 
    #print posRobot
    #print tableau
    #plt.plot(tableau, 'ro')
    #plt.plot(posRobot)
    #plt.axis([0, 10, 0, 15])
    #if dessin == True:        
    #    plt.show()
    #else:
    #    plt.draw()               
    #dessin = True
    
    os.system('clear')
    tableau = data.data.split(";")
    for i in tableau:
        print i
    
def callbackConsole(data):
    print "callBackConsole: " + data.data

    
rospy.Subscriber("topic_ia_ecrireconsole", String, callbackConsole)
rospy.Subscriber("pub_geosphere_stringmap", String, callbackTableau) 
rospy.Subscriber("pub_geosphere_position", String, callBackPosition) 

print "Console en attente..."

# On boucle a l'infini.  Seul le callback sera appele sur reception d'un message. 
rospy.spin()

