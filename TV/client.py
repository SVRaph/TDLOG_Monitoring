#!/usr/bin/python
#encoding: latin1

import urllib
import os


page=urllib.urlopen('http://localhost:8080/resultats_bruts.txt')
strpage=page.read()
print strpage
os.system("/home/raphal/Bureau/o/chrono/chrono 20")
