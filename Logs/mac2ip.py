#!/usr/bin/python
#encoding: latin1

import netaddr
import datetime
import sqlite3

sys.path.append("../Commun")
from outils_dates import *

lmac=['74:44:01:81:93:1D','74:44:01:81:93:90','00:18:4D:D7:5B:1D','00:18:4D:D7:5B:17','20:4E:7F:8B:67:02','00:18:4D:D5:46:52','74:44:01:81:93:95','74:44:01:81:93:97','00:1E:2A:DB:DC:3C','00:1B:2F:B0:15:54','00:18:4D:D4:35:E4','00:1E:2A:DB:BD:70','00:18:4D:2E:89:54']

# renvoie les différentes ip associé à une mac en utilisant les leases et les tables mac.
def mac2ip(strmac):
    mac=netaddr.EUI(strmac)

    #leases
    conn=sqlite3.connect('BDD/leases.db')
    curs=conn.cursor()
    req='SELECT ip FROM leases WHERE mac=%d ' % int(mac)
    curs.execute(req)
    res=curs.fetchall()
    for ipint in res:
        ipint=int(ipint[0])
        ip=netaddr.IPAddress(int(ipint))
        print mac,ip

    #tables mac
    conn=sqlite3.connect('BDD/TablesMAC.db')
    curs=conn.cursor()
    req='SELECT switch,port FROM table_mac WHERE mac=%d ' % int(mac)
    curs.execute(req)
    res=curs.fetchall()
    for x in res:
        ipintsw=res[0]
        port=res[1]
        ip=netaddr.IPAddress(int(ipint))
        print mac,ip,port




def info_mac(strmac):
    # objectif : améliorer la recherche d'un DHCP sur Perronet

    mac=netaddr.EUI(strmac)
    conn_leases=sqlite3.connect('../Logs/BDD/leases.db') # table leases
    conn_utilis=sqlite3.connect('../Logs/BDD/utilisateur.db') #table dcpp
    conn_tables=sqlite3.connect('../Logs/BDD/TablesMAC.db') #table table_mac

    port=-1
    switch=0

    #'TABLE table_mac(date INT,switch INT, mac INT,port INT)'
    #'TABLE leases(ip INT,mac INT,date_start INT,date_end INT,hostname VARCHAR(20))'
    #'TABLE dcpp(ip INT,time INT,pseudo VARCHAR(40),chambre VARCHAR(20),mail VARCHAR(40))'

    # On localise la MAC 
    # -- TODO -- faciliter la recherche par requete ARP
    # Rq : on recherche aussi dans les leases (peut servir pour autre chose qu'un dhcp rogue)

    curs=conn_tables.cursor()
    req='SELECT * FROM table_mac WHERE mac=%d' % int(mac)
    curs.execute(req)
    res1=curs.fetchall()

    curs=conn_leases.cursor()
    req='SELECT * FROM leases WHERE mac=%d ' % int(mac)
    curs.execute(req)
    res2=curs.fetchall()

    print '*** Tables MAC : recherche %s ***' % str(mac)
    for x in res1:
        if len(x)>0:
            port=x[3]
            switch=x[2]
        print x

    print '*** Leases : recherche %s ***' % str(mac)
    for x in res2:
        print x     
 
    # On cherche les gens branchés sur le même ports
    if port>0:
        curs=conn_tables.cursor()
        req='SELECT * FROM table_mac WHERE switch=%d AND port=%d' % switch,port
        curs.execute(req)
        res3=curs.fetchall()
        print '*** Port : recherche du port %d du switch %d ***' % port,switch
        for x in res3:
            print x   


    # Puis on relance manuellemen info_mac sur les MAC ainsi trouvées
