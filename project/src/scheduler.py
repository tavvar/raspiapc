import threading, time, config, request, measure, readht, readdust, requests

class Scheduler:
    SENSOR = 22
    PIN = 4
    TEMPURL = "https://httpbin.org/put"
    
    lock = ""
    
    config_obj = ""
    measure_obj = ""
    
    url_config = "offline"
    url_measure = "http://wasdabyx.de:8080"
    
    
    
    def __init__(self):
        self.lock = threading.Lock()
        self.config_obj = config.Config()
        self.measure_obj = measure.Measure()
        
        self.url_config = self.config_obj.getUrl()
        
    
    def syncConfig(self):
        if request.isOnline(self.url_config):
            response = request.getReq(self.url_config)
            response = json.loads(response.text)
            self.config_str = response['data']
            self.config_obj.update(config_str)
            if response.status_code == 200:
                return True
        self.config_obj.getConfig()
        return False       
        
        
    
    def syncMeasures(self, measures=5, id=12345):
        humidity, temperature = readht.getAll(self.SENSOR, self.PIN)
        pm25, pm10 = readdust.getAll(measures)
        self.measure_obj.addFetch(humidity, temperature, pm25, pm10, id)
        if request.isOnline("https://httpbin.org"):
            response = requests.put(url=self.url_measure, json=self.measure_obj.getJson())
            print("Debug: Status Code = %i" % (response.status_code))
            print("Debug: Response.text = %s" % (response.text))
            if response.status_code == 200:
                self.measure_obj.deleteFile()
                return True
        return False
    
    
    def syncConfigInterval(self):
        while True:
            self.lock.acquire()
            print("Syncing config...\n")
            self.syncConfig()
            wait = self.config_obj.configDict['intervalConfig']
            print("Syncing config sleeps %i seconds\n" % (wait))
            self.lock.release()
            time.sleep(wait)
        
    
    def syncMeasuresInterval(self, measures=5, id=12345):
        while True:
            self.lock.acquire()
            print("Syncing measures...")
            self.syncMeasures(measures, id)
            wait = self.config_obj.configDict['intervalMeasures']
            print("Syncing measures sleeps %i seconds\n" % (wait))
            self.lock.release()
            time.sleep(wait)
        

        