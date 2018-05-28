import request
import jsonObject
import time
import readht
import readdust
import os

SENSOR = 22
PIN = 4
WAITBTWMEASURES = 10

testobject = jsonObject.JsonFile() 

#url = "http://httpbin.org"
url = "abc"

while True:
    print("fetching humidity and temperature")
    humidity, temperature = readht.getAll(SENSOR,PIN)
    print(">>> humidity: %f, temperature: %f" % (humidity, temperature))
    print("fetching dust")
    pm25, pm10 = readdust.getAll(2)
    print(">>> pm25: %f, pm10: %f" % (pm25, pm10))
    testobject.addFetch(humidity, temperature, pm25, pm10)
    print("Add values to '%s/%s'" % (os.getcwd(), testobject.filename))
    data = jsonObject.json.dumps(testobject.getJson())
    #print(request.sendData(url,data))
    if request.sendData(url,data):
        print("Data was sent to %s" % (url))
        testobject.deleteFile()
    else:
        print("Data saved to local file '%s'" % (testobject.filename))
    print("Success! Wait %i seconds for new measure...\n\n" % (WAITBTWMEASURES))
    time.sleep(WAITBTWMEASURES)


