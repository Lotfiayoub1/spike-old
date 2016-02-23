#!/usr/bin/env python	
import pygtk
pygtk.require('2.0')
import gtk

# Code vient d'ici:  http://www.pygtk.org/pygtk2tutorial/sec-Images.html#idp5575312 

class ExpressionFaciale:

# create the main window, and attach delete_event signal to terminating
# the application
# JSD: Voir les autres propriétés de Window
# Mon écran a 800X480
# Haut: 800X80:  Reflexion
# Bas: 800X400: Figure

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.connect("delete_event", self.close_application)
window.set_border_width(0)
window.show()

# a vertical box to hold the buttons
vbox = gtk.VBox()
vbox.show()
window.add(hbox)

pixbufanim = gtk.gdk.PixbufAnimation("monimage.png")
imageReflexion = gtk.Image()
imageRefelxion.set_from_animation(pixbufanim)
imageRefelxion.show()


# To display the image, we use a fixed widget to place the image
fixedHaut = gtk.Fixed()
fixedHaut.set_size_request(800, 80)
fixedHaut.put(imageReflexion, 0, 0)
window.add(fixedHaut)
fixedHaut.show()

fixedBas = gtk.Fixed()
fixedBas.set_size_request(800, 400)
fixedBas.put(imageHumeur, 81, 0)
window.add(fixedBas)
fixedBas.show()



def main():
gtk.main()
return 0
	
if __name__ == "__main__":
ExpressionFaciale()
main()
