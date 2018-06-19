#!/bin/bash

# VARS
DESTINATION=$HOME"/.apc"
DESTINATION_FILE="apc.tar.gz"
DEST_HELPER="helper.py"
RELEASE="https://github.com/tavvar/raspiapc/releases/latest"
ADAFRUIT=$DESTINATION"/lib/Adafruit_Python_DHT"
CFG="config"


function jumpto
{
    label=$1
    cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}


OS_VERSION=$(< /etc/os-release)
RASPI=0
if [[ $OS_VERSION = *"raspbian"* ]]; then
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

# Requirements
echo ""
echo "Installing requirements"
echo ""
echo "First install pip"
sudo apt-get install python-pip
echo ""
echo "And now the pip requirements"
pip install pyserial
echo ""
echo "Apt-get dependecies:"
sudo apt-get install curl wget jq build-essential python-dev

sleep 1


echo ""
echo "Initialize 'config'..."
echo ""
sleep 1

python ${DEST_HELPER} $CFG $URL $IDENTIFIER $INTERVAL

sleep 1
echo ""
echo "Clean the installation path"

sudo rm -rf ${DESTINATION} --verbose
sleep 1

#echo "Remove old file..."
#rm -f ${HOME}/${DESTINATION_FILE}

echo ""
echo "Get the Files from APC Repository..."
sleep .5
echo ""
dl=$(curl -s https://api.github.com/repos/tavvar/raspiapc/releases/latest | \jq --raw-output '.assets[0] | .browser_download_url')
wget -O ${DESTINATION_FILE} $dl --limit-rate=100k
#wget -O ${HOME}/${DESTINATION_FILE} ${RELEASE} --limit-rate=100k
echo ""


echo "Extract files and move them..."
sleep 1
# Extract the archive
mkdir ${DESTINATION} --verbose
echo ""
tar -xzf ${DESTINATION_FILE} -C ${DESTINATION} --verbose
echo ""
mv $CFG ${DESTINATION} --verbose

sleep 1

# install Adafruit lib
echo ""
echo "##########################"
echo "Trying to install the Adafruit DHT library..."
echo ""
cd $ADAFRUIT
sudo python setup.py install

sleep .5
echo ""
echo ""
echo ""
echo "Adding Air Pollution Control to the Raspbian startup?"
sleep 1
# Adding program to autostart
while true; do
    echo ""
    read -p "Are your inputs correct? [Y/n]" yn
    case $yn in
        [Y] ) jumpto _autostart;;
        [n] ) jumpto _restart;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

_autostart
echo ""
echo "Make the launcher launchable."
cd ${DESTINATION}
chmod 755 launcher.sh --verbose
echo ""
echo "Add APC launcher to crontab..."
mkdir $DESTINATION"/log" --verbose
crontab @reboot sh $DESTINATION"/launcher.sh >"$DESTINATION"/logs/cronlog 2>&1"


_restart
# Restart
echo ""
echo "The process will restart in 10seconds..."
sleep 10
sudo reboot

echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
