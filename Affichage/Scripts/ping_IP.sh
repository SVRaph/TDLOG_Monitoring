#!/bin/bash

#reponse recue
ping -c 1 $1 | grep 'bytes from' > Scripts/pingIP.txt
#hote inatteignable
ping -c 1 $1 | grep 'Unreachable' >> Scripts/pingIP.txt
#time to live depace
ping -c 1 $1 | grep 'exceeded' >> Scripts/pingIP.txt
