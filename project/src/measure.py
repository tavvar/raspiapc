import time
import json
import os

class Measure:
    'Makes a File with Timestamp as name and fills it with Json'
    filename = ""

    def __init__(self, filename = "queue.json"):
        self.filename = filename
        
    def initFile(self):
        try:
            fo = open(self.filename, "r")
        except IOError:
            print("Create File '%s' at '%s'" % (self.filename, os.getcwd()))
            fo = open(self.filename, "w")
            fo.write("{}")
        return fo.close()
    
    
    def deleteFile(self):
        try:
            os.remove(self.filename)
        except IOError:
            print("Deletion failed")
            return False
        else:
            print("File '%s' deleted successful" % (self.filename))
            return True
        return False

    
    def getJson(self):
        try:
            fo = open(self.filename, "r")
        except IOError:
            self.initFile()
            fo = open(self.filename, "r")
            jsonPython = json.load(fo)
        else:
            jsonPython = json.load(fo)
        fo.close()
        return jsonPython
            
    
    def addFetch(self, humidity, temperature, pm25, pm10, ts = "0"):
        ts = int(time.time())
        try:
            float(pm25)
            float(pm10)
            float(humidity)
            float(temperature)
        except ValueError:
            dummy = -999
            humidity = temperature = pm25 = pm10 = dummy
            
        json2add_str = ("{\"%i\" : {\"humidity\" : \"%f\", \"temperature\" : \"%f\", \"pm25\" : \"%f\", \"pm10\" : \"%f\"}}" % (ts, humidity, temperature, pm25, pm10))
        #print(json2add_str)
        json2add = json.loads(json2add_str)
        #print(json2add)
        try:
            fo = open(self.filename, "r+")
            print("Update File '%s'" % (self.filename))
        except IOError:
            self.initFile()
            fo = open(self.filename, "r+")
        data = self.getJson()
        data.update(json2add)
        json.dump(data, fo)
        fo.close()
        
            
    
#testobject = JsonFile()
#testobject.addFetch(47.0, 22.5, 0.75)

            
        


