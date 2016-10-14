#!/usr/bin/env python
import rospy
import pyaudio
import numpy
import matplotlib.pyplot as plt
import time
import rospy
from std_msgs.msg import String
    

# Plusieurs exemples d'utilisation du son et pyaudio ici:
# www.programcreek.com/python/example/52624/pyaudio.PyAudio

# Initialisation des constantes
ROSBAG = 0
ROS = 1
TEST = 2

# Initialisation des variables
mode = ROS
verbose = True

# Constanstes enregistrement 
# Format Entier 16 bits
FORMAT = pyaudio.paInt16
# 1 seul canal pour mono, 2 pour stereo
CHANNELS = 1
# Frequence de 44100 ou 16000
RATE = 16000
# Nombre de frames lus par buffer (1024)
CHUNK = 50   # 16
#RECORD_SECONDS = 3
# Nombre de frames a lire (800)
NOFFRAMES = 10000   
# Pour ne prendre qu'une partie des donnees.  Permet d'alleger les donnees.
ECHANTILLON = 1   # On capture une valeur tous les x frames. (8)
 
rospy.init_node('node_saisie_son_ambiant', anonymous=True)
rospy.loginfo("Behavior_saisie_son_ambiant")

if mode == ROS or mode == ROSBAG:
    topic_son_ambiant = rospy.Publisher('topic_in_SNN_SonGamma', String, queue_size=100)

frames = []

def cycleRecording():
      
    rospy.loginfo("BEGINNING OF CYCLE")
    start = time.time()
    time.clock()
        
    audio = pyaudio.PyAudio()
        
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    if verbose:
        rospy.loginfo("Recording...")
      
    #print "Type of frames is " + str(type(frames))

    r = rospy.Rate(500) #  hz
    for i in range(0, NOFFRAMES):
        data = stream.read(CHUNK)
        # Si on est en mode ROS, on publie!    
        decoded = numpy.fromstring(data, 'Int16')
        # Trouve la moyenne des sons lus. 
        somme = 0.0
        for j in range(0, CHUNK):
            somme = somme + decoded[j]
        moyenne = somme / CHUNK
        #for j in range(0, len(decoded)):
        #    print str(i) + " " + str(decoded[j])
        if mode == ROS or mode == ROSBAG:
            tmp = float(moyenne) + float(2000) # float(32767.0)  
            normalized = tmp / float(4000) # float(65535.0)
            #print str(i) + " decoded: " + str(float(moyenne)) + " normalized: " + str(float(normalized))
            topic_son_ambiant.publish(str(float(normalized)))  
            if verbose:    
                printIntensite(normalized)
        if mode == ROSBAG or mode == TEST:            
            frames.append(decoded)
        r.sleep()
   
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    rospy.loginfo("END OF CYCLE")
    elapsed = time.time() - start
    print "cycle: %.2f" % (elapsed)

def printIntensite(intensite):
    strToDisplay = ""
    while intensite > 0:
        strToDisplay = strToDisplay + "#####"
        intensite = intensite - 0.1   
    print strToDisplay


def printAfterRecord():
    if printAfterRecord:
        if mode == 1:     
            print "Affichage des frames lus."
            for i in range(len(frames)):
                print frames
        if mode == 2:
            print "Sommaire"
            print "Nombre de frames: " + str(len(frames))
            print "Dernier frame:"
            print frames[len(frames)-1]

def plotAfterRecord():
    # Convertir ce bout de code pour matplotlib (pour executer en ROS.)
    if plotAfterRecord:
        plt.plot(frames)
        plt.ylabel('Signal sonore')
        plt.xlabel('Frame #')
        plt.show()

if mode == ROS:
    print "MODE ROS"
    while True:
        cycleRecording()

if mode == TEST:
    print "MODE TEST"    
    while True:
        cycleRecording()
        printAfterRecord()       
        plotAfterRecord()
    
if mode == ROSBAG:
    print "MODE ROSBAG"
    cycleRecording()
    printAfterRecord()
    plotAfterRecord()    
  
