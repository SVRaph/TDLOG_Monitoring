#!/usr/bin/python
#encoding: latin1

import cgitb
cgitb.enable()

print 'Content-type: text/html'
print
# Là commence votre code.


import xml.dom.minidom as xdom
import cgi

from outils import *
#standard_title, standard_end, str2html


#cette page vérifie la validité du vote (!?) l'enregistre
#et affiche une page de confirmation
def vote():
    source='sondage.xml'
    votes_progs=[]
    resvote=''
    
    try:
        #on charge le fichier sondage.xml et les arguments GET
        dico = cgi.FieldStorage()
        for c in dico:
            if c=="Envoyer":
                pass
            else:
                votes_progs.append(int(c))

        doc=xdom.parse(source)
        progs=[p for p in doc.getElementsByTagName('programme')]
    
        for i in votes_progs:
            r=progs[i].getElementsByTagName('nbVote')
            n=int(r[0].firstChild.data)
            r[0].firstChild.data=str(n+1)
            resvote+='<br>'+progs[i].getElementsByTagName('description')[0].firstChild.data
                
    except Exception,ex:
        #principalement: c n'est pas un bon entier 
        print ex
        return "Vote invalide"  

    #affichage de la page
    res="Vous avez vot&eacute : %s<br>Merci de votre participation, votre vote a bien &eacutet&eacute pris en compte<br><a href=\"/resultats.py\">Voir les r&eacutesultats</a><br>" % (resvote)
    return res


print standard_title
print vote()
print standard_end
