#!/usr/bin/env python
import rospy
import numpy as np
from brian2 import *
import matplotlib.pyplot as plt
      
# Recuperation des neurones de sorties
# spikeMonitor.num_spikes: Total des spikes
# spikeMonitor.count: Total des spikes / par neurones
# spikeMonitor.count: Total des spikes / pour neurones i
# spikeMonitor.i: Tableau des spikes enregistres

def displaySpikeMonitorInfo(spikeMonitor):
    print "Information sur les spikes en SORTIE"
    print "Nombre total de spikes------------------: " + str(spikeMonitor.num_spikes)
    #nb = len(spikeMonitor.count)
    #print "Total des spikes par neurones: " + str(nb)
    #for j in range(0,nb):
    #    print "spike: " + str(j) + " " + str(spikeMonitor.count[j])

def plotVoltTemps(statemon, titre, debut, fin):
    title(titre + " (Neurones de " + str(debut) + " a " + str(fin) + ")")
    for j in range(debut,fin):
        plt.plot(statemon.t/ms, statemon.v[j])
    plt.ylabel('voltage')
    plt.xlabel('Temps m/s')
    plt.show()
    
def plotOutputNeurons(stateOutput, debut, fin):
    title("Difference de potentiel final des neurones de SORTIE")
    for j in range(debut,fin):
        plt.plot(stateOutput.t/ms, stateOutput.v[j])
    plt.ylabel('voltage')
    plt.xlabel('Temps en ms')
    plt.show()
    

def plotSpikeTemps(spikemon):
    title("Decharges des neurones de SORTIE en fonction du temps")
    plt.plot(spikemon.t/ms, spikemon.i, '.k')
    plt.ylabel('Spikes')
    plt.xlabel('Temps m/s')
    plt.show()
    
def plotPopulationRate(popratemon):
    title("Population Rate des spikes")
    plt.plot(popratemon.t/ms, popratemon.rate/Hz)
    plt.xlabel('Temps m/s')
    plt.ylabel('Rate/Hz')
    plt.show()

def plotConnectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10,4))
    #subplot(111)
    plot(np.zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(np.ones(Nt), arange(Nt), 'ok', ms=10)
    for i,j in zip(S.i, S.j):
        plot([0,1], [i,j], '-k')
    xticks([0,1], ['Source', 'Target'])
    ylabel("Neuron index")
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    title("Connectivite des couches de neurones et synapses")
    plt.show()

