import threading, config, request

class Scheduler:
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
        self.url_config = config_obj.getUrl()
        
    
    def syncConfig(self):
        if request.isOnline(self.url):
            response = request.getReq(self.url)
            response = json.loads(response.text)
            config_str = response['data']
            config_obj.update(config_str)            
            return True
        return False       
        
        
    
    def syncMeasures():
        print("ToDo")
        
        
    def newThread(self, method, intervalType):
        lock = threading.acquire()
        method()
        lock = threading.release()
        if intervalType == "config"
            time.sleep(int(config_str['intervalConfig']))
            
        elif intervalType == "measure"
            time.sleep(int(config_str['intervalMeasure']))
        