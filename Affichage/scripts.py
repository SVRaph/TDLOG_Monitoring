#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.
from outils_web import *
import cgi

def page_scripts():
    codeHTML = ''
    info = cgi.FieldStorage()
    if "Test_IP_connues" in info:
        codeHTML += "<p>Le script testant les r&eacuteponses de l'ensemble des switchs du r&eacuteseau a bien &eacutet&eacute &eacutex&eacutecut&eacute.<p>"
        subprocess.call('Scripts/Test_IP_connues')
    if "ping_IP" in info:
        if "adresseIP" in info:
            codeHTML += "<h2>Commande <i>ping " + str(info["adresseIP"]) + "</i></h2><p>"
            subprocess.call(['Scripts/ping_IP',info["adresseIP"]])
            with open("Scripts/pingIP.txt",'r') as pingIP:
                codeHTML += str(pingIP.readlines()[0].strip('\n')) + "</p>"
    codeHTML += '<p><a href="index.html">Retour &agrave l\'accueil</a></p>'
    return codeHTML

print standard_title
print page_scripts()
print standard_end
