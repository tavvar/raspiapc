import threading, config, request, measure, readht, readdust, requests

class Scheduler:
    SENSOR = 22
    PIN = 4
    TEMPURL = "https://httpbin.org/put"
    
    url_config = ""
    url_measure = TEMPURL
    
    intervalMeasures = 0
    intervalConfig = 0
    lock = ""
    
    config_obj = ""
    measure_obj = ""
    
    
    
    def __init__(self):
        self.lock = threading.Lock()
        self.config_obj = config.Config()
        self.measure_obj = measure.Measure()
        
        self.url_config = self.config_obj.getUrl()
        
    
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
        humidity, temperature = readht.getAll(self.SENSOR, self.PIN)
        pm25, pm10 = readdust.getAll(1)
        self.measure_obj.addFetch(humidity, temperature, pm25, pm10)
        if request.isOnline("https://httpbin.org"):
            response = requests.put(url=self.url_measure, json=self.measure_obj.getJson())
            print("Debug: Status Code = %i" % (response.status_code))
            print("Debug: Response.data = %s" % (response.data))
            if response.status_code == 200:
                self.measure_obj.deleteFile()
                return True
        return False  
        

        