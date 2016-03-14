#!/usr/bin/env python

import roslib
import rospy, os, sys
import pygtk
pygtk.require('2.0')
import gtk

rospy.init_node('node_humeur', anonymous=True)
rospy.loginfo("behavior_humeur")

# Code vient d'ici:  http://www.pygtk.org/pygtk2tutorial/sec-Images.html#idp5575312 

class ExpressionFaciale:

	def expression(self, widget, data=None):
		print "expression"

	def delete_event(self, widget, event, data=None):
		print "delete event occured"
		return False

	def destroy(self, widget, data=None):
		print "destroy signal occured"
		gkt.main_quit()

	def __init__(self):

		# JSD: Voir les autres proprietes de Window
		# Mon ecran a 800X480
		# Haut: 800X80:  Reflexion
		# Bas: 800X400: Figure
	
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.set_border_width(0)
		self.window.set_title("SPIKE")
		#self.window.fullscreen()
		self.window.resize(800, 480)
		self.window.show()

		pixbufanim = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/reflexion/reflexion5.gif")
		imageReflexion = gtk.Image()
		imageReflexion.set_from_animation(pixbufanim)
		imageReflexion.show()

		pixbufanim2 = gtk.gdk.PixbufAnimation("/home/ubuntu/catkin_ws/src/spike/src/spike/reflexion/reflexion8.gif")
		imageHumeur = gtk.Image()
		imageHumeur.set_from_animation(pixbufanim2)
		imageHumeur.show()

		fixedHaut = gtk.Fixed()
		fixedHaut.set_size_request(800, 480)
		fixedHaut.put(imageReflexion, 0, 0)
		fixedHaut.put(imageHumeur, 0, 81)
		self.window.add(fixedHaut)
		fixedHaut.show()

	def main(self):
		gtk.main()
		return 0
	
if __name__ == "__main__":
	expression = ExpressionFaciale()
	expression.main()

