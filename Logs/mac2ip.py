#!/usr/bin/python
#encoding: latin1

import netaddr
import datetime
import sqlite3


def mac2ip(strmac):
    mac=netaddr.EUI(strmac)

    conn=sqlite3.connect('leases.db')
    curs=conn.cursor()
    req='SELECT ip FROM leases WHERE mac=%d ' % int(mac)
    curs.execute(req)
    ipint=curs.fetchall()
    if len(ipint)>0:
        ipint=ipint[0]
    if len(ipint)>0:
        ipint=int(ipint[0])
        ip=netaddr.IPAddress(int(ipint))
        print mac,ip


lmac=['74:44:01:81:93:1D','74:44:01:81:93:90','00:18:4D:D7:5B:1D','00:18:4D:D7:5B:17','20:4E:7F:8B:67:02','00:18:4D:D5:46:52','74:44:01:81:93:95','74:44:01:81:93:97','00:1E:2A:DB:DC:3C','00:1B:2F:B0:15:54','00:18:4D:D4:35:E4','00:1E:2A:DB:BD:70','00:18:4D:2E:89:54']

for s in lmac:
    mac2ip(s)



