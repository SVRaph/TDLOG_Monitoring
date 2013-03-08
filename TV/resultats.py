#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.


import xml.dom.minidom as xdom
import operator

from outils import *
#standard_title, standard_end, str2html, type Programme...


# méthode pour récupérer la valeur du champs st dans le fichier xml
def getTag(p,st):
    r=p.getElementsByTagName(st)[0].firstChild.data
    r=r.encode('latin1')
    r=str2html(r)
    return r


# Affiche les deux programmes sélectionnés
# Crée un fichier texte comportant 2 programmes compatibles : 19:30 - Arte
def resultats():
    source='sondage.xml'
    outputfile='resultats_bruts.txt'
    progs=[]
    try:
        #lecture du fichier et initialisation
        doc=xdom.parse(source)
        for p in doc.getElementsByTagName('programme'):
            des=getTag(p,'description')
            chaine=getTag(p,'chaine')
            debut=getTag(p,'debut')
            duree=getTag(p,'duree')
            vote=getTag(p,'nbVote')
            progs.append(Programme(des,chaine,debut,duree,int(vote)))

        #on trie les programmes
        progs.reverse()#pour la stabilité du tri
        progs.sort(key=operator.attrgetter('vote'))
        progs.reverse()  
        #et on récupère 2 progs compatibles
        p1=progs[0]
        p2=Programme()
        b=True
        for x in progs:
            if (b)&p1.iscompatible(x):
                p2=x
                b=False

        # Affichage des résultats
        with open(outputfile, 'w') as fw:
            st =str(p1.debut)+' - '+p1.chaine+'\n'
            st+=str(p2.debut)+' - '+p2.chaine
            fw.write(st)
        res ='Et les r&eacutesultats sont...<br>'
        res+=p1.description+'<br>'
        res+=p2.description

    except Exception,ex:
        print ex
        return "Probl&egraveme de cr&eacuteation du formulaire"
    return res

print standard_title
print resultats()
print standard_end
