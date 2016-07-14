#!/usr/bin/env python

import pyaudio
import numpy
import matplotlib.pyplot as plt

# Plusieurs exemples d'utilisation du son et pyaudio ici:
# www.programcreek.com/python/example/52624/pyaudio.PyAudio

# Initialisation des constantes
ROSBAG = 0
ROS = 1
TEST = 2

mode = ROSBAG
verbose = True
rosbag = True
printAfterRecord = False
plotAfterRecord = True

if mode == ROS or mode == ROSBAG:
    from std_msgs.msg import String
    import rospy
    rospy.init_node('node_saisie_son_ambiant', anonymous=True)
    rospy.loginfo("Behavior_saisie_son_ambiant")
    topic_son_ambiant = rospy.Publisher('topic_son_ambiant', String, queue_size=10)


frames = []

def cycleRecording():
       
    audio = pyaudio.PyAudio()
        
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    if verbose:
        print "Recording..."
        #print "Type of frames is " + str(type(frames))
    
    #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    for i in range(0, NOFFRAMES):
        data = stream.read(CHUNK)
        if (i%ECHANTILLON == 0): 
            #print type(data)
            # Si on est en mode ROS, on publie!    
            if mode == ROS or mode == ROSBAG:
                topic_son_ambiant.publish(data)        
            if mode == ROSBAG or mode == TEST:            
                decoded = numpy.fromstring(data, 'Int16')
                #print decoded
                frames.append(decoded)
    
    if verbose:
        print "Recording finished!"

   
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

def printAfterRecord():
    if printAfterRecord:
        mode = 2
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
        plt.ylabel('Spectre sonore')
        plt.xlabel('Frame #')
        plt.show()

        # Sans ROS
        #plot(frames)
        #xlabel('Frame #')
        #ylabel('d')
        #legend(loc="best")


# Constanstes enregistrement 
# Format Entier 16 bits
FORMAT = pyaudio.paInt16
# 1 seul canal pour mono, 2 pour stereo
CHANNELS = 1
# Frequence de 44100 ou 16000
RATE = 16000
# Nombre de frames lus par buffer (1024)
CHUNK = 16
#RECORD_SECONDS = 3
# Nombre de frames a lire
NOFFRAMES = 800    
# Pour ne prendre qu'une partie des donnees.  Permet d'alleger les donnees.
ECHANTILLON = 8   # On capture une valeur tous les x frames. 
 
if mode == ROS:
    print "MODE ROS"
    while True:
        cycleRecording()

if mode == TEST:
    print "MODE TEST"
    cycleRecording()
    printAfterRecord()
    plotAfterRecord()
    
if mode == ROSBAG:
    print "MODE ROSBAG"
    cycleRecording()
    printAfterRecord()
    plotAfterRecord()    


