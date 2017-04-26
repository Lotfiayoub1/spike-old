#!/usr/bin/env python

import rospy, numpy, math
#import pygtk
#pygtk.require('2.0')
#from mpltools import style
import gtk

from std_msgs.msg import String
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
import matplotlib
from matplotlib.figure import Figure
from numpy import arange, sin, pi
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pickle
#matplotlib.use('TkAgg')

rospy.init_node('node_humeur', anonymous=True)
rospy.loginfo("behavior_humeur")

modeTest = 1
modeRecoitSignal = 2

mode = modeRecoitSignal
verbose = True

delais = 5000    # va rafraichir toutes les x millisecondes.

# Plot
temps_max = 150
figure = Figure(figsize=(1280,125))
figure.patch.set_facecolor('black')
ax = figure.add_subplot(111, facecolor='black')
line, = ax.plot(0,2)
ax.set_ylim(-0.2,1.0)    # mv:  -0.5 a 1
ax.set_xlim(0,temps_max)    
ax.set_axis_bgcolor('black')

class ExpressionFaciale:
    # Code vient d'ici:  http://www.pygtk.org/pygtk2tutorial/sec-Images.html#idp5575312
    if verbose == True:
        rospy.loginfo("Definition de la classe.")

    etatPensee = "Neutre"
    etatHumeur = "Neutre"
    etatStatut = "En attente..."

    envoieSpikePret = True
    # Communication avec Behavior_chatbot
    topic_attention_conversation = rospy.Publisher('topic_attention_conversation', String, queue_size=10)
        
    # Images et textes 
    imageReflexion = gtk.Image()
    imageHumeur = gtk.Image()
    imageFiller = gtk.Image()
    statut = gtk.TextView()
    statut.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
    statut.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
    texte = statut.get_buffer()
    texte.set_text(etatStatut)

    def update_line(data):

        print "Reading SNN data from pickle files."
        try:
            # Open the files (_v for voltage and _t for time) 
            pk1_v = open("/home/ubuntu/catkin_ws/src/spike/src/spike/SNN/learned/Son528Hz_learned_v.pk1", 'rb')
            pk1_t = open("/home/ubuntu/catkin_ws/src/spike/src/spike/SNN/learned/Son528Hz_learned_t.pk1", 'rb')
            #pk1_v = open("/home/ubuntu/catkin_ws/src/spike/src/spike/SNN/learned/Ambiance_learned_v.pk1", 'rb')
            #pk1_t = open("/home/ubuntu/catkin_ws/src/spike/src/spike/SNN/learned/Ambiance_learned_t.pk1", 'rb')
            # Load the data in some arrays
            data_v = pickle.load(pk1_v)
            data_t = pickle.load(pk1_t)   
            # Close the files     
            pk1_v.close()
            pk1_t.close()
            # Assing the data to the axes of the graph. 
            #data_v[0].insert(0,0)
            #data_v.insert(0, len(data_v))
            line.set_ydata(data_v[0])
            line.set_xdata(data_t)
        except:
            print "Error reading Pickle files"

        return line, 

    # Fonctions originales qui fonctionnent avec FuncAnimation
    #def update_line(data):
    #    print "update:" + str(data)
    #    line.set_ydata(data)
    #    return line, 

    #def data_gen():
    #    while True:
    #        yield numpy.random.rand(10)


    #ax.plot(t,s)
    plotCanevas = FigureCanvas(figure) 
 
    plt.show(block=False)
    ani = animation.FuncAnimation(figure, update_line, interval=delais)
 
    plt.style.use('dark_background')

    pix_filler = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/imageFiller.jpeg")
    imageFiller.set_from_animation(pix_filler)

    pix_pensee_neutre = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeNeutre.gif")
    pix_pensee_reflexion1 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion1.gif")
    pix_pensee_reflexion2 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion2.gif")
    pix_pensee_reflexion3 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion3.gif")
    pix_pensee_reflexion4 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion4.gif")

    pix_humeur_neutre = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurNeutre.jpeg")
    pix_humeur_joyeux = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurJoyeux.png")
    pix_humeur_fatigue = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurFatigue.gif")
    pix_humeur_triste = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurTriste.gif")
    pix_humeur_troll = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurTroll.png")
    pix_humeur_terminator = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurTerminator.png")



    def expression(self, widget, data=None):
        print "Expression faciale"

    def delete_event(self, widget, event, data=None):
        print "La fenetre ExpressionFaciale a ete detruite..."
        return False

    def destroy(self, widget, data=None):
        print "La fenetre ExpressionFaciale a ete detruite..."
        self.main_quit()

    def my_timer(self):

        if mode == modeTest:
            if verbose:
                rospy.loginfo("Timer modeTest: Change les etats...")

            if self.etatPensee == "Neutre":
                self.etatPensee = "Reflexion"
            else:
                self.etatPensee = "Neutre"
            if self.etatHumeur == "Neutre":
                self.etatHumeur = "Joyeux"
            else:
                self.etatHumeur = "Neutre"
        if mode == modeRecoitSignal:
            if verbose:
                rospy.loginfo("Timer modeRecoitSignal")

        self.rafraichir()

    def rafraichir(self):

        if verbose == True:
            rospy.loginfo("Redef. Pensee: " + self.etatPensee + " Humeur: " + self.etatHumeur )

        # Execute ce code UNE fois, au debut.  ChatBot - Spike est pret!
        if self.envoieSpikePret == True:
            self.envoieSpikePret = False
            if verbose:
                rospy.loginfo("Envoie le message que Spike est pret au chatbot.")
            self.topic_attention_conversation.publish("SPIKE PRET")

        # On ajuste la pensee selon l'etat
        if self.etatPensee == "Reflexion":
            self.imageReflexion.set_from_animation(self.pix_pensee_reflexion1)
        if self.etatPensee == "Neutre":
            self.imageReflexion.set_from_animation(self.pix_pensee_neutre)
        self.imageReflexion.show()
        # On reinitialise pour le prochain rafraichissement
        self.etatPensee = "Neutre"

        # On ajuste l'humeur selon l'etat
        if self.etatHumeur == "Neutre":
            self.imageHumeur.set_from_animation(self.pix_humeur_neutre)
        if self.etatHumeur == "Joyeux":
            self.imageHumeur.set_from_animation(self.pix_humeur_joyeux)
        if self.etatHumeur == "Triste":
            self.imageHumeur.set_from_animation(self.pix_humeur_triste)
        if self.etatHumeur == "Fatigue":
            self.imageHumeur.set_from_animation(self.pix_humeur_fatigue)
        if self.etatHumeur == "Troll":
            self.imageHumeur.set_from_animation(self.pix_humeur_troll)
        if self.etatHumeur == "Terminator":
            self.imageHumeur.set_from_animation(self.pix_humeur_terminator)
        self.imageHumeur.show()
        # On reinitialise pour le prochain rafraichissement
        self.etatHumeur = "Neutre"

        # mise a jour du message a ecran
        self.texte.set_text(self.etatStatut)
        self.statut.set_buffer(self.texte)
        self.statut.show()
        # On reinitialise pour le prochain rafraichissement
        self.etatStatut = ""

        # Declaration du timer
        gtk.timeout_add(delais, self.my_timer)

        self.plotCanevas.show()
        
        #if verbose == True:
        #    rospy.loginfo("Fin de la redefinition de l'expression faciale...")


    def __init__(self):

        # JSD: Voir les autres proprietes de Window
        # Mon ecran a 1280X1024
        # Haut: 1280X512:  Reflexion
        # Bas: 1280X512: Figure

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(1)
        self.window.set_title("SPIKE")
    
        #self.window.fullscreen()
        self.window.resize(1280, 1024)
        
        #fixed = gtk.Fixed()
        #fixed.set_size_request(1280, 1024)
        self.imageHumeur.set_from_animation(self.pix_humeur_neutre)
        self.imageReflexion.set_from_animation(self.pix_pensee_neutre)
        #self.canevas.put(self.imageReflexion, 0, 0)

        #fixed.put(self.plotCanevas,0,0)
        #fixed.put(self.imageHumeur, 0, 256)
        #fixed.put(self.statut, 100, 50)
        #self.plotCanevas.show()
        #fixed.show()
     
        #self.window.add(self.imageHumeur)
        #self.window.add(self.statut)
        
        vbox = gtk.VBox(False, 0)
        vbox.pack_start(self.plotCanevas)
        vbox.pack_start(self.imageHumeur, False, False)
        vbox.pack_start(self.imageFiller, False, False)
        vbox.pack_start(self.statut)

        self.window.add(vbox)
        self.window.show_all()
        self.rafraichir()


    def main(self):
        gtk.main()

if __name__ == "__main__":

        if verbose == True:
            rospy.loginfo("Behavior_humeur: Main")

        if mode == modeRecoitSignal:
            if verbose == True:
                rospy.loginfo("Mode RecoiSignal... Definition des callbacks.")

            def callbackHumeur(data):
                expression.etatHumeur = data.data
                if verbose == True:
                    rospy.loginfo("Humeur: %s", expression.etatHumeur)

            def callbackStatut(data):
                expression.etatStatut = data.data
                if verbose == True:
                    rospy.loginfo("Statut: %s", expression.etatStatut)

            # Ne sert plus depuis que l'on recoit la pensee avec un fichier pickle. 
            def callbackPensee(data):
                global temps, temps_max
                global frames_y, frames_x
                if verbose:
                    rospy.loginfo(rospy.get_caller_id() + "Le callback a recu: %s", data.data)  
                decoded = numpy.fromstring(data.data)   # Default datatype: float
                frame_y = decoded
                frame_x = numpy.zeros(len(decoded))
            
            if verbose == True:
                rospy.loginfo("Mode RecoiSignal... Enregistrement des Subscribers.")

            # On s'inscrit aux topics
            rospy.Subscriber("topic_humeur", String, callbackHumeur)
            rospy.Subscriber("behavior_ecoute/output", String, callbackStatut)
            

        if verbose == True:
            rospy.loginfo("Appel de la definition de l'expression faciale.")

        expression = ExpressionFaciale()
        expression.main()








