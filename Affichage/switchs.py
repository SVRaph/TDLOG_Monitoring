#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.

from outils_web import *


#--------------------------------------------------
# Plan des switchs

def page_switch():
    # Génération du code HTML de la page
    codeHTML=''
    with open("codeHTML/switch.html", 'r') as code:
        for phrase in code:
            if "|***InsertionPlan***|" not in phrase:
                codeHTML += phrase
            else:
                # Sinon, c'est l'endroit où insérer l'arborescence des switch
                with open("Scripts/switchs_connus_reponse_ping.txt", 'r') as tmp:
                    tmp = tmp.readlines()
                    reponse = []
                    for ligne in tmp:
                        ligne = ligne.strip('\n')
                        reponse.append(ligne.split(' '))
                    sw.routeur.reponseSwitch(reponse)
                codeHTML += sw.routeur.afficheHTML("","")
        return codeHTML

print standard_title
print page_switchs()
print standard_end
