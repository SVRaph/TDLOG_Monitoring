#!/usr/bin/python
#encoding: latin1

import sys
sys.path.append("../dhcp")
sys.path.append("../dcpp")

import outils_dates as o_d
import traitement_dhcp_leases as t_dhcp
import traitement_dcpp as t_dcpp

if __name__=='__main__':
    o_d.tests_outils_date()
    #t_dhcp.tests()
    #t_dcpp.tests()

