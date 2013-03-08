#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()
print 'Content-type: text/html'
print
# Là commence votre code.

from outils import *
#standard_title, standard_end, str2html


# Page d'index laisse le choix entre un vers la page clubinfo.org et un lien vers la page accueil.html pour voter
def index():
    s='<p> Que cherches-tu ? : <br> <a href="http://clubinfo.enpc.org">le site du KI ?</a> <br> ou <br> <a href="/accueil.py">les votes pour la t&eacutel&eacute ?</a> <p>'    
    return s

print standard_title
print index()
print standard_end
