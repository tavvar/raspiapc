import threading, time, config, request, measure, readht, readdust, requests, json

class Scheduler:
    SENSOR = 22
    PIN = 4
    TEMPURL = "http://wasdabyx.de:8080"
    
    lock = ""
    
    config_obj = ""
    measure_obj = ""
    
    url_config = "http://offline"
    url_measure = "http://offline"
    
    
    
    def __init__(self):
        self.lock = threading.Lock()
        self.config_obj = config.Config()
        self.measure_obj = measure.Measure()
        
        self.url_config = self.config_obj.getUrl()
        
    
    def syncConfig(self):
        self.url_config = self.config_obj.configDict['serverUrl']
        if request.isOnline(self.url_config):
            response = request.getReq(self.url_config)
            if response.status_code == 200:
                try:
                    response = json.loads(response.text)
                except ValueError as valerr:
                    print("No JSON in response. Config wasn't updated.")
                    return False
                self.config_str = response['data']
                self.config_obj.update(config_str)
                return True
        return False       
        
        
    
    def syncMeasures(self, measures=5, id=12345):
        self.url_measure = self.config_obj.configDict['serverUrl']
        humidity, temperature = readht.getAll(self.SENSOR, self.PIN)
        pm25, pm10 = readdust.getAll(measures)
        self.measure_obj.addFetch(humidity, temperature, pm25, pm10, id)
        if request.isOnline(self.url_measure):
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
            self.config_obj.getConfig()
            print("Syncing config...")
            self.syncConfig()
            wait = self.config_obj.configDict['intervalConfig']
            print("Syncing config sleeps %i seconds\n" % (wait))
            self.lock.release()
            time.sleep(wait)
        
    
    def syncMeasuresInterval(self, measures=5, id=12345):
        while True:
            self.lock.acquire()
            self.config_obj.getConfig()
            print("Syncing measures...")
            self.syncMeasures(measures, id)
            wait = self.config_obj.configDict['intervalMeasures']
            print("Syncing measures sleeps %i seconds\n" % (wait))
            self.lock.release()
            time.sleep(wait)
        

        