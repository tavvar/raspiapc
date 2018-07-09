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
            fo.close()
            return True
        except IOError:
            print("Create File '%s' at '%s'" % (self.filename, os.getcwd()))
            fo = open(self.filename, "w")
            fo.write("{}")
            fo.close()
            return True
        return False
    
    
    def deleteFile(self):
        if(os.path.isfile(self.filename)): 
            try:
                os.remove(self.filename)
            except IOError:
                print("Deletion failed")
                return False
            else:
                print("File '%s' deleted successfully" % (self.filename))
                return True
        print("Deletion failed. No file '%s' found!" % (self.filename))
        return False

    
    def getJson(self):
        try:
            fo = open(self.filename, "r")
        except IOError:
            return False
        jsonPython = json.load(fo)
        fo.close()
        return jsonPython
            
    
    def addFetch(self, humidity, temperature, pm25, pm10, id, long=0.0, lat=0.0, ts=0):
        try:
            float(pm25)
            float(pm10)
            float(humidity)
            float(temperature)
        except ValueError:
            dummy = False
            humidity = temperature = pm25 = pm10 = dummy
            return False
        json2add = {'timestamp':ts,'humidity':humidity,'temperature':temperature,'pm25':pm25,'pm10':pm10,'long':long,'lat':lat}
        json2overwrite = {'id':id,'data':[]}
        json2overwrite['data'].append(json2add)
        data = self.getJson()
        if data == False:
            self.initFile()
            data = json2overwrite
        else:
            print("Update File '%s' at '%s'" % (self.filename, os.getcwd()))
            data['data'].append(json2add)
        fo = open(self.filename, 'w+')
        json.dump(data, fo)
        fo.close()
        return True        
        


if __name__ == '__main__':
    m = Measure()
    m.addFetch(10.0,20.5,1.8,2.4,12345,17.2,11.0)

            
        


