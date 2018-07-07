import threading, time, config, measure, readht, readdust, requests, json, Queue
#import urllib2

class Scheduler:
    SENSOR = 22
    PIN = 4
    interval = 0
    
    lock = ""
    
    config_obj = ""
    measure_obj = ""
    
    
    def __init__(self, interval):
        self.interval = interval
        self.lock = threading.Lock()
        self.config_obj = config.Config()
        self.measure_obj = measure.Measure()
        
        #self.url_config = self.config_obj.getUrl()
       
    def isOnline(self,url):
        try:
            r = requests.get(url)
        except IOError as err:
            print("Url '%s' unreachable. Using local file '%s'" % (url, self.config_obj.filename))
            return False
        return True
    
    
    def syncConfig(self):
        _url = self.config_obj.getUrl()+"/config"
        _id = "id="+str(self.config_obj.getId())
        if self.isOnline(self.config_obj.getUrl()):
            response = requests.get(url=_url, params=_id)
            if response.status_code == 200:
                print("Response data from %s: '%s'" % (_url,response.text))
                try:
                    config_str = json.dumps(response.json())
                except ValueError as valerr:
                    print("No JSON in response. Config wasn't updated.")
                    return False
                else:
                    self.config_obj.updateConfig(config_str)
                    return True
        return False       
        
        
    
    def syncMeasures(self, measures=5):
        url_t = self.config_obj.getUrl()
        id_t = self.config_obj.getId()
        long_t = self.config_obj.getLong()
        lat_t = self.config_obj.getLat()
        
        que = Queue.Queue()
        args_ht = [self.SENSOR, self.PIN, measures]
        ht = threading.Thread(target=lambda q, arg1: q.put(readht.getAll(arg1)), args=(que, measures))
        dust = threading.Thread(target=lambda q, arg1: q.put(readdust.getAll(arg1)), args=(que, measures))
        ht.start()
        dust.start()       
        ht.join()
        dust.join()
        result = que.get()
        humidity_t, temperature_t = result[0], result[1]
        result = que.get()
        pm25_t, pm10_t = result[0], result[1]
        self.measure_obj.addFetch(humidity=humidity_t, temperature=temperature_t, pm25=pm25_t, pm10=pm10_t, id=id_t, long=long_t, lat=lat_t)
        if self.isOnline(url_t):
            response = requests.put(url=url_t, json=self.measure_obj.getJson())
            #print("Debug: Status Code = %i" % (response.status_code))
            #print("Debug: Response.text = %s" % (response.text))
            if response.status_code == 200:
                print("Success in sending file!")
                self.measure_obj.deleteFile()
                return True
        print("File could not be sent due to failing connectivity. Measures are cached locally in file '%s' instead." % (self.measure_obj.filename))
        return False
    
    
    def syncConfigInterval(self):
        while True:
            self.lock.acquire()
            self.config_obj.getConfig()
            print("Syncing config...")
            self.syncConfig()
            wait = self.interval*60
            waitm = self.interval
            print("Syncing config sleeps %i seconds / %f minutes\n" % (wait, waitm))
            self.lock.release()
            time.sleep(wait)
        
    
    def syncMeasuresInterval(self, measures=5):
        while True:
            self.lock.acquire()
            self.config_obj.getConfig()
            id = self.config_obj.getId()
            print("Syncing measures...")
            self.syncMeasures(measures)
            wait = self.config_obj.getInterval()*60
            waitm = wait/60
            print("Syncing measures sleeps %i seconds / %f minutes\n" % (wait, waitm))
            self.lock.release()
            time.sleep(wait)
        

        