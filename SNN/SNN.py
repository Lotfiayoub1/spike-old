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
sensory_neurons = rospy.get_param("/SNN/sensory_neurons")
motor_neurons = rospy.get_param("/SNN/motor_neurons")
inter_neurons = rospy.get_param("/SNN/inter_neurons")
inter_layers = rospy.get_param("/SNN/inter_layers")
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
rospy.loginfo("sensory_neurons:" + str(sensory_neurons))
rospy.loginfo("motor_neurons:" + str(motor_neurons))
rospy.loginfo("inter_neurons:" + str(inter_neurons))
rospy.loginfo("inter_layers:" + str(inter_layers))
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
    SENSORY_LAYER = 0             # input layer index
    MOTOR_LAYER = inter_layers + 2 - 1    # Output layer index:  Hidden layer +  1 input layer + 1 output layer (- 1 because the index starts at 0).
    postsynaptic = "v_post += " + synapse_weight    # Synapse weight
    
    # Creation of the neurons and synapses structures
    for layer in range(SENSORY_LAYER,MOTOR_LAYER+1): 
        # Neurons
        if layer == SENSORY_LAYER:
            neurons.append(NeuronGroup(sensory_neurons, equation, threshold=threshold_value, reset=reset_value, refractory=refractory_value))
            if verbose: 
                print "Assigning SENSORY layer: " + str(layer)
        if layer == MOTOR_LAYER: 
            neurons.append(NeuronGroup(motor_neurons, equation, threshold=threshold_value, reset=reset_value, refractory=refractory_value))
            if verbose: 
                print "Assigning MOTOR layer: " + str(layer)
        if layer < MOTOR_LAYER and layer > SENSORY_LAYER:
            neurons.append(NeuronGroup(inter_neurons, equation, threshold=threshold_value, reset=reset_value, refractory=refractory_value))
            if verbose: 
                print "Assigning INTER layer: " + str(layer)
        # Synapses
        if layer > SENSORY_LAYER:
            synapses.append(Synapses(neurons[layer-1], neurons[layer],  on_pre=postsynaptic))  
            #synapses.append(Synapses(neurons[layer-1], neurons[layer], 'w : 1', on_pre='v_post += w' ))          
            synapses[layer-1].connect() 
            if verbose: 
                print "Assigning SYNAPSES between layer: " + str(layer-1) + " and layer " + str(layer)
    
    # Creation of the monitors
    stateSensory = StateMonitor(neurons[SENSORY_LAYER], 'v', record=True)
    if inter_neurons > 0:
        stateInter = StateMonitor(neurons[SENSORY_LAYER + 1], 'v', record=True)
    stateMotor = StateMonitor(neurons[MOTOR_LAYER], 'v', record=True)
    spikeMonitor = SpikeMonitor(neurons[MOTOR_LAYER])
    
    # Integrtion of each component in the network. 
    if verbose: 
        print "Integration of each component in the network."
    net = Network(collect())
    net.add(neurons)
    net.add(synapses)

    #for iN in range(len(neurons)): 
    #    net.add(neurons[iN])
    #for iS in range(len(synapses)): 
    #    net.add(synapses[iS])   
    
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
            #net.restore(learnedFile, pathSNN+learnedFile+".dat")
        
        # When the callback function has received all the input neurons, assign those neurons to the input layer. 
        frames_assignation = frames_in

        if len(frames_assignation) >= sensory_neurons:    
            if verbose:
                rospy.loginfo("Assigning sensory neurons...")
            
            for i in range(0,sensory_neurons): 
                neurons[SENSORY_LAYER].v[i] = frames_assignation[i]  # Only v of the first simulation
                #neurons[SENSORY_LAYER].v = frames_assignation[i]    # All v's of the simulation
                #synapses[i].w[j] = frames_assignation[i]
                #neurons[SENSORY_LAYER].I[i] = frames_assignation[i] 
                if verbose:
                    #rospy.loginfo("synapse layer: " + str(i) + " neuron: " + str(j) + " poid synpatique: " + str(synapses[i].w[j])) 
                    rospy.loginfo("neuron : " + str(i) + " voltage: " + str(neurons[SENSORY_LAYER].v))  

            # Simulation execution
            if verbose:
                rospy.loginfo("Simulation execution...")   
        
            if verbose:
                net.run(simulation_lenght, report='text', report_period=0.2*second)
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
                pickle.dump(stateMotor.v, pickleOutput_v)
                pickle.dump(stateMotor.t/ms, pickleOutput_t)
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
            plotVoltTemps(stateSensory, "Difference de potentiel des neurones SENSORIELLES fonction du temps", 0, sensory_neurons)
            if inter_neurons > 0:
                plotVoltTemps(stateInter, "Difference de potentiel des INTER neurones fonction du temps",0, inter_neurons)
            plotVoltTemps(stateMotor, "Difference de potentiel des neurones MOTEUR fonction du temps",0, motor_neurons)
            plotSpikeTemps(spikeMonitor)
            for k in range (0, len(synapses)):
                plotConnectivity(synapses[k])
            #plotPopulationRate(popRateMonitor)
            #profiling_summary(show=5)            

    # If LEARNING mode, store the learned SNN in a file.  
    if mode == LEARNING:
        if verbose:
            rospy.loginfo("Saving SNN after training...")  
        net.store(learnedFile, pathSNN+learnedFile+".dat") 

if verbose:
    rospy.loginfo("Subscribe to the callbacks (input neurons)...")
rospy.Subscriber("topic_in_SNN_"+SNNname, String, callbackReceiveMsgFromTopic)

# Call the SNN system
SNN()

