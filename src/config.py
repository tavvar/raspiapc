import json

class Config:
    'Config object for administrating the Pi\'s configuration'
    
    filename = ""
    configDict = ""
    
    def __init__(self, filename = "config"):
        self.filename = filename
        self.configDict = self.getConfig()
        
        

    def initConfig(self):
        try:
            file = open(self.filename,"r")
            json.load(file)
            print("Success init config")
        except (IOError, ValueError) as err:
            file = open(self.filename,"w")
            file.write(json.dumps({'id':"12345",'interval':30,'url':'http://wasdabyx.de:8080'}))
            print(err)
            print("Standard config has been made.")
        return file.close()


    def getConfig(self):
        result = ""
        file = ""
        try:
            file = open(self.filename,"r")
            result = json.load(file)
        except (IOError, ValueError) as err:
            self.initConfig()
            file = open(self.filename,"r")
            result = json.load(file)
            print("No config or config wasn't valid JSON so initConfig() has been called!")
        file.close()
        self.configDict = result
        return result
   
   
    def updateConfig(self,newConfig):
        try:
            file = open(self.filename,"w+")
        except (IOError) as err:
            print("Not able to create or open file. Error -> %s" % (err))
            return False
        try:
            json.loads(newConfig)
        except ValueError as valerr:
            print("No JSON")
            return False
        file.write(newConfig)                
        file.close()
        return True
        

    def getMachineId(self):
        try:
            file = open("/etc/machine-id","r")
        except IOError:
            file = open("/var/lib/dbus/machine-id","r")
        id = file.read()
        id = id.rstrip()
        file.close()
        return id
    
    def getId(self):
        try:
            return str(self.configDict['id'])
        except KeyError as kerr:
            return False
        except TypeError as terr:
            return False
        except NameError as nerr:
            return False
    
    def getUrl(self):
        try:
            return self.configDict['url']
        except KeyError as kerr:
            return False
        except TypeError as terr:
            return False
        except NameError as nerr:
            return False
    
    def getInterval(self):
        try:
            return int(self.configDict['interval'])
        except KeyError as kerr:
            return False
        except TypeError as terr:
            return False
        except NameError as nerr:
            return False
        
    def getLong(self):
        try:
            return float(self.configDict['long'])
        except KeyError as kerr:
            return False
        except TypeError as terr:
            return False
        except NameError as nerr:
            return False
        
    def getLat(self):
        try:
            return float(self.configDict['lat'])
        except KeyError as kerr:
            return False
        except TypeError as terr:
            return False
        except NameError as nerr:
            return False


if __name__ == '__main__':
    c = self.Config()