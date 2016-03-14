#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
import pyaudio
import wave
import pocketsphinx
import sphinxbase

from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_ecoute', anonymous=True)
rospy.loginfo("Behavior_ecoute")

francais = 1
anglais = 2

hmdir = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/"
lmd = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/5202.lm"
dictd = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/5202.dic"

langue = francais

print "1"

texte = 'espeak "Bonjour, je suis Spike le robot. Je vous ecoute..." -v french -s 150 -p 20' 
print texte
#os.system(texte)

def decodeSpeech(hmmd, lmdir, dictp, wavefile) :

	speechRec = ps.Decoder(hmm = hmmd, lm = lmdire, dict = dictp)
	waveFile = file(wavfile, 'rb')
	wavFileseek(44)
	speechRec.decode_raw(waveFile)
	result = speechRec.get_hyp()

	return result[0] 
	
#CHUNK = 1024
CHUNK = 512
#FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paALSA
CHANNELS = 1
RATE = 16000
#RATE = 44100
RECORD_SECONDS = 10

noEntree = 1
while True:
	print "2"
	fn = "entree"+str(noEntree)+".wav"
	print fn
	p = pyaudio.PyAudio()
	print "3"
	#stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
	#print ("* Recording")
	#frames = []
	#print str(RATE / CHUNK * RECORD_SECONDS) + " size \n"
	#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	#	print "3"
	#	data = stream.read(CHUNK)
	#	print "4"
	#	frames.append(data)
	#print ("* Done recording")
	#stream.stop_stream()
	#stream.close()
	#print "5"
	#wf = wave.open(fn, 'wb')
	#print "6"
	#wf.setnchannels(CHANNELS)
	#print "7"
	#wf.setsampwidth(p.get_sample_size(FOMRAT))
	#print "8"
	#p.terminate()
	#wf.setframerate(RATE)
	#print "9"
	#wf.writeframes(b''.join(frames))
	#print "10"
	#wf.close()
	#wavefile = fn
	#print "10"
	#recognised = decodeSpeech(hmdir, lmd, dictd, wavfile)
	#print "11"
	#print "Texte reconnu: "  + recognised
	#entree = recognised

	#reponse = k.respond(entree)
	print reponse
	#texte = 'espeak "' + reponse + '" -v french -s 150 -p 20' 
	#print texte
	#os.system(texte)

