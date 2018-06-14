#!/bin/bash

# VARS
DESTINATION="./test/"


function jumpto
{
    label=$1
    cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}


echo ""
echo "Welcome to the 'Air Pollution Control'. This script will guide you through the installation of your Raspberry Pi"
echo ""
echo "At first, please type in your identifier you entered at your account. This will allow you to connect your Raspberry with your APC-account."
jumpto _identifier

_identifier:
echo ""
echo "Identifier [Followed by ENTER]: "
read identifier


_url:
echo ""
echo "URL of APC Server [Followed by ENTER]: "
read url

_intervalM:
echo ""
echo "Interval of syncing measures [Followed by ENTER]: "
read intervalM

_intervalC:
echo ""
echo "Interval of syncing config [Followed by ENTER]: "
read intervalC

_check:
echo ""
echo "########################################"
echo "Please check all of your inputs:"
echo -e "ID: \t\t\t'$identifier'"
echo -e "URL: \t\t\t'$url'"
echo -e "Measuring interval: \t'$intervalM'"
echo -e "Configuration interval: '$intervalC'"

while true; do
    echo ""
    read -p "Are your inputs correct? [Y/n]" yn
    case $yn in
        [Y] ) break;;
        [n] ) jumpto _identifier;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

python helper.py config $url $identifier $intervalM $intervalC


# Create destination folder
#mkdir -p ${DESTINATION}

echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
