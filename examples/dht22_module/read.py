import sys

import Adafruit_DHT

def getTemp(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return temperature

def getHumidity(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return humidity
	
print getTemp(22,4)
#print getHumidity()
#print getAll(22,4)