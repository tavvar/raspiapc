import json

class Config:
    'Config object for administrating the Pi\'s configuration'
    
    filename = ""
    configDict = ""
    
    def __init__(self, filename = "config"):
        self.filename = filename
        #blubb = initConfig()
        self.configDict = self.getConfig()
        
        

    def initConfig(self):
        try:
            file = open(self.filename,"r")
            json.load(file)
            print("Success init config")
        except (IOError, ValueError) as err:
            file = open(self.filename,"w")
            file.write(json.dumps({'id':self.getMachineId(),'intervalMeasures':30,'intervalConfig':10,'serverUrl':'https://httpbin.org'}))
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
        if (newConfig is not None):
            try:
                file = open(self.filename,"w+")
            except (IOError) as err:
                print("Not able to create or open file. Error -> %s" % (err))
            file.write(newConfig)                
            file.close()
            return True
        return False
        
    
    def getUrl(self,platzhalter=True):
        #what are parts of the url?
        if platzhalter:
            return "abcde"
        else:
            return "http://httpbin.org"
        

    def getMachineId(self):
        try:
            file = open("/etc/machine-id","r")
        except IOError:
            file = open("/var/lib/dbus/machine-id","r")
        id = file.read()
        id = id.rstrip()
        file.close()
        return id
    
