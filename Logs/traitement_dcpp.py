#!/usr/bin/python
#encoding: latin1

import netaddr
import sqlite3
import sys
import subprocess

sys.path.append("../Commun")
from outils_dates import *

ORIGINE=0


class Utilisateur:
    def __init__(self,ip,mois,jour,heure,pseudo="",chambre="",mail=""):
        self.ip=netaddr.IPAddress(ip)
        self.date_connexion=str2time(mois+' '+jour+','+heure)
        self.pseudo=pseudo
        self.chambre=chambre
        self.mail=mail
    def __str__(self):
        return self.pseudo
    def insert_user(self,cursor,debut):
        if self.date_connexion>debut:
            cursor.execute('INSERT INTO dcpp VALUES (?,?,?,?,?)',(int(self.ip),self.date_connexion,self.pseudo,self.chambre,self.mail))
            print>>sys.stderr, str(self) 


def init_base(nombdd):
    # Si la bdd n'existe pas, la crée
    '''La BDD contient la table utilisateurs qui contient les ip/time/pseudo/chambre/mail
    les dates se comptent en systeme UNIX, probleme->1900
    les champs peuvent être vide'''
    
    test=subprocess.call(["ls",nombdd])
    if test==0:
        print "la base existe deja"
        return 0
    else:
        conn=sqlite3.connect(nombdd)
        try:
            conn.execute('CREATE TABLE dcpp(ip INT,time INT,pseudo VARCHAR(40),chambre VARCHAR(20),mail VARCHAR(40))')
            conn.commit()
            conn.close()
            print "la base a ete creee" 
            return 0
        except Exception, ex:
            print "probleme lors de la creation de la base de donnees ",ex
            conn.close()
            return 1


def lit(nomfichier,nombdd):
    '''lit le fichier et stocke au fur et à mesure les informations dans la bdd. On ne stocke que les info plus récentes que debut'''
    l=[]#ligne du fichier

    #initialisation de la bdd - debut : date de dernière modif
    init_base(nombdd)
    conn=sqlite3.connect(nombdd)
    curs=conn.cursor()
    curs.execute('SELECT max(time) FROM dcpp')
    debut=curs.fetchall()
    debut=debut[0][0]
    if debut==None:
        debut=ORIGINE

    #on ouvre le fichier en lecture
    with open(nomfichier,'r') as f:
        for ligne in f.readlines():
            login=""
            info=""
            mail=""
            ip="0.0.0.0"
            #on lit les lignes une à une
            ligne=ligne.strip('\n |')
            l=ligne.split(' ')
            L=len(l)
            if (L<3):
                continue
            mois=l[0]
            jour=l[1]
            heure=l[2]
            i=3
            while i<L:
                if l[i]=="user_info":
                    ip=l[i+3]
                    i=i+4
                if l[i]=="$ALL":
                    login=l[i+1]
                    info=l[i+2]
                    i=i+3
                else:
                    i=i+1
            l=ligne.split('$')
            L=len(l)
            i=0
            while i<L:
                if l[i]=="MyINFO ":
                    mail=l[i+4]
                    i=i+5
                else:
                    i=i+1
            U=Utilisateur(ip,mois,jour,heure,login,info,mail)
            U.insert_user(curs,debut)
    conn.commit()
    conn.close()
    
def execute(logFile,bddFile):
    subprocess.call(["rm","tmp"])
    cmd=["/bin/bash","-c","cat"+logFile+" | grep MyINFO | grep 4413 > tmp"]
    subprocess.Popen(cmd);# on filtre au préalable les logs
    time.sleep(3);# pour attendre la création du fichier tmp
    l=lit("tmp",bddFile);
    subprocess.call(["rm","tmp"]);

def tests():
    execute("../Logs/Data/logdcpp","../Logs/BDD/utilisateurs_tests.db")
        
if __name__=='__main__':
    execute("Data/logdcpp","BDD/utilisateurs.db")
