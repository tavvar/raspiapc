#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

#cd /
cd ${HOME}/.apc	
DATE="`date +%F_%T`.log" 
mkdir logs
#touch logs/$DATE
stdbuf -oL python main.py > logs/$DATE
#cd /