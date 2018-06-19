#!/bin/bash

# VARS
DESTINATION=$HOME"/.apc"
DESTINATION_FILE="apc.tar.gz"
DEST_HELPER="helper.py"
RELEASE="https://github.com/tavvar/raspiapc/releases/download/0.0.1/apc_0.0.1.tar.gz"


function jumpto
{
    label=$1
    cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}


OS_VERSION=$(< /etc/os-release)
RASPI=0
if [[ $OS_VERSION = *"mint"* ]]; then
  RASPI=0
else
  RASPI=1
  echo "Sorry, this is no Raspberry. Bye bye!"
  exit 1
fi


echo ""
echo "Welcome to the 'Air Pollution Control'. This script will guide you through the installation of your Raspberry Pi"
echo ""
echo "At first, please type in your identifier you entered at your account. This will allow you to connect your Raspberry with your APC-account."
jumpto _identifier

_identifier:
echo ""
echo "Identifier [Followed by ENTER]: "
read IDENTIFIER
if [ -z "$IDENTIFIER" ]; then
    echo "Please type in something"
    jumpto _identifier
fi

_url:
echo ""
echo "URL of APC Server (Standard: http://wasdabyx.de:8080) [Followed by ENTER]: "
read URL
if [ -z "$URL" ]; then
    URL="http://wasdabyx.de:8080";
fi

_interval:
echo ""
echo "Interval of syncing measures in minutes (Standard: 10)  [Followed by ENTER]: "
read INTERVAL
if [ -z "$INTERVAL" ]; then
    INTERVAL="10";
fi


_check:
echo ""
echo "########################################"
echo "Please check all of your inputs:"
echo -e "ID: \t\t\t'$IDENTIFIER'"
echo -e "URL: \t\t\t'$URL'"
echo -e "Measuring interval: \t'$INTERVAL'"

while true; do
    echo ""
    read -p "Are your inputs correct? [Y/n]" yn
    case $yn in
        [Y] ) break;;
        [n] ) jumpto _identifier;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done


echo ""
echo "Initialize 'config'..."
echo ""

python ${DEST_HELPER} config $URL $IDENTIFIER $INTERVAL

echo ""

rm -rf ${DESTINATION} --verbose
rm -rf ${HOME}/${DESTINATION_FILE}${DESTINATION} --verbose

wget -O ${HOME}/${DESTINATION_FILE} ${RELEASE} --limit-rate=100k
echo ""

# Extract the archive
mkdir ${DESTINATION} --verbose
echo ""
tar -xzf ${HOME}/${DESTINATION_FILE} -C ${DESTINATION} --verbose

echo ""
mv config ${DESTINATION} --verbose

# Requirements
echo ""
echo "Installing requirements"
pip install --user requests


# install Adafruit lib
echo ""
echo "Trying to install the Adafruit DHT library..."
sudo python ${DESTINATION}/lib/Adafruit_Python_DHT/setup.py install


# Adding program to autostart

# Starting program

echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
