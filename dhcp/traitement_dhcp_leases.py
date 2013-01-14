#!/usr/bin/python
#encoding: latin1

import netaddr
import datetime

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


if __name__=='__main__':
    l=lit("logdhcp")
    for le in l:
        1==1
        #print le
    print l[1]
    print l[1].start
