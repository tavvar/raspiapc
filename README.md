[![Build Status](https://travis-ci.org/tavvar/raspiapc.svg?branch=master)](https://travis-ci.org/tavvar/raspiapc)

# raspiapc
Repository for project 'Air Pollution Control'. It only contains code for the Raspberry Pi part e.g. python scripts to retreive data from both implemented sensors (DHT22, SDS011) etc.

Main repository: https://github.com/sweigel1/RichClientApplicationDevelopment


# How to Use
## Requirements:
- Raspberry Pi (Raspberry Pi 3b is recommended) with Raspbian Stretch
- Dustsensor SDS011
- Humidity and Temperature sensor DHT22
## Installation
You can clone the repository or just download the [install.sh](https://github.com/tavvar/raspiapc/blob/master/installer/install.sh) from [/installer/](https://github.com/tavvar/raspiapc/blob/master/installer/).
Open the terminal and make *install.sh* executable and run it:
```bash
chmod +x install.sh && ./install.sh
```
The installer will load the requiered dependencies.
## Run
To run the measuring go to the new created directory and execute *main.py* with Python (not Python3).
```bash
cd ${HOME}/.apc && python main.py
```
