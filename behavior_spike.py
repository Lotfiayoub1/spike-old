#!/usr/bin/env python
os, sys
import time

print "Starting SPIKE Robbot..."

modeVerbose = 1
modeSilencieux = 2
mode = modeVerbose

if mode == modeVerbose:
	print "Starting ROSCORE"	
os.system("ROSCORE")
time.sleep(3)

if mode == modeVerbose:
	print "Starting Sound_play"	
os.system("ROSLAUCH sound_play soundplay_node.py")
time.sleep(3)

if mode == modeVerbose:
	print "Starting PocketSphinx"	
os.system("ROSLAUNCH reconnaissanceVoix pocket_sphinx.py")
time.sleep(3)

if mode == modeVerbose:
	print "Starting Spike's attention behavior..."	
os.system("ROSRUN spike behavior_attention.py")

print "Completed!  Spike is running!"

