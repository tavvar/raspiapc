import sys, time

import Adafruit_DHT

def getTemp(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return temperature

def getHumidity(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return humidity
	
def getAllDepreciated(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	return humidity, temperature
    
def getAll(sensor, pin, measures):
    print("   DHT22 sensor:")
    humidity = temperature = 0.0
    for t in range(measures):
        h, t = Adafruit_DHT.read_retry(sensor, pin)
        if (h is not None) & (t is not None):
            print("Humidity: ", h, ", Temperature: ", t)
            humidity += h
            temperature += t
            time.sleep(2)
    humidity = humidity/measures
    temperature = temperature/measures
    print("Averages: Humidity = %f, Temperature = %f" % (humidity, temperature))
    return humidity, temperature

#print getTemp(22,4)
#print getHumidity(22,4)
#print getAll(22,4)
