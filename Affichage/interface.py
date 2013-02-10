#!/usr/bin/python
#encoding: latin1

import web
import switch as sw
import sqlite3
import os
import os.path
import netaddr
import time
import sys
import subprocess

#------------------------------------------------------------
# En-tête de page (à mettre au début de chaque nouvelle page)
#------------------------------------------------------------
standard_title='''
<html>

<head>
	<title>KI :// R&eacute;seau des r&eacute;sidences :: Diagnostic r&eacute;seau</title>

	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
	<meta http-equiv="Content-Style-Type" content="text/css"/>
	<meta name="keywords" content="ENPC,Ponts,ParisTech,Clubinfo,KI,Meunier,Perronet,R&eacute;seau des r&eacute;sidences,Diagnostic"/>

	<link rel="stylesheet" type="text/css" href="static/style.css"/>
</head>

<body>

<table class="full" style="width:100%;height:100%;">
	<tr style="height:100px;">
		<td style="height:100px;width:200px;background:url('static/c1.png') repeat-y right;"></td>
		<td style="height:100px;width:17px;background:url('static/c2l1.png') bottom no-repeat #006650;"></td>
		<td id="header" style="height:100px;background:url('static/c3l1.png') bottom repeat-x #006650;"><div>Clubinfo de l'&Eacute;cole des Ponts ParisTech</div><i>P 401 - clubinfo@clubinfo.enpc.fr</i></td>
	</tr>
	<tr>
		<td id="menu" style="width:200px;background:url('static/c1.png') repeat-y right;padding-top:60px;"></td>
		<td style="width:17px;background:url('static/c2l2.png') left repeat-y #fff;"></td>
		<td id="corpus">
			       
<h1>R&eacute;seau des r&eacute;sidences :: Diagnostic r&eacute;seau</h1>
'''

#------------------------------------------------------------
# Bas de page (à mettre en fin de chaque nouvelle page)
#------------------------------------------------------------
standard_end='''
<hr/>
<center><i>clubinfo@clubinfo.enpc.fr - ENPC KI<br/>Refonte du site par H&egravel&egravene Dieumegard et Kevin Obrejan (KI'011) : Septembre 2009<br/>Ajout du diagnostique r&eacuteseau par Etienne de Saint Germain, Alexandre Sarrazin et Raphael Sivera (KI'014) : f&eacutevrier 2013</i></center>

</table>

<img src="static/logo.png" alt="static/logo.png" style="position:absolute;left:0px;top:0px;border:0px;"/>
<img src="static/c4l1.png" alt="" style="position:absolute;top:0px;right:0px;"/>

</body>
</html>
'''



#------------------------------------------------------------
# Défintion des différentes pages
#------------------------------------------------------------

#--------------------------------------------------
# Page d'index

class page_index:
    def GET(self):
        # Génération du code HTML de la page
        codeHTML=standard_title
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
        codeHTML+=standard_end
        return codeHTML


#--------------------------------------------------
# Plan des switchs

class page_switch:
    def GET(self):
        # Génération du code HTML de la page
        codeHTML=standard_title
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
        codeHTML+=standard_end
        return codeHTML


#------------------------------------------------------------
# Affichage des logs

# La base de données leases.db est constituée de
# (ip INT,mac INT,date_start INT,date_end INT,hostname VARCHAR(20))
# Attribut de la classe
att_leases = {"ip":"Adresse IP", "mac":"Adresse mac", "date_start":"Date de d&eacutebut d'attribution de l'IP", "date_end":"Date de fin d'attribution de l'IP", "hostname":"Nom d'utilisateur"}

# Conversion d'un INTtime en STRtime
def int2time(INTtime):
    t = time.gmtime(INTtime)
    year = str(t.tm_year)
    mon = str(t.tm_mon)
    if len(mon)<2:
        mon = "0" + mon
    day = str(t.tm_mday)
    if len(day)<2:
        day = "0" + day
    hour = str(t.tm_hour)
    if len(hour)<2:
        hour = "0" + hour
    mi = str(t.tm_min)
    if len(mi)<2:
        mi = "0" + mi
    sec = str(t.tm_sec)
    if len(sec)<2:
        sec = "0" + sec
    return year + "/" + mon + "/" + day + " " + hour + ":" + mi + ":" + sec


class page_logs:
    def GET(self):
        # Récupération des informations à afficher
        info=web.input()
        del info["Afficher"]

        # Génération du code HTML de la page
        codeHTML=standard_title
        with open("codeHTML/logDCHP.html", 'r') as code:
            for phrase in code:
                if "|***AffichageLog***|" not in phrase:
                    codeHTML += phrase

                # Sinon, c'est l'endroit où afficher les logs
                else:
                    BDD_leases = sqlite3.connect('Bases_de_donnees/leases.db')

                    if "tout" in info:
                        # Affichage des log
                        instruction = "SELECT * FROM leases"
                        if "class" in info:
                            if info["class"]=="0":
                                instruction += " ORDER BY ip"
                            elif info["class"]=="1":
                                instruction += " ORDER BY mac"
                            elif info["class"]=="2":
                                instruction += " ORDER BY date_start"
                            elif info["class"]=="3":
                                instruction += " ORDER BY date_end"
                            elif info["class"]=="4":
                                instruction += " ORDER BY hostname"
                        curseur = BDD_leases.cursor().execute(instruction)
                        donnees = curseur.fetchall()
                        codeHTML += '<table border="1" width="100%" cellpadding="1" cellspacing="0">'
                        codeHTML += "<thead>"
                        codeHTML += "<tr>"
                        codeHTML += "<td><b>Adresse IP</b></td>"
                        codeHTML += "<td><b>Adresse mac</b></td>"
                        codeHTML += "<td><b>D&eacutebut d'attribution de l'IP</b></td>"
                        codeHTML += "<td><b>Fin d'attribution de l'IP</b></td>"
                        codeHTML += "<td><b>Utilisateur</b></td>"
                        codeHTML += "</tr>"
                        codeHTML += "</thead>"
                        codeHTML += "<tbody>"
                        for ligne in donnees:
                            codeHTML += "<tr>"
                            codeHTML += "<td>" + str(netaddr.IPAddress(ligne[0])) + "</td>"
                            codeHTML += "<td>" + str(netaddr.EUI(ligne[1])) + "</td>"
                            codeHTML += "<td>" + int2time(ligne[2]) + "</td>"
                            codeHTML += "<td>" + str(ligne[3]) + "</td>"
                            codeHTML += "<td>" + ligne[4] + "</td>"
                            codeHTML += "</tr>"
                        codeHTML += "</tbody>"
                        codeHTML += "</table>"
                        curseur.close()

                    else:
                        # Génération de la requête SQL
                        instruction = "SELECT "
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
                        codeHTML += '<table border="1" width="100%" cellpadding="1" cellspacing="0">'
                        codeHTML += "<thead>"
                        codeHTML += "<tr>"
                        for key in cles:
                            codeHTML += "<td><b>" + att_leases[key] + "</b></td>"
                        codeHTML += "</tr>"
                        codeHTML += "</thead>"
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
                                    codeHTML += "<td>" + int2time(ligne[i]) + "</td>"
                                elif cles[i]=="date_end":
                                    codeHTML += "<td>" + str(ligne[i]) + "</td>"
                                elif cles[i]=="hostname":
                                    codeHTML += "<td>" + ligne[i] + "</td>"
                            codeHTML += "</tr>"
                        codeHTML += "</tbody>"
                        codeHTML += "</table>"
                        curseur.close()

        codeHTML+= standard_end
        return codeHTML


#------------------------------------------------------------
# Confirmation du lancement manuel des scripts

class page_scripts:
    def GET(self):
        codeHTML = standard_title
        info = web.input()
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
        codeHTML += standard_end
        return codeHTML


#------------------------------------------------------------
# Lancement du site
#------------------------------------------------------------
if __name__ == '__main__':
    urls = (
        "/index.html" , "page_index",
        "/logdhcp.html" , "page_logs",
        "/switch.html" , "page_switch",
        "/script.html", "page_scripts"
    )
    webapp = web.application(urls, globals() )
    webapp.run()
