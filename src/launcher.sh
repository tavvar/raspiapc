#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

#cd /
cd ${HOME}/.apc
stdbuf -oL python main.py & > log
#cd /