#!/bin/bash

# VARS
DESTINATION="./test/"
ID=""


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


# Create destination folder
#mkdir -p ${DESTINATION}


# Put your logic here (if you need)

echo ""
echo "Installation complete."
echo ""

# Exit from the script with success (0)
exit 0
