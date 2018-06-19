#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd ${HOME}.apc
python main.py > ${HOME}.apc/log/log
cd /