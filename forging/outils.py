#!/usr/bin/python
#encoding: latin1


from scapy.all import *

##### Pour l'instant utiles et fonctionnels :
'''
ping_arp() -> liste des appareils présents sur le réseau
dhcp_rogue() -> liste des DHCP
ping_listemac(l) -> ip associées aux mac
ping2(ip) -> ping de puis une adresse inaccessible est sensé générer des erreurs
'''
#####

def test_ttl():
    pkt=IP(dst='172.24.0.103')/ICMP()
    pkt.ttl=(0,16)
    rep=sr(pkt)
    rep=rep[0]
    
    for m in rep:
        if m[0].type==11: #time-exceeded
            print "exceeded : ", m[1].ttl # m[2] IP in ICMP
        else:
            print  m[1].ttl, "ok"


def ping_arp(nretry=1,lk=[200,201,202,203]):
    s="172.24"
    l,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="172.24.0.0" ),retry=0, timeout=2) 
    
    ans1,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.0-63"    % (s,0)) ),retry=nretry, timeout=1)
    ans2,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.64-127"  % (s,0)) ),retry=nretry, timeout=1)
    ans3,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.128-191" % (s,0)) ),retry=nretry, timeout=1)
    ans4,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.192-255" % (s,0)) ),retry=nretry, timeout=1)
    l=l+ans1+ans2+ans3+ans4  
    
    for k in xrange(101):
        ans1,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.0-63"    % (s,k+99)) ),retry=nretry, timeout=1)
        ans2,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.64-127"  % (s,k+99)) ),retry=nretry, timeout=1)
        ans3,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.128-191" % (s,k+99)) ),retry=nretry, timeout=1)
        ans4,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=("%s.%d.192-255" % (s,k+99)) ),retry=nretry, timeout=1)
        l=l+ans1+ans2+ans3+ans4
    l.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )


#ping (ICMP) l'ensemble de la plage d'ip : trop violent cause des erreurs
def ping_all():
    ans,unans=sr( (IP(dst="172.24.0.0/16")/ICMP()) , timeout=0.1,retry=0)
    ans.summary(lambda (s,r): r.sprintf("%IP.src%") )

#simule une requete DHCP pour détecter les offres
def dhcp_rogue():
    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(conf.iface)
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"),"end"])
    ans, unans = srp(dhcp_discover, inter=0.5,retry=20,timeout=2, multi=True) 
    for p in ans: 
        print p[1][Ether].src, p[1][IP].src

#essai pour envoyer un paquet à une adresse ip hors domaine
def test_arping(macrezo='00:11:2f:40:d9:9b',macswitch='00:01:e7:c6:f1:80',mactouareg='00:18:f3:c6:6d:e4'):
    conf.checkIPaddr = False
    pkt=Ether(dst=macrezo)/ARP(pdst="255.255.255.255",op="who-has")
    sendp(pkt)        

#controle des id des paquet IP
def checkipid():
    ping101=IP(dst='10.204.200.28')/ICMP()   
    r1=sr1(ping101)
    r2=sr1(ping101)
    print r1.id," ",r2.id
 
#ping arp vers une ou plusieurs adresse mac
def ping_1mac(mac): 
    pkt=Ether(dst=mac)/ARP(pdst="172.24.0.0/16",hwdst=mac)
    ans,unans=srp(pkt,retry=1, timeout=1)
    return ans
def ping_listemac(lstmac):
    ans=[]
    for mac in lmac:
        ans.append(ping_1mac(mac))
    for a in ans:
        a.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )

#ping de puis une adresse hors domaine -> génération d'erreurs sur le chemin
def ping2(ip="172.24.0.21"):
    pkt=IP(dst=ip,src="192.168.0.1")/ICMP()
    for i in xrange(1000):
        send(pkt)
    
#test_ttl()
#ping_arp()
#dhcp_rogue()
#ping_all()
#checkipid()

lmac=['74:44:01:81:93:1D','74:44:01:81:93:90','00:18:4D:D7:5B:1D','00:18:4D:D7:5B:17','20:4E:7F:8B:67:02','00:18:4D:D5:46:52','74:44:01:81:93:95','74:44:01:81:93:97','00:1E:2A:DB:DC:3C','00:1B:2F:B0:15:54','00:18:4D:D4:35:E4','00:1E:2A:DB:BD:70','00:18:4D:2E:89:54']

#ping_listemac(lmac)

#Ne marche pas si pdst != ip_destinataire
def test():
    mac='00:1b:2f:b0:15:54'
    macalex='8c:89:a5:02:f3:b4'
    pkt=Ether(dst=macalex)/ARP(pdst="172.24.255.255",hwdst=macalex)
    pkt.show2()
    a=sr1(pkt,retry=1,timeout=1)
    print a
