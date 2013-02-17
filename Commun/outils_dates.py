#!/usr/bin/python
#encoding: latin1

import datetime
import time


DICO_MOIS={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
EPOCH=datetime.datetime(1970,1,1,1)


#                     #
# --- Conversions --- #
#                     #



# Convertit de string vers datetime
'''
Formats supportés
 - 'Nov 10,06:48:54' (implicite année en cours /!\)
 - '2012/11/10,06:48:22'
 - never (== 2050/1/1)
 - si l'heure est absente utilise 0:0:0
Formats de sortie
 - datetime(2012,11,10,06,48,22)

En cas d'erreur affiche problème conversion et renvoie 1970/1/1
'''
def str2datetime(s):
    try:
        NOW=datetime.datetime.now()
        if s=='never':
            return datetime.datetime(2050,1,1)
        # t tableau y,m,d,h,m,s
        t=[0,0,0,0,0,0]
        l=s.split(',')
        d=l[0].split('/')
        # si il y a une heure on s'en occupe
        if (len(l)==2):
            h=l[1].split(':')
            t[3]=int(h[0])
            t[4]=int(h[1])
            t[5]=int(h[2])
        # et on s'occupe de la date
        if (len(d)==3):
            t[0]=int(d[0])
            t[1]=int(d[1])
            t[2]=int(d[2])
        else:
            d=d[0].split(' ')
            t[1]=DICO_MOIS[d[0]]
            t[2]=int(d[1])
            if (t[1]>NOW.month or (t[1]==NOW.month and t[2]>NOW.day)):
                t[0]=NOW.year-1
            else:
                t[0]=NOW.year
        # on renvoie le résultat sous forme datetime
        return datetime.datetime(t[0],t[1],t[2],t[3],t[4],t[5])
    # on rattrape les exceptions
    except Exception, ex:
        print "Probleme conversion des dates : ", s, ex
        return datetime.datetime(1900,1,1)


# Convertit de datetime vers int (seconds since the epoch 1970/1/1) 
def datetime2time(dt):
    return time.mktime(dt.timetuple())

# Convertit directement une string en int
def str2time(s):
    return datetime2time(str2datetime(s))

# Convertit de int vers datetime (seconds since the epoch 1970/1/1) 
def time2datetime(INTtime):
    t=time.localtime(INTtime)
    dt=datetime.datetime(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
    return dt

# Conversion d'un datetime vers une string personalisé
def datetime2str(dt):
    #convertit en str et rajoute un zero au début si longueur < 2
    def str2(i):
        s=str(i)
        if len(s)<2:
            s= "0" + s
        return s

    y = str2(dt.year)
    m = str2(dt.month)
    d = str2(dt.day)
    h = str2(dt.hour)
    mn= str2(dt.minute)
    s = str2(dt.second)
    return y + "/" + m + "/" + d + " " + h + ":" + mn + ":" + s

# Conversion directe INTtime -> STRtime
def time2str(INTtime):
    return datetime2str(time2datetime(INTtime))

# Quelques tests
def tests_outils_date():
    s=['Nov 10,06:48:54','2012/11/10,06:48:22','Dec 12','Feb 29','never']
    for d in s:
        print d," -> ",time2str(str2time(d))
    print 'time of EPOCH', datetime2time(EPOCH)

if __name__=='__main__':
    tests_outils_date()
