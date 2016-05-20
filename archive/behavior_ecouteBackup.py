#!/usr/bin/env python
import roslib
import rospy, os, sys
from ctypes import *
from contextlib import contextmanager
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
#import sphinxbase.sphinxbase
#import pocketsphinx.pocketsphinx

rospy.init_node('node_Behavior_ecoute', anonymous=True)
rospy.loginfo("Behavior_ecoute")

verbose = True

francais = 1
anglais = 2
langue = francais

script_dir = os.path.dirname(os.path.realpath(__file__))
model_dir = "/home/ubuntu/catkin_ws/src/spike/src/spike/pocketsphinx/"

hmmd = os.path.join(model_dir, "fr_FR/")
lmdir = os.path.join(model_dir, "9477.lm")
dictp = os.path.join(model_dir, "9477.dic")

sys.stderr = open(os.path.join(script_dir, "stderr.log"), "a")
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    print "NO ASLA detected!"
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

con = Decoder.default_config()
con.set_string('-dict', dictp)	
con.set_string('-hmm', lmdir)
con.set_string('-logfn', '/dev/null')
decoder = Decoder(con)

if (verbose):
	print ("Test: Prononciation de hello: ", decoder.lookup_word("hello")) 

with noalsaerr():
	p = pyaudio.PyAudio()

if (verbose):
    print "OUVERTURE audio stream"

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
#stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

if (verbose):
    print "DEMARRAGE AUDIO STREAM"

stream.start_stream()
in_speech_bf = True

if (verbose):
    print "Avant Start UTT et boucle"

decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        try:
            if decoder.hyp().hypstr != '':
                print('Partial decoding result:', decoder.hyp().hypstr)
        except AttributeError:
            pass
        if decoder.get_in_speech():
            sys.stdout.write('.')
            sys.stdout.flush()
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                try:
                    if decoder.hyp().hypstr != '':
                        print('Stream decoding result:', decoder.hyp().hypstr)
                except AttributeError:
                    pass
                decoder.start_utt()
        else:
            break

decoder.end_utt()
if (verbose):
    print('An Error occured:', decoder.hyp().hypstr)
"""


# Communication avec Behavior_parle
#//topic_parle = rospy.Publisher('topic_parle', String, queue_size=10)

def decodeSpeech(hmmd, lmdir, dictp, wavefile) :

	speechRec = ps.Decoder(hmm = hmmd, lm = lmdire, dict = dictp)
	waveFile = file(wavfile, 'rb')
	wavFileseek(44)
	speechRec.decode_raw(waveFile)
	result = speechRec.get_hyp()

	return result[0] 
	

noEntree = 1
while True:
	
#	time.sleep(10)

#	texteCapte = "Spike"
#	topic_parle.publish(texteCapte)
#	if verbose:
#		rospy.loginfo("TexteCapte: " + texteCapte)


"""

