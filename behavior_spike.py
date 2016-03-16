#!/usr/bin/env python
import os, sys
import time

print "Starting SPIKE Robot..."

modeVerbose = 1
modeSilencieux = 2
mode = modeVerbose

if mode == modeVerbose:
	print "Starting ROSCORE"	
os.system("roscore")
time.sleep(3)

if mode == modeVerbose:
	print "Starting Sound_play"	
os.system("roslaunch sound_play soundplay_node.py")
time.sleep(3)

#if mode == modeVerbose:
#	print "Starting PocketSphinx"	
#os.system("roslaunch reconnaissanceVoix pocket_sphinx.py")
#time.sleep(3)

if mode == modeVerbose:
	print "Starting Spike's attention behavior..."	
os.system("rosrun spike behavior_attention.py")

print "Completed!  Spike is running!"

