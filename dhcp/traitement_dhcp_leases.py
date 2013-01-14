#!/usr/bin/python
#encoding: latin1



class Lease:
    def __init__(self,ip,mac,start,end,hostname=""):
        self.ip=ip
        self.mac=mac
        self.start=start
        self.end=end
        self.hostname=hostname
    def __str__(self):
        return self.ip+" <-> "+self.mac

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
        print le
