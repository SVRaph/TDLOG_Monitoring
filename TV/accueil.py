#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.


import xml.dom.minidom as xdom

from outils import *
#standard_title, standard_end, str2html, type Programme...


# méthode pour récupérer la valeur du champs st dans le fichier xml
def getTag(p,st):
    r=p.getElementsByTagName(st)[0].firstChild.data
    r=r.encode('latin1')
    r=str2html(r)
    return r


#La page d'accueil doit afficher un formulaire
#on utilise un formulaire de type checkbox pour laisser à l'utilisateur la possibilité de choisir plusieurs programmes (même s'ils sont incompatibles)
#on génère le formulaire à partir de la list du fichier sondage.xml
def accueil():
    source='sondage.xml'
    l_base='<input type="checkbox" name="%d" value="1">%s</input><br>\n'
    form='<h2>Fomulaire</h2><form action="vote.py" method="get">\n'
    progs=[]
    try:
        #lecture du fichier et initialisation
        doc=xdom.parse(source)
        for p in doc.getElementsByTagName('programme'):
            description=getTag(p,'description')
            chaine=getTag(p,'chaine')
            debut=getTag(p,'debut')
            duree=getTag(p,'duree')
            progs.append(Programme(description,chaine,debut,duree))
        #creation des differentes lignes du formulaire
        indice=0
        for p in etat_des_progs: 
            form+=l_base % (indice,p.description)
            indice+=1
        #finalisation
        form+='<input type="submit" name="Envoyer"></form>\n'
        form+='<a href="/resultats.py">Voir les resultats</a>\n'
    except Exception,ex:
        print ex
        return "Probl&egraveme de cr&eacuteation du formulaire"
    return form

print standard_title
print accueil()
print standard_end
