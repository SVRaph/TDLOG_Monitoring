#!/usr/bin/python
#encoding: latin1



#un type d'Exception
class ParametreNonValide(Exception):
    def __init__(self,s):
        self.mess=s
    def __str__(self):
        return ("***ERREUR : Parametre "+self.mess+" non reconnu")


# remplace é,è,à dans s par leurs équivalents en html
def str2html(s):
    dico={"é":"&eacute","è":"&egrave","à":"&agrave"}
    for c in dico:
        s=s.replace(c,dico[c])
    return s

#classe enregistrant les différents paramètres caractérisant un programme télé en particulier
class Programme:
    def __init__(self,d="",c="",deb="18:00",dur="9:00",vote=0):
        try:
            self.description=d
            self.chaine=c
            #les heures début et fin sont définies en min après 18h
            self.debut=((int(deb[0:2])+6) %24)*60+int(deb[3:5])
            duree=int(dur[0])*60+int(dur[2:4])
            self.fin=self.debut+duree
            self.vote=vote
        except Exception,ex:
            print "***ERREUR : Probleme intialisation Programme",ex
    def iscompatible(self,p):
        return ((self.fin<p.debut)|(p.fin<self.debut))
      



#on définie l'en-tête et l'en-queue standard
standard_title='''
<html>

<head>
	<title>KI :// R&eacute;seau des r&eacute;sidences :: La t&eacute;l&eacute;</title>

	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
	<meta http-equiv="Content-Style-Type" content="text/css"/>
	<meta name="keywords" content="ENPC,Ponts,ParisTech,Clubinfo,KI,Meunier,Perronet,R&eacute;seau des r&eacute;sidences,La t&eacute;l&eacute;"/>

	<link rel="stylesheet" type="text/css" href="static/style.css"/>
</head>

<body>

<table class="full" style="width:100%;height:100%;">
	<tr style="height:100px;">
		<td style="height:100px;width:200px;background:url('static/c1.png') repeat-y right;"></td>
		<td style="height:100px;width:17px;background:url('static/c2l1.png') bottom no-repeat #006650;"></td>
		<td id="header" style="height:100px;background:url('static/c3l1.png') bottom repeat-x #006650;"><div>Clubinfo de l'&Eacute;cole des Ponts ParisTech</div><i>P 401 - clubinfo@clubinfo.enpc.fr</i></td>
	</tr>
	<tr>
		<td id="menu" style="width:200px;background:url('static/c1.png') repeat-y right;padding-top:60px;"></td>
		<td style="width:17px;background:url('static/c2l2.png') left repeat-y #fff;"></td>
		<td id="corpus">
			       
<h1>R&eacute;seau des r&eacute;sidences :: La t&eacute;l&eacute;</h1>
'''
standard_end='''
<hr/>
<center><i>clubinfo@clubinfo.enpc.fr - ENPC KI<br/>Refonte du site par H&egravel&egravene Dieumegard et Kevin Obrejan (KI'011) : Septembre 2009</i></center>

</table>

<img src="static/logo.png" alt="static/logo.png" style="position:absolute;left:0px;top:0px;border:0px;"/>
<img src="static/c4l1.png" alt="" style="position:absolute;top:0px;right:0px;"/>

</body>
</html>
'''


