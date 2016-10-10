#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
tableau = []
tableau2 = []

info = [1,1,1,1,1,1,1,1,1,1,1,1,1],[1,2,3,4,5,6,7,8,9,11,13,15,16]

def fillMap(data):
    tableau = np.matrix(data)
        
def drawMap(carte):
    print(np.matrix(carte))
    
    
def callback():
    print "numpy.matrix 1"
    drawMap(info)
    print "matplotlib 1"
    plt.plot(info)
    plt.axis([0,5,0,5])
    plt.show()

fillMap(info)    
print "info"
print info
print "tableau"
print tableau

print "startCallback"
#callback()

plt.plot(info,'ro')
plt.plot([3],[3])
plt.axis([0,6,0,20])
plt.show()
