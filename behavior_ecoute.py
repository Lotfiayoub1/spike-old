#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import pyaudio
import wave
import pocketsphinx
import sphinxbase

from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

rospy.init_node('node_ecoute', anonymous=True)
rospy.loginfo("Behavior_ecoute")

verbose = True

francais = 1
anglais = 2
langue = francais

hmdir = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/"
lmd = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/5202.lm"
dictd = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/5202.dic"

# Communication avec Behavior_parle
topic_parle = rospy.Publisher('topic_parle', String, queue_size=10)

def decodeSpeech(hmmd, lmdir, dictp, wavefile) :

	speechRec = ps.Decoder(hmm = hmmd, lm = lmdire, dict = dictp)
	waveFile = file(wavfile, 'rb')
	wavFileseek(44)
	speechRec.decode_raw(waveFile)
	result = speechRec.get_hyp()

	return result[0] 
	

noEntree = 1
while True:
	
	time.sleep(10)

	texteCapte = "Spike"
	topic_parle.publish(texteCapte)
	if verbose:
		rospy.loginfo("TexteCapte: " + texteCapte)



