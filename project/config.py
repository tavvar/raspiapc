import json

class Config:
    'Config object for administrating the Pi\'s configuration'
    
    def __init__(self, filename = "config"):
        self.filename = filename
        

    def initConfig(self):
        try:
            file = open(self.filename,"r")
            json.load(file)
            print("Success init config")
        except (IOError, ValueError) as err:
            file = open(filename,"w")
            file.write(json.dumps({'id':getMachineId(),'intervalMeasures':30,'intervalConfig':10}))
            print(err)
            print("Standard config has been made.")
        return file.close()

    def importConfig(self):
        result = ""
        try:
            file = open(self.filename,"r")
            result = json.load(file)
        except (IOError, ValueError) as err:
            initConfig(self.filename)
            file = open(self.filename,"r")
            result = json.load(file)
            print("No config or config wasn't valid JSON so initConfig() has been called!")
        file.close()
        return result

    def getMachineId():
        try:
            file = open("/etc/machine-id","r")
        except IOError:
            file = open("/var/lib/dbus/machine-id","r")
        id = file.read()
        id = id.rstrip()
        file.close()
        return id

    def syncValues():
    
