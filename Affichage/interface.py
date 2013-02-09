#!/usr/bin/python
#encoding: latin1

import web
import switch as sw
import sqlite3
import os
import os.path


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
        codeHTML+=standard_end
        return codeHTML


#--------------------------------------------------
# Plan des switch

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
                    codeHTML += sw.switchRacine.afficheHTML("","")
        codeHTML+=standard_end
        return codeHTML


#------------------------------------------------------------
# Affichage des logs

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
                    BDD_leases = sqlite3.connect('leases.db')

                    if "tout" in info:
                        # Affichage des log
                        curseur = BDD_leases.cursor().execute("SELECT * FROM leases")
                        for row in curseur :
                            codeHTML += str(row) + "<br>"
                        curseur.close()

                    else:
                        # Génération de la requête SQL
                        instruction = "SELECT "
                        for key in info:
                            instruction += key + ","
                        instruction = instruction[:-1]
                        instruction += " FROM leases"
                        curseur = BDD_leases.cursor().execute(instruction)
                        
                        # Affichage des log
                        for row in curseur :
                            codeHTML += str(row) + "<br>"
                        curseur.close()

        codeHTML+=standard_end
        return codeHTML

#------------------------------------------------------------
# Lancement du site
#------------------------------------------------------------
if __name__ == '__main__':
    urls = (
        "/index.html" , "page_index",
        "/logdhcp.html" , "page_logs",
        "/switch.html" , "page_switch"
    )
    webapp = web.application(urls, globals() )
    webapp.run()
