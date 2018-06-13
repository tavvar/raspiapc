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
echo "Identifier [Followed by ENTER]: "
read identifier
while true; do
    echo ""
    read -p "Your identifier is: '$identifier' ? [Y/n]" yn
    case $yn in
        [Y] ) break;;
        [n] ) jumpto _identifier;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

_url:
echo "URL of APC Server [Followed by ENTER]: "
read url
while true; do
    echo ""
    read -p "The server URL is: '$url' ? [Y/n]" yn
    case $yn in
        [Y] ) break;;
        [n] ) jumpto _url;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

_intervalM:
echo "Interval of syncing measures [Followed by ENTER]: "
read intervalM
while true; do
    echo ""
    read -p "Measuring interval is: '$intervalM' ? [Y/n]" yn
    case $yn in
        [Y] ) break;;
        [n] ) jumpto _intervalM;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

_intervalC:
echo "Interval of syncing config [Followed by ENTER]: "
read intervalC
while true; do
    echo ""
    read -p "Config interval is: '$intervalC' ? [Y/n]" yn
    case $yn in
        [Y] ) break;;
        [n] ) jumpto _intervalC;;
        * ) echo "Please answer Y(es) or n(o). ";;
    esac
done

python helper.py config $url $identifier $intervalM $intervalC


# Create destination folder
#mkdir -p ${DESTINATION}


# Put your logic here (if you need)

echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
