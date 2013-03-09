#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.

import sys
sys.path.append("../../Commun")
from outils_dates import *
import cgi

#------------------------------------------------------------
# Affichage des logs

# La base de données leases.db est constituée de
# (ip INT,mac INT,date_start INT,date_end INT,hostname VARCHAR(20))
# Attribut de la classe
att_leases = {"ip":"Adresse IP", "mac":"Adresse mac", "date_start":"Date de d&eacutebut d'attribution de l'IP", "date_end":"Date de fin d'attribution de l'IP", "hostname":"Nom d'utilisateur"}

def page_logs():
    # Récupération des informations à afficher
    info=cgi.FieldStorage()
    del info["Afficher"]
    
    # Génération du code HTML de la page
    codeHTML=''
    with open("codeHTML/logDCHP.html", 'r') as code:
        for phrase in code:
            if "|***AffichageLog***|" not in phrase:
                codeHTML += phrase

            # Sinon, c'est l'endroit où afficher les logs
            else:
                BDD_leases = sqlite3.connect('Bases_de_donnees/leases.db')

                if "tout" in info:
                    info.remove("tout")
                    info+=att_leases.keys()

                cles=[]
                for key in info:
                    if key!="class":
                        instruction += key + ","
                        cles.append(key)
                instruction = instruction[:-1]
                instruction += " FROM leases"
                if "class" in info:
                    if info["class"]=="0" and "ip" in info:
                        instruction += " ORDER BY ip"
                    elif info["class"]=="1" and "mac" in info:
                        instruction += " ORDER BY mac"
                    elif info["class"]=="2" and "date_start" in info:
                        instruction += " ORDER BY date_start"
                    elif info["class"]=="3" and "date_end" in info:
                        instruction += " ORDER BY date_end"
                    elif info["class"]=="4" and "hostname" in info:
                        instruction += " ORDER BY hostname"
                curseur = BDD_leases.cursor().execute(instruction)
                donnees = curseur.fetchall()

                # Affichage des log

                #Initialisation du tableau
                codeHTML += '<table border="1" width="100%" cellpadding="1" cellspacing="0">'
                #Colonnes
                codeHTML += "<thead>"
                codeHTML += "<tr>"
                for key in cles:
                    codeHTML += "<td><b>" + att_leases[key] + "</b></td>"
                codeHTML += "</tr>"
                codeHTML += "</thead>"
                #Données
                codeHTML += "<tbody>"
                l = len(donnees[0])
                for ligne in donnees:
                    codeHTML += "<tr>"
                    for i in xrange(l):
                        if cles[i]=="ip":
                            codeHTML += "<td>" + str(netaddr.IPAddress(ligne[i])) + "</td>"
                        elif cles[i]=="mac":
                            codeHTML += "<td>" + str(netaddr.EUI(ligne[i])) + "</td>"
                        elif cles[i]=="date_start":
                            codeHTML += "<td>" + time2str(ligne[i]) + "</td>"
                        elif cles[i]=="date_end":
                            codeHTML += "<td>" + str(ligne[i]) + "</td>"
                        elif cles[i]=="hostname":
                            codeHTML += "<td>" + ligne[i] + "</td>"
                    codeHTML += "</tr>"
                codeHTML += "</tbody>"
                codeHTML += "</table>"
                curseur.close()

    return codeHTML


print standard_title
print page_logs()
print standard_end
