#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.

from outils_web import *


#--------------------------------------------------
# Page d'index

def page_index():
    # Génération du code HTML de la page
    codeHTML=''
    with open("codeHTML/index.html", 'r') as code:
        code=code.readlines()
        for phrase in code:
            if "|***DHCPsurlereseau***|" not in phrase:
                codeHTML+=phrase
            else:
                with open("Scripts/dhcp_rogue.txt",'r') as dhcp_rogue:
                    presence = dhcp_rogue.readlines()[0][0]
                    if presence=="1":
                        codeHTML+='<h2><font color="red">/!\\ Pr&eacutesence d\'un autre DHCP sur le r&eacuteseau /!\\</font></h2>'
    return codeHTML

print standard_title
print page_index()
print standard_end
