#!/usr/bin/env python

'''
Filename: SNN.py
Author: Jean-Sebastien Dessureault
Date created: 01/06/2016
Python version 2.7
'''

import rospy
import numpy as np
from brian2 import *
from std_msgs.msg import String
import matplotlib.pyplot as plt
import time
import pickle
from graphics import plotVoltTemps, plotOutputNeurons, plotSpikeTemps, plotPopulationRate, plotConnectivity, displaySpikeMonitorInfo

# Registering node to ROS
rospy.init_node('node_spiking_neural_networks', anonymous=True)
rospy.loginfo("Behavior SNN - Spiking Neural Network")

# Retriving parameters from launcher
SNNname = rospy.get_param("/SNN/SNNname")
verbose = rospy.get_param("/SNN/verbose")  
mode = rospy.get_param("/SNN/mode")
nb_learn = rospy.get_param("/SNN/nb_learn")
input_neurons = rospy.get_param("/SNN/input_neurons")
output_neurons = rospy.get_param("/SNN/output_neurons")
hidden_neurons = rospy.get_param("/SNN/hidden_neurons")
hidden_layers = rospy.get_param("/SNN/hidden_layers")
synapse_weight = str(rospy.get_param("/SNN/synapse_weight"))
tau = rospy.get_param("/SNN/tau") * ms
threshold_value = rospy.get_param("/SNN/threshold")
refractory_value = rospy.get_param("/SNN/refractory") * ms
reset_value = rospy.get_param("/SNN/reset")
simulation_lenght = rospy.get_param("/SNN/simulation_lenght") * ms
equation = rospy.get_param("/SNN/equation")
graph = rospy.get_param("/SNN/graph")
pathSNN = rospy.get_param("/SNN/path")
 
# Displaying parameters to console
rospy.loginfo("Parameters received from launcher:")
rospy.loginfo("SNNname:" + SNNname)
rospy.loginfo("verbose:" + str(verbose))
rospy.loginfo("mode:" + str(mode))
rospy.loginfo("nb_learn:" + str(nb_learn))
rospy.loginfo("graph:" + str(graph))
rospy.loginfo("input_neurons:" + str(input_neurons))
rospy.loginfo("output_neurons:" + str(output_neurons))
rospy.loginfo("hidden_neurons:" + str(hidden_neurons))
rospy.loginfo("hidden_layers:" + str(hidden_layers))
rospy.loginfo("synapse_weight" + synapse_weight)
rospy.loginfo("tau:" + str(tau))
rospy.loginfo("threshold:" + str(threshold_value))
rospy.loginfo("refractory:" + str(refractory_value))
rospy.loginfo("simulation_lenght:" + str(simulation_lenght))
rospy.loginfo("equation:" + equation)
rospy.loginfo("path:" + pathSNN)

# Filenames and path where the trained SNN and pickle files will be saved. 
initFile = SNNname + "_initialized"
learnedFile = SNNname + "_learned"

# Mode
LEARNING = 0
RUN = 1

# Global variable that receives the frames from the topic.
frames_in = []

# Callback triggered when there is a new message on the topic.
def callbackReceiveMsgFromTopic(data):
    #rospy.loginfo("Le callback a recu: %s", data.data)
    if float(data.data) != 0.0:
        frames_in.append(float(data.data))
     
def SNN():

    if verbose and mode == LEARNING:
        rospy.loginfo("SNN LEARNING (train) mode")
    if verbose and mode == RUN:
        rospy.loginfo("SNN RUN mode")
        
    start_scope()
    
    # Definition des variables 
    if verbose:
        rospy.loginfo("Creating SNN...")
    
    # SNN Creation    
    neurons = []                # Array of neuronGroup
    synapses = []               # Array of synapses
    INPUT_LAYER = 0             # input layer index
    OUTPUT_LAYER = hidden_layers + 2 - 1    # Output layer index:  Hidden layer +  1 input layer + 1 output layer (- 1 because the index starts at 0).
    postsynaptic = "v_post += " + synapse_weight    # Synapse weight
    
    # Creation of the neurons and synapses structures
    for layer in range(INPUT_LAYER,OUTPUT_LAYER+1): 
        # Neurons
        if layer == INPUT_LAYER:
            neurons.append(NeuronGroup(input_neurons, equation, threshold=threshold_value, reset=reset_value, refractory=refractory_value))
            if verbose: 
                print "Assigning INPUT layer: " + str(layer)
        if layer == OUTPUT_LAYER: 
            neurons.append(NeuronGroup(output_neurons, equation, threshold=threshold_value, reset=reset_value, refractory=refractory_value))
            if verbose: 
                print "Assigning OUTPUT layer: " + str(layer)
        if layer < OUTPUT_LAYER and layer > INPUT_LAYER:
            neurons.append(NeuronGroup(hidden_neurons, equation, threshold=threshold_value, reset=reset_value, refractory=refractory_value))
            if verbose: 
                print "Assigning HIDDEN layer: " + str(layer)
        # Synapses
        if layer > INPUT_LAYER:
            synapses.append(Synapses(neurons[layer-1], neurons[layer], on_pre=postsynaptic))           
            synapses[layer-1].connect()
            if verbose: 
                print "Assigning SYNAPSES between layer: " + str(layer-1) + " and layer " + str(layer)
    
    # Creation of the monitors
    stateInput = StateMonitor(neurons[INPUT_LAYER], 'v', record=True)
    stateOutput = StateMonitor(neurons[OUTPUT_LAYER], 'v', record=True)
    spikeMonitor = SpikeMonitor(neurons[OUTPUT_LAYER])
    #popRateMonitor = PopulationRateMonitor(HiddenGroup1)
    
    # Integrtion of each component in the network. 
    net = Network(collect())
    net.add(neurons)
    net.add(synapses)

    # Save the state if LEARNING mode. 
    if mode == LEARNING:
        if verbose:
            rospy.loginfo("Saving initialized SNN...")
        net.store(initFile, pathSNN+initFile+".dat")

    # Main loop.  Inifite if RUN mode.   Quit after X iteration if LEARNING mode. 
    theExit = False
    while not theExit: 
        # Start the cycle and the timer.
        rospy.loginfo("BEGINNING OF CYCLE")
        start = time.time()
        time.clock()
        
        # If RUN mode, restore the learned SNN. 
        if mode == RUN:
            if verbose:
                rospy.loginfo("Restoring previously learned SNN...")
            net.restore(learnedFile, pathSNN+learnedFile+".dat")
        
        # When the callback function has received all the input neurons, assign those neurons to the input layer. 
        frames_assignation = frames_in
        #print len(frames_assignation)
        #print input_neurons
        if len(frames_assignation) >= input_neurons:    
            if verbose:
                rospy.loginfo("Assigning input neurons...")
            
            for i in range(0,input_neurons): 
                neurons[INPUT_LAYER].v[i] = frames_assignation[i] 
                if verbose:
                    rospy.loginfo("neuron : " + str(i) + " voltage: " + str(neurons[INPUT_LAYER].v[i]))  

            
            # Simulation execution
            if verbose:
                rospy.loginfo("Simulation execution...")   
        
            if verbose:
                net.run(simulation_lenght, report='text', report_period=1*second)
            else:
                net.run(simulation_lenght)
            del frames_in[:] 
            # If LEARNING mode, store the learned SNN in a file.  
            if mode == LEARNING:
                # If it was the last train data, then exit. 
                global nb_learn
                nb_learn = nb_learn - 1
                if nb_learn == 0:
                    theExit = True       

            # If RUN mode, send the data to some pickle files
            if mode == RUN:
                # Send output_neurons on topics
                if verbose:
                    rospy.loginfo("Send the result to the topic...")              
                pickleOutput_v = open(pathSNN+learnedFile+"_v.pk1", 'wb')
                pickleOutput_t = open(pathSNN+learnedFile+"_t.pk1", 'wb')
                # Send the voltage and time of the output state monitor. (contains spikes)
                pickle.dump(stateOutput.v, pickleOutput_v)
                pickle.dump(stateOutput.t/ms, pickleOutput_t)
                pickleOutput_v.close()
                pickleOutput_t.close()
                # Display some basic information to the console. 
                displaySpikeMonitorInfo(spikeMonitor)

        # If we asked for a graph, then exit afterward. 
        if graph == True:
            theExit = True

        # End of the cycle
        rospy.loginfo("END OF CYCLE")
        elapsed = time.time() - start
        print "Cycle time: %.2f" % (elapsed)
 
        # Show the graphics
        if graph == True:
            if verbose:
                rospy.loginfo("Display graphics...")
            plotVoltTemps(stateInput, 0, input_neurons)
            plotSpikeTemps(spikeMonitor)
            for k in range (0, len(synapses)):
                plotConnectivity(synapses[k])
            #plotPopulationRate(popRateMonitor)
            plotOutputNeurons(stateOutput, 0, output_neurons)
            #profiling_summary(show=5)            

    # If LEARNING mode, store the learned SNN in a file.  
    if mode == LEARNING:
        if verbose:
            rospy.loginfo("Saving SNN after training...")  
        net.store(learnedFile, pathSNN+learnedFile+".dat") 
        net.restore(initFile, pathSNN+initFile+".dat")

if verbose:
    rospy.loginfo("Subscribe to the callbacks (input neurons)...")
rospy.Subscriber("topic_in_SNN_"+SNNname, String, callbackReceiveMsgFromTopic)

# Call the SNN system
SNN()

