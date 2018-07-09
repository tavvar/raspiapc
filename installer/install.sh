#!/bin/bash

# VARS
DESTINATION=$HOME"/.apc"
DESTINATION_FILE="apc.tar.gz"
DEST_HELPER="helper.py"
RELEASE="https://github.com/tavvar/raspiapc/releases/latest"
ADAFRUIT=$HOME"/Adafruit_Python_DHT"
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
  echo ""
  echo "Sorry, this is no Raspberry. Bye bye!"
  echo ""
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
echo "########################################"

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
sleep 1

# Some inline python...
python << END
import json

filename = "config"
url = "$URL"
id = "$IDENTIFIER"
im = "$INTERVAL"

fo = open(filename, 'w+')
fo.write(json.dumps({'id':id,'interval':im,'url':url}))
fo.close()
print("Everything seems good. Creating 'config' should be done.")
END

echo ""
echo "INFO:"
echo -e "\tIf creating 'config' fails, you can generate your own config file:"
echo -e "\t1. Open terminal"
echo -e "\t2. Do: cd $DESTINATION "
echo -e "\t3. Do: nano config"
echo -e "\t4. Add '{\"id\":\"$IDENTIFIER\",\"url\":\"$URL\",\"interval\":$INTERVAL}' (without quotation mark)"
echo -e "\t5. Save and close the file and be lucky :)"


# Requirements
echo ""
echo "Installing requirements"
echo ""
echo "First install pip and other dependencies..."
sudo apt-get install python-pip build-essential python-dev subversion git
echo ""
echo "And now the pip requirements"
pip install pyserial requests
echo ""
#echo "Apt-get dependecies:"
#sudo apt-get install build-essential python-dev subversion git
#sudo apt-get install curl wget jq

sleep 0.5
echo ""
echo "Clean the installation path"
sleep 0.5

sudo rm -rf ${DESTINATION} --verbose
sleep 1

echo ""
echo "Get the Files from APC Repository..."
sleep .5
echo ""
##dl=$(curl -s https://api.github.com/repos/tavvar/raspiapc/releases/latest | \jq --raw-output '.assets[0] | .browser_download_url')
##wget -O ${DESTINATION_FILE} $dl --limit-rate=100k

svn export https://github.com/tavvar/raspiapc/trunk/src $DESTINATION
echo ""
echo "Move 'config' to program directory..."
mv $CFG ${DESTINATION} --verbose
echo ""

##echo "Extract files and move them..."
##sleep 1
### Extract the archive
##mkdir ${DESTINATION} --verbose
##echo ""
##tar -xzf ${DESTINATION_FILE} -C ${DESTINATION} --verbose
##echo ""

sleep 0.5


# install Adafruit lib
echo ""
echo "##########################"
echo "Trying to install the Adafruit DHT library..."
sleep 1
if [[ ! -d $ADAFRUIT ]]; then
    echo "Cloning Adafruit repository..."
    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd $ADAFRUIT
    sudo python setup.py install
    cd $HOME
else
    echo "---> Adafruit repository already installed. Skip this step!"
    echo "Install the lib..."
    sleep .5
    cd $ADAFRUIT
    sudo python setup.py install
    cd $HOME
fi
echo "##########################"


sleep 1
echo ""
echo ""
echo ""
echo "Adding Air Pollution Control to the Raspbian startup?"
sleep 1


# Adding program to autostart
while true; do
    echo ""
    read -p "Are you sure? [Y/n]" yn1
    case $yn1 in
        [Y] ) break;;
        [n] ) jumpto _complete;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

_startup:
echo ""
echo "Make the launcher launchable."
cd ${DESTINATION}
chmod 755 launcher.sh --verbose
echo ""
echo "Add APC launcher to crontab..."
mkdir $DESTINATION"/log" --verbose
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
##echo "@reboot sh ${DESTINATION}/launcher.sh" >> mycron
echo "@reboot sudo sleep 10 && ${DESTINATION}/./launcher.sh &" >> mycron
#install new cron file
crontab mycron
rm mycron
echo "Added to Crontab"


_restart:
# Restart
echo ""
echo "Your computer will restart in 10seconds. To break press CTRL+C"
secs=$((10))
while [ $secs -gt 0 ]; do
   echo -ne "     Remaining $secs\033[0K\r "
   sleep 1
   : $((secs--))
done
sudo reboot

_complete:
echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
