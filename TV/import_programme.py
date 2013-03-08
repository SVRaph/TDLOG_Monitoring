#!/usr/bin/python
#encoding: latin1

# on récupère le flux xml contenant le programme télé et on souhaite l'enregistrer suivant le format décrit par le fichier modele.dtd
# bon normalement je devrai rajouter la ligne <!DOCTYPE greeting SYSTEM "modele.dtd"> mais j'arrive pas à trouver le bon paramètre à passer

import xml.dom.minidom as xdom
import urllib
import re

#variables globales

adresse = 'http://feeds.feedburner.com/programme-television?format=xml'
path_fichier='sondage.xml'

#à partir du flux xml on crée la liste des titres de la forme :
#Chaine | 20:50 : Nom de l'émission (0h30) Type de l'émission

doc_input = xdom.parse(urllib.urlopen(adresse))
liste=[]

for item in doc_input.getElementsByTagName('item'):
    titre = item.getElementsByTagName('title')[0].firstChild.data
    liste.append(titre)
    #print titre

#à partir de cette liste on va générer notre document xml

#pour simplifier on crée une classe doc_xml qui contient le document et quelques routines nécessaires
class doc_xml:
    def __init__(self):
        self.impl = xdom.getDOMImplementation()
        self.doc  = self.impl.createDocument(None,"Yop",None)
    def ajouterTextElement(self,pere,element,valeur):
        noeud = self.doc.createElement(element)
        texte = self.doc.createTextNode(valeur)
        noeud.appendChild(texte)
        pere.appendChild(noeud)
    def ajouterProg(self, des, chaine,debut,duree):
        prog = self.doc.createElement("programme")
        self.ajouterTextElement(prog,"description",des)
        self.ajouterTextElement(prog,"chaine",chaine)
        self.ajouterTextElement(prog,"debut",debut)
        self.ajouterTextElement(prog,"duree",duree)
        self.ajouterTextElement(prog,"nbVote","0")# nbVotes serait + correct
        self.doc.documentElement.appendChild(prog)
    def aff(self):
        print self.doc.toprettyxml()
    def enregistre(self,path):
        with open(path,'w') as fichier:
            fichier.write(self.doc.toxml("latin1"))


doc_output=doc_xml()

'''
print str(doc_output)
doc_output.ajouterProg("Chaine | 20:50 : Nom de l'émission (0h30) Type de l'émission","France_2","20:50","0:30")
print str(doc_output)
'''

#on parcours la liste en sélectionnant les éléments qui nous intéresse à l'aide de regexp
for t in liste:
    des=t
    r=re.search("^.*\|",t)
    chaine=r.group(0)
    chaine=chaine.strip('|').strip(' ')
    chaine=chaine.replace(' ','_')

    r=re.search("[0-9]+:[0-9]+",t)
    deb=r.group(0)

    r=re.search("[0-9]+h[0-9]+",t)
    dur=r.group(0)
    dur=dur.replace('h',':')

    doc_output.ajouterProg(des,chaine,deb,dur)


#et on écrit tout ça dans un fichier
doc_output.aff()
doc_output.enregistre(path_fichier)


