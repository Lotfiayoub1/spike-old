#!/usr/bin/env python
import roslib
import rospy, os, sys
import time
import aiml
import pyaudio
import wave

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

rospy.init_node('node_aiml', anonymous=True)
rospy.loginfo("Behavior_aiml")

hmdir = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/"
lmd = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/5202.lm"
dictd = "/home/ubuntu/catkin_ws/src/reconnaissanceVoix/config/5202.dic"


def decodeSpeech(hmmd, lmdir, dictp, wavefile) :

	import pocketsphinx as ps
	import sphinxbase

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

soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()

#soundhandle.say('Testing the new A P I.')
#rospy.sleep(3)

#voix = soundhandle.voiceSound("Testing the new A P I.")
#voix.repeat()
#rospy.sleep(3)
#voix.stop()

francais = 1
anglais = 2

langue = francais

# L'objet Kernel est l'interface public pour l'interpreteur AIML. 
k = aiml.Kernel()

# Chargement de d'un fichier de contenu
# startup.xml charge tous les fichiers de contenu .aiml

if langue == anglais:
	# Version anglaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/en/startup.xml")
	k.respond("LOAD AIML ENGLISH")
else:
	# Version francaise
	k.learn("/home/ubuntu/catkin_ws/src/spike/src/spike/aiml/fr/startup.xml") 
	k.respond("LOAD AIML FRENCH")

texte = 'espeak "Bonjour, je suis Spike le robot. Je vous ecoute..." -v french -s 150 -p 20' 
print texte
#os.system(texte)

noEntree = 1
while True:
	print "1"
	#entree = raw_input("Spike chat BOT> ")
	fn = "entree"+str(noEntree)+".wav"
	print fn
	p = pyaudio.PyAudio()
	print "2"
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
	#print reponse
	#texte = 'espeak "' + reponse + '" -v french -s 150 -p 20' 
	#print texte
	#os.system(texte)
	#soundhandle.stsopAll()
	#soundhandle.say(reponse)


config = Decoder.default_config()
config.set_string('-hmm', hmdir)
config.set_string('-lm', lmd)
config.set_string('-dict', dictd)

decoder = Decoder(config)
decoder.start_utt()

stream = open('goforward.raw', 'rb')

while True:
	buf = stream.read(4046)
	if buf: 
		decoder.process_raw(buf, False, False)
	else:
		break
decoder.end_utt()
hypothesis = decoder.hyp()
print ('Meilleure hypothese: ', hypothesis.hypstr, " pointage: ", hypothesis.best_score, " indice de confiance: ", hypothesis.prob)
print ('Meilleur segement hypothese: ', [seg.word for seg in decoder.seg()])




