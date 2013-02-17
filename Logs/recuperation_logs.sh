#! /bin/bash

#recupere les logs de DHCP et de DC++ sur rezo 
#   -> fichier logdhcp et logdcpp dans le repertoire ~/Monitoring
#on rajoute des pauses pour attendre la creation des fichiers

# Se lance quotidiennement par tache cron

#Connection ssh grace à une clé RSA 

scp rezo@172.24.0.10:/var/lib/dhcp3/dhcpd.leases ~/Monitoring/logdhcp;
sleep 5;

ssh rezo@172.24.0.10 'sudo cp -r .opendchub/log logdcpp; sudo chmod a+rw logdcpp;';
sleep 5; 
scp rezo@172.24.0.10:logdcpp ~/Monitoring/logdcpp ;
sleep 5;
ssh rezo@172.24.0.10 'rm logdcpp;';
sleep 5;