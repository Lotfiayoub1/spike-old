#!/usr/bin/env python

import roslib
import rospy, os, sys
import pygtk
pygtk.require('2.0')
import gtk
from std_msgs.msg import String

rospy.init_node('node_humeur', anonymous=True)
rospy.loginfo("behavior_humeur")

modeTest = 1
modeRecoitSignal = 2

mode = modeRecoitSignal
verbose = True


delais = 3000	# va rafraichir toutes les x millisecondes.

# Code vient d'ici:  http://www.pygtk.org/pygtk2tutorial/sec-Images.html#idp5575312 

class ExpressionFaciale:

	if verbose == True:
		rospy.loginfo("Definition de la classe.")

	etatPensee = "Reflexion"
	etatHumeur = "Neutre"

	imageReflexion = gtk.Image()
	imageHumeur = gtk.Image()
	canevas = gtk.Fixed()

	pix_pensee_neutre = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeNeutre.gif")
	pix_pensee_reflexion1 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion1.gif")
	pix_pensee_reflexion2 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion2.gif")
	pix_pensee_reflexion3 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion3.gif")
	pix_pensee_reflexion4 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/pensees/penseeReflexion4.gif")

	pix_humeur_neutre = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/images/humeurs/humeurNeutre.gif")
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
		gkt.main_quit()

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
				rospy.loginfo("Timer modeRecoitSignal:Les etat sont changes dans les callback.")

		self.rafraichir()
	
	def rafraichir(self):

		if verbose == True:
			rospy.loginfo("Redefinition de l'expression faciale...")

		# On ajuste la pensee selon l'etat	
		if self.etatPensee == "Reflexion":
			self.imageReflexion.set_from_animation(self.pix_pensee_neutre)
		if self.etatPensee == "Neutre":
			self.imageReflexion.set_from_animation(self.pix_pensee_reflexion1)
		self.imageReflexion.show()

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

		# Declaration du timer
		gtk.timeout_add(delais, self.my_timer)

		if verbose == True:
			rospy.loginfo("Fin de la redefinition de l'expression faciale...")


	def __init__(self):

		# JSD: Voir les autres proprietes de Window
		# Mon ecran a 1280X1024
		# Haut: 1280X512:  Reflexion
		# Bas: 1280X512: Figure

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.set_border_width(0)
		self.window.set_title("SPIKE")
		#self.window.fullscreen()
		self.window.resize(1280, 1024)
		self.window.show()

		self.canevas.set_size_request(1280, 1024)
		self.imageHumeur.set_from_animation(self.pix_humeur_neutre)
		self.imageReflexion.set_from_animation(self.pix_pensee_neutre)
		self.canevas.put(self.imageReflexion, 0, 0)
		self.canevas.put(self.imageHumeur, 0, 256)
		self.window.add(self.canevas)
		self.canevas.show()
		self.rafraichir()


	def main(self):
		gtk.main()
	
if __name__ == "__main__":

		if verbose == True:
			rospy.loginfo("Behavior_humeur: Main")
	
		if mode == modeRecoitSignal:
			if verbose == True:
				rospy.loginfo("Mode RecoiSignal... Definition des callbacks.")
	
			def callbackPensee(data):
				if verbose:
					rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
				expression.etatPensee = data.data	
		
			def callbackHumeur(data):
				if verbose:
					rospy.loginfo(rospy.get_caller_id() + " Message recu: %s", data.data)
				expression.etatHumeur = data.data
	
			if verbose == True:
				rospy.loginfo("Mode RecoiSignal... Enregistrement des Subscribers.")
		
			# On s'inscrit aux topics
			rospy.Subscriber("topic_humeur", String, callbackHumeur)
			rospy.Subscriber("topic_pensee", String, callbackPensee)
	
		if verbose == True:
			rospy.loginfo("Appel de la definition de l'expression faciale.")
	
		expression = ExpressionFaciale()
		expression.main()
	
		# Puisqu'on attend un signal, il ne faut pas quitter
		# L'instruction suivante permet de rester dans le programme
#		rospy.spin()
		
	
	
	



