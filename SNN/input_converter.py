#!/usr/bin/env python

'''
Filename: input_converter.py
Author: Jean-Sebastien Dessureault
Date created: 19/05/2017
Python version 2.7
'''

import rospy
import numpy as np
from std_msgs.msg import *
from sensor_msgs.msg import *
import string

# Registering node to ROS
rospy.init_node('node_input_converter', anonymous=True)
rospy.loginfo("Input converter for SNN topics")

# Retriving parameters from launcher
verbose = rospy.get_param("/input_converter/verbose") 
SNNname = rospy.get_param("/input_converter/SNNname")
sensory_neurons = rospy.get_param("/input_converter/sensory_neurons")
p_topic = []
p_type = []
p_field = []
out_topic = []
for x in range (0, sensory_neurons):
    p_topic.append(rospy.get_param("/input_converter/input_topic_"+str(x+1))) 
    p_type.append(rospy.get_param("/input_converter/topic_type_"+str(x+1)))
    p_field.append(rospy.get_param("/input_converter/input_field_"+str(x+1)))

def callback(data, neuron_nb):
    #rospy.loginfo(data)
    field = eval("data"+p_field[neuron_nb])
    converted_value = float(field) 
    #rospy.loginfo("Le callback publie la valeur %f sur le topic.", converted_value)
    out_topic[neuron_nb].publish(str(converted_value))
    #print "Publie: " + str(converted_value) + " sur " + str(neuron_nb)
    
if verbose:
    rospy.loginfo("Mapping and converting topics for sensory inputs of the SNN.  Do NOT interrupt while SNN execute. ")

for x in range (0, sensory_neurons):
    rospy.Subscriber(p_topic[x], eval(p_type[x]) , callback, x)
    out_topic.append(rospy.Publisher('topic_in_SNN_'+SNNname+'_'+str(x+1), String, queue_size=10))
    #print "Declaration du topic " + str(x)

rospy.spin()
