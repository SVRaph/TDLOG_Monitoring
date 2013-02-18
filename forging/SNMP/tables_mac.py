#!/usr/bin/python
#encoding: latin1

import netaddr
import sys
import subprocess
import sqlite3
import time

sys.path.append("../../Commun")
import outils_dates


OID_MAC_HP='1.3.6.1.2.1.17.4.3.1.2'

#snmpwalk -v1 -c public 172.24.0.101 .1.3.6.1.2.1.17.4.3.1.2


IPs_HP=['172.24.0.100','172.24.0.101','172.24.0.102','172.24.0.103','172.24.0.104']


#écrit le résultat de la requête dans le fichier table.txt
def lance_requete(IPswitch='172.24.0.103',File='table.txt'):
    cmd="snmpwalk -v1 -c public %s .1.3.6.1.2.1.17.4.3.1.2 > %s" % (IPswitch,File)
    subprocess.call([cmd])

#initialise la base
def init_base(nom):
    ''' nomme la base TableMAC_@IPswitch_@NOW(int).db
    La BDD contient la table mac qui contient mac/port'''

    conn=sqlite3.connect(nom)
    try:
        conn.execute('CREATE TABLE table_mac(mac INT,port INT)')
        conn.commit()
        conn.close()
        print "la base a ete creee" 
        return 0
    except Exception, ex:
        print "probleme lors de la creation de la base de donnees",ex
        conn.close()
        return 1
    
#lit le fichier table
#iso.3.6.1.2.1.17.4.3.1.2.0.10.87.18.205.250 = INTEGER: 25
#et crée une bdd (cf init_base)
def lit_table(IPswitch,File='table.txt'):
    nombdd="TableMAC_%s_%d.db" % (IPswitch,outils_dates.NOW())
    init_base(nombdd)
    conn=sqlite3.connect(nombdd)
    curs=conn.cursor()
    with open(File,'r') as fichier:
        for ligne in fichier.readlines():
            k=len('iso.3.6.1.2.1.17.4.3.1.2.')
            l=ligne[k:].strip('\n').split(' ')
            assert len(l)==4,l
            #port et mac
            port=int(l[3])
            m=l[0].split('.')
            #formatage de la mac
            assert len(m)==6
            mac=0
            for x in m:
                mac *= 256
                mac += int(x)
            #ajout dans la BDD
            curs.execute('INSERT INTO table_mac VALUES (?,?)',(mac,port))
    conn.commit()
    conn.close()
    return nombdd
                

#execution de tout le tsointsoin
def execute(listeIP):
    filetmp='table.txt'
    for IPswitch in listeIP:
        lance_requete(IPswitch,filetmp)
        time.sleep(10)
        lit_table(IPswitch,filetmp)
        subprocess.call(["rm",filetmp])
        time.sleep(3)


#affiche la bdd
def affiche_bdd(nombdd):
    conn=sqlite3.connect(nombdd)
    curs=conn.cursor()
    curs.execute('SELECT * FROM table_mac')
    liste=curs.fetchall()
    print "Lecture de "+nombdd
    for l in liste:
        print str(netaddr.EUI(l[0]))+' --> '+str(l[1])

#tests
def tests(filetest):
    nombdd=lit_table('IPtest',filetest)
    affiche_bdd(nombdd)


if __name__=='__main__':
    #execute(IPs_HP)
    tests('table_test.txt')
