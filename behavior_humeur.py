#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Float32
import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

rospy.init_node('node_humeur', anonymous=True)
rospy.loginfo("behavior_humeur")

verbose = True

volts = []
times = []
iTime = 0

# Plot
# Petit ecran Spike: 600 X 480
temps_max = 600
img_neutre = mpimg.imread("/home/pi/ros_catkin_ws/src/spike/src/spike/images/humeurs/humeurNeutre.png")
mpl.rcParams['toolbar'] = 'None'
figsize = mpl.rcParams['figure.figsize']
figsize[0] = 8
figsize[1] = 4.5
mpl.rcParams['figure.figsize'] = figsize

figure, ax = plt.subplots(2, sharex=True)
plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0, hspace=0.0)

line, = ax[0].plot(times,volts)
ax[0].set_ylim(-0.2,1.0)    # mv:  -0.5 a 1
ax[0].set_xlim(0,temps_max)    
ax[0].set_facecolor('black')
ax[1].set_facecolor('black')
ax[1].axis('off')
ax[1].imshow(img_neutre)

def update_line(data):
    print "update: " + str(len(volts)) + " " + str(len(times))
    line.set_ydata(volts)
    line.set_xdata(times) 
    return line, 

delais=100
ani = animation.FuncAnimation(figure, update_line, interval=delais)
plt.style.use('dark_background')
        
# Communication avec Behavior_chatbot
topic_attention_conversation = rospy.Publisher('topic_attention_conversation', String, queue_size=10)
topic_attention_conversation.publish("SPIKE PRET")
        
if verbose == True:
    rospy.loginfo("Definition des callbacks.")

def callbackHumeur(data):
    etatHumeur = data.data
    if verbose == True:
        rospy.loginfo("Humeur: %s", etatHumeur)

def callbackNeurones(data):
    global iTime
    #print "Callback neurones " + str(iTime)
    if iTime >= 600:
        del times[:]
        del volts[:]
        iTime = 0
    volts.append(data.data)
    times.append(iTime)
    iTime += 1
    
if verbose == True:
    rospy.loginfo("Enregistrement des Subscribers.")

# On s'inscrit aux topics
rospy.Subscriber("topic_humeur", String, callbackHumeur)
rospy.Subscriber('/topic_motor_volt_1', Float32, callbackNeurones)

if verbose == True:
    rospy.loginfo("Spin...")

plt.show()

rospy.spin()
