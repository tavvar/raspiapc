import sys, time, logging

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
    
def getAll(measures):
    return getAll3(22,4,measures)
    
def getAll3(sensor, pin, measures):
    humidity = temperature = 0.0
    false_m_h = 0
    false_m_t = 0
    for t in range(measures):
        h, t = Adafruit_DHT.read_retry(sensor, pin)
        if (h is not None) and (t is not None):
            print("DHT22\t-> Humidity: %f, Temperature: %f" % (h,t))
            if (0 <= h <= 100):
                humidity += h
            else:
                false_m_h += 1
            if (-80 <= t <= 80):
                temperature += t
            else:
                false_m_t += 1
            time.sleep(2)
    humidity = humidity/(measures-false_m_h)
    temperature = temperature/(measures-false_m_t)
    print("DHT22\t-> Averages: Humidity = %f, Temperature = %f" % (humidity, temperature))
    result = [humidity, temperature]
    return result

#print getTemp(22,4)
#print getHumidity(22,4)
#print getAll(22,4)
