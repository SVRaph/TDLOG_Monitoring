#!/usr/bin/python
#encoding: latin1

import netaddr
import datetime
import sqlite3
import sys

ORIGINE=datetime.date(1970,1,1)


class Lease:
    def __init__(self,ip,mac,start,end,hostname=""):
        self.ip=netaddr.IPAddress(ip)
        self.mac=netaddr.EUI(mac)
        self.start=str2date(start)
        self.end=str2date(end)#attention peut contenir "never"
        self.hostname=hostname
    def __str__(self):
        return str(self.ip)+" <-> "+str(self.mac)

def str2date(s):
    #convertit 2009/12/16 en datetime.date(2009,12,16)
    if s=="never":
        return "never"
    s=s.split('/')
    try:
        return datetime.date(int(s[0]),int(s[1]),int(s[2]))
    except:
        print "Probleme conversion des dates : ", s
        return datetime.date(1900,1,1)

def lit(nomfichier):
    liste=[];
    #on ouvre le fichier en lecture
    with open(nomfichier,'r') as f:
        f=f.readlines()
        L=len(f)#nbre de lignes
        nl=0
        #boucle sur les lignes
        while nl<L:
            l=f[nl].strip('\n ;').split(' ')
            nl+=1
            if l[0] == "lease":
                ip=l[1]
                mac=""
                start=""
                end=""
                host=""
                while l[0] != "}" and nl<L:
                    l=f[nl].strip('\n ;').split(' ')
                    nl+=1
                    if l[0]=="starts":
                        start=l[2]
                    if l[0]=="ends":
                        if l[1]=="never":
                            end="never"
                        else:
                            end=l[2]
                    if l[0]=="hardware":
                        mac=l[2]
                    if l[0]=="client-hostname":
                        host=l[1]
                liste.append(Lease(ip,mac,start,end,host))
        return liste

def stock(liste,path):
    debut=(datetime.date(2012,1,1)-ORIGINE).days
    connexion=sqlite3.connect(path)
    '''La BDD contient la table usr contient les ip/mac/date_start/date_end/hostname
    les dates se comptent en jours depuis le 1970/1/1, -1 signifie 'never'
    hostname peut être vide'''
    #on teste si la base existe déjà, le cas écheant on remplie uniquement avec les données récentes
    try:
        connexion.execute('CREATE TABLE usr(ip INT,mac INT,date_start INT,date_end INT,hostname VARCHAR(20))')
        connexion.commit()
        print "creation de la base" 
    except:
        print "la base existe déjà"
        curseur=connexion.cursor()
        curseur.execute('SELECT max(date_start) as delta FROM usr')
        debut=curseur.fetchall()
        debut=debut[0][0]
    for lease in liste:
        n=0
        if (lease.end=='never'):
            n=-1
        elif (lease.end>=datetime.date.today() and (lease.start-ORIGINE).days>=debut):
            n=(lease.end-ORIGINE).days
        if n!=0:
            connexion.execute('INSERT INTO usr VALUES (?,?,?,?,?)',(int(lease.ip),int(lease.mac),(lease.start-ORIGINE).days,n,lease.hostname))
        connexion.commit()
        print>>sys.stderr, lease.start-ORIGINE
        print>>sys.stderr, lease
        print>>sys.stderr, lease.end
    connexion.close()

if __name__=='__main__':
    l=lit("logdhcp")
    stock(l,'./utilisateurs.sqlite3')
