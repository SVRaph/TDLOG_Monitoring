#!/bin/bash

ips="172.24.0.1 172.24.0.10 172.24.0.21 172.24.0.23 172.24.0.30 172.24.0.100 172.24.0.101 172.24.0.103 172.24.0.104 172.24.0.111 172.24.0.112 172.24.0.113 172.24.0.114 172.24.0.121 172.24.0.122 172.24.0.131 172.24.0.132 172.24.0.133 172.24.0.141 172.24.0.142 172.24.0.143 172.24.0.144 172.24.0.203 172.24.0.204 195.221.194.14"

echo "Réponse en ping des adresses IP connues" > Scripts/switchs_connus_reponse_ping.txt

for ip in $ips 
do
	echo -n "$ip " >> Scripts/switchs_connus_reponse_ping.txt
	if ping -c1 $ip 
	then
		echo 0 >> Scripts/switchs_connus_reponse_ping.txt
	else
		echo 1 >> Scripts/switchs_connus_reponse_ping.txt
	fi
done

