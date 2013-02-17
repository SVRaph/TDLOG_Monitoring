#!/usr/bin/python
#encoding: latin1

import netaddr
import sqlite3
import sys
import subprocess

sys.path.append("../Commun")
from outils_dates import *


ORIGINE=0
NOW=datetime2time(datetime.datetime.now())

class Lease:
    def __init__(self,ip,mac,startd,startt,endd,endt,hostname=""):
        self.ip=netaddr.IPAddress(ip)
        self.mac=netaddr.EUI(mac)
        self.start=str2time(startd+','+startt)
        self.end=str2time(endd+','+endt)
        self.hostname=hostname
    def __str__(self):
        return str(self.ip)+" <-> "+str(self.mac)
    def estrecent(self,ini,fin):
        return ((self.start>ini)&(self.end>fin))
    def insert_lease(self,cursor,ini=ORIGINE,fin=NOW):
    #on ajoute la lease à la bdd ssi elle est récente ie encore valide et pas déjà enregistrée
        if self.estrecent(ini,fin):
            cursor.execute('INSERT INTO leases VALUES (?,?,?,?,?)',(int(self.ip),int(self.mac),self.start,self.end,self.hostname))
            print>>sys.stderr, str(self) 



def init_base(nombdd):
    # Si la bdd n'existe pas, la crée
    '''La BDD contient la table Lease qui contient les ip/mac/time_start/time_end/hostname
    les dates se comptent en systeme UNIX, 'never'->2100, probleme->1900
    hostname peut être vide'''
    
    test=subprocess.call(["ls",nombdd])
    if test==0:
        print "la base existe deja"
        return 0
    else:
        conn=sqlite3.connect(nombdd)
        try:
            conn.execute('CREATE TABLE leases(ip INT,mac INT,date_start INT,date_end INT,hostname VARCHAR(20))')
            conn.commit()
            conn.close()
            print "la base a ete creee" 
            return 0
        except:
            print "probleme lors de la creation de la base de donnees"
            conn.close()
            return 1
        
def lit(nomfichier,nombdd):
    '''lit le fichier et stocke au fur et à mesure les informations dans la bdd. On ne stocke que les info plus récentes que début et tjrs d'actualité'''
    l=[]#ligne du fichier

    #initialisation de la bdd - debut : date de dernière modif
    init_base(nombdd)
    conn=sqlite3.connect(nombdd)
    curs=conn.cursor()
    curs.execute('SELECT max(date_start) FROM leases')
    debut=curs.fetchall()
    debut=debut[0][0]
    if debut==None:
        debut=ORIGINE
    print 'Debut le ',debut
    #on ouvre le fichier en lecture
    # et on lit les lignes 1 à 1
    with open(nomfichier,'r') as f:
        for ligne in f.readlines():
            l=ligne.strip('\n ;').split(' ')
            # si on débute une lease, on prépare le stockage des infos
            if l[0] == "lease":
                ip=l[1]
                # on reinitialise les données cherchées
                mac=""
                startd=""
                startt=""
                endd=""
                endt=""
                host=""
            # si on a fini une lease on stocke
            elif l[0] == "}":
                L=Lease(ip,mac,startd,startt,endd,endt,host)
                L.insert_lease(curs,debut,debut)# verifie les dates
            #sinon on cherche des données
            elif l[0] == "lease":
                ip=l[1]
            elif l[0]=="starts":
                startd=l[2]
                startt=l[3]
            elif l[0]=="ends":
                if l[1]=="never":
                    endd="never"
                else:
                    endd=l[2]
                    endt=l[3]
            elif l[0]=="hardware":
                mac=l[2]
            elif l[0]=="client-hostname":
                host=l[1]

    conn.commit()
    conn.close()


def tests():
    lit("../dhcp/logdhcp","leases_tests.db")


if __name__=='__main__':
    lit("logdhcp","leases.db")
