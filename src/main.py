import request
import measure
import time
import readht
import readdust
import os
import json

SENSOR = 22
PIN = 4
WAITBTWMEASURES = 10

testobject = measure.Measure() 

#url = "http://httpbin.org"
url = "https://google.com"

while True:
    print("fetching humidity and temperature")
    humidity, temperature = readht.getAll(SENSOR,PIN)
    print(">>> humidity: %f, temperature: %f" % (humidity, temperature))
    print("fetching dust")
    pm25, pm10 = readdust.getAll(2)
    print(">>> pm25: %f, pm10: %f" % (pm25, pm10))
    testobject.addFetch(humidity, temperature, pm25, pm10)
    print("Add values to '%s/%s'" % (os.getcwd(), testobject.filename))
    data = json.dumps(testobject.getJson())
    #print(request.sendData(url,data))
    if request.isOnline(url):
        print("Just a dummy send")
        print("Data was sent to %s" % (url))
        testobject.deleteFile()
    else:
        print("Data saved to local file '%s'" % (testobject.filename))
    print("Success! Wait %i seconds for new measure...\n\n" % (WAITBTWMEASURES))
    time.sleep(WAITBTWMEASURES)

