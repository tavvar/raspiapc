import threading, config, request, measure, readht, readdust

class Scheduler:
    SENSOR = 22
    PIN = 4
    
    url_config = ""
    url_measure = ""
    
    intervalMeasures = 0
    intervalConfig = 0
    lock = ""
    
    config_obj = ""
    measure_obj = ""
    
    
    
    def __init__(self):
        self.lock = threading.Lock()
        self.config_obj = config.Config()
        self.measure_obj = measure.Measure()
        
        self.url_config = config_obj.getUrl()
        
    
    def syncConfig(self):
        if request.isOnline(self.url_config):
            response = request.getReq(self.url_config)
            response = json.loads(response.text)
            config_str = response['data']
            config_obj.update(config_str)
            if response.status_code == 200:
                return True
        return False       
        
        
    
    def syncMeasures(self):
        humidity, temperature = readht.getAll(SENSOR,PIN)
        pm25, pm10 = readdust.getAll(5)
        measure_obj.addFetch(humidity, temperature, pm25, pm10)
        if request.isOnline(self.url_measure):
            response = requests.put(url=self.url_measure, json=self.measure_obj.getJson)           
            if response.status_code == 200:
                self.measure_obj.deleteFile()
                return True
        return False  
        

        