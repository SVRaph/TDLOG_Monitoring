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
        code = prefix + "IP: " + str(self.IP) + " (mac: "+ self.mac + ")<br>"
        taille = len(self.fils)
        if taille>0:
            code += prefixB + "|<br>"
            for i in xrange(taille-1):
                code += self.fils[i].afficheHTML(prefixB+"|-----------------", prefixB+"|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
                code += prefixB + "|<br>"
            code += self.fils[taille-1].afficheHTML(prefixB+"\-----------------",prefixB+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        return code


#------------------------------------------------------------
# Création de l'arborescence des résidences
#------------------------------------------------------------

# switch racine
switchRacine = Switch("172.24.0.101","inconnu")

# partie relative à Meunier
switchRacine.fils.append(Switch("172.24.0.103","inconnu"))

# Armoire 1 de Meunier
switchRacine.fils[0].fils.append(Switch("172.24.0.111","inconnu"))
switchRacine.fils[0].fils.append(Switch("172.24.0.112","inconnu"))
switchRacine.fils[0].fils.append(Switch("172.24.0.113","00:18:4D:D7:5B:1D"))
switchRacine.fils[0].fils.append(Switch("172.24.0.114","inconnu"))

# Armoire 2 de Meunier
switchRacine.fils[0].fils.append(Switch("172.24.0.121","inconnu"))
switchRacine.fils[0].fils.append(Switch("172.24.0.122","inconnu"))

# Armoire 3 de Meunier
switchRacine.fils[0].fils.append(Switch("172.24.0.131","inconnu"))
switchRacine.fils[0].fils.append(Switch("172.24.0.132","inconnu"))
switchRacine.fils[0].fils.append(Switch("172.24.0.133","inconnu"))

# Armoire 4 de Meunier
switchRacine.fils[0].fils.append(Switch("172.24.156.248","00:1B:2F:B0:15:54"))
switchRacine.fils[0].fils.append(Switch("172.24.0.142","00:18:4D:D4:35:E4"))
switchRacine.fils[0].fils.append(Switch("172.24.0.143","00:1E:2A:DB:BD:70"))
switchRacine.fils[0].fils.append(Switch("172.24.0.144","00:18:4D:2E:89:54"))
