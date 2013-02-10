#encoding: latin1

#------------------------------------------------------------
# Ce fichier sert à créer l'arborescence des switch
#------------------------------------------------------------

#Ajouter de la robustesse => vérifier qu'on ajoute pas deux fois le même switch avec la même IP
class Switch:
    # Constructeur
    def __init__(self,IP,mac):
        self.IP = IP
        self.mac = mac
        self.ping = "0" # 0 si le switch répond à ping IP
        self.fils = []
    
    # Affichage de l'aborescence des switch (à partir de celui-ci)
    def affiche(self, prefix, prefixB):
        print prefix + str(self.IP)
        taille = len(self.fils)
        if taille>0:
            for i in xrange(taille-1):
                self.fils[i].affiche(prefixB+"|----", prefixB+"|    ")
            self.fils[taille-1].affiche(prefixB+"\----",prefixB+"     ")
            print prefixB

    # Affichage HTML de l'arboresscence des switch (à partir de celui-ci)
    def afficheHTML(self, prefix, prefixB):
        if self.ping=="0":
            code = prefix + "IP: " + str(self.IP) + " (MAC: "+ self.mac + ")<br>"
        else:
            code = prefix + '<font color="red"><b>IP: ' + str(self.IP) + "</b></font> (MAC: "+ self.mac + ")<br>"
        taille = len(self.fils)
        if taille>0:
            code += prefixB + "|<br>"
            for i in xrange(taille-1):
                code += self.fils[i].afficheHTML(prefixB+"|-----------------", prefixB+"|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
                code += prefixB + "|<br>"
            code += self.fils[taille-1].afficheHTML(prefixB+"\-----------------",prefixB+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        return code

    # Cette fonction parcours l'arborescence et remplace la variable ping dans la classe switch
    def reponseSwitch(self, reponse):
        for ligne in reponse:
            if self.IP==ligne[0]:
                if ligne[1]=="0" or ligne[1]=="1":
                    self.ping=ligne[1]
                break
        for switchFils in self.fils:
            switchFils.reponseSwitch(reponse)


#------------------------------------------------------------
# Création de l'arborescence des résidences
#------------------------------------------------------------

# Routeur
routeur = Switch("172.24.0.1","inconnu")

# Rezo
routeur.fils.append(Switch("172.24.0.10", "inconnu"))

# Cyber
routeur.fils.append(Switch("172.24.0.11", "inconnu"))

# Berbere
routeur.fils.append(Switch("172.24.0.20", "inconnu"))

# Touareg
routeur.fils.append(Switch("172.24.0.21", "inconnu"))

# Bedouin
routeur.fils.append(Switch("172.24.0.22", "inconnu"))

# Colossus
routeur.fils.append(Switch("172.24.0.23", "inconnu"))

# Local technique
switchMeunier = Switch("172.24.0.101","inconnu")
routeur.fils.append(switchMeunier)

# Local technique -> Meunier
switchMeunier.fils.append(Switch("172.24.0.103","inconnu"))

# Armoire 1 de Meunier
switchMeunier.fils[0].fils.append(Switch("172.24.0.111","inconnu"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.112","00:18:4d:d7:5b:17"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.113","00:18:4d:d7:5b:1d"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.114","74:44:01:81:93:90"))

# Armoire 2 de Meunier
switchMeunier.fils[0].fils.append(Switch("172.24.0.121","20:4e:7f:8b:67:02"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.122","00:18:4d:d5:46:52"))

# Armoire 3 de Meunier
switchMeunier.fils[0].fils.append(Switch("172.24.0.131","74:44:01:81:93:95"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.132","74:44:01:81:93:97"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.133","00:1e:2a:db:dc:3c"))

# Armoire 4 de Meunier
switchMeunier.fils[0].fils.append(Switch("inconnu","00:1B:2F:B0:15:54"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.142","000:18:4d:d4:35:e4"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.143","00:1E:2A:DB:BD:70"))
switchMeunier.fils[0].fils.append(Switch("172.24.0.144","00:18:4d:2e:89:54"))

# local technique -> Perronet
switchMeunier.fils.append(Switch("172.24.0.100","00:0a:57:12:cd:e1"))
switchMeunier.fils.append(Switch("172.24.0.104","00:0a:57:dc:2b:21"))
switchMeunier.fils.append(Switch("172.24.0.203","20:4e:7f:8b:67:35"))
switchMeunier.fils.append(Switch("172.24.0.204","20:4e:7f:8b:67:1e"))
