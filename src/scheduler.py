import threading, time, config, measure, readht, readdust, requests, json, Queue
#import urllib2

class Scheduler:
    SENSOR = 22
    PIN = 4
    
    lock = ""
    
    config_obj = ""
    measure_obj = ""
    
    
    def __init__(self):
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
##        try:
##            urllib2.urlopen(url, timeout=1)
##            return True
##        except urllib2.URLError as err: 
##            return False
##        except ValueError as valerr:
##            return False
    
    
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
        _url = self.config_obj.getUrl()
        _id = self.config_obj.getId()
        _long = self.config_obj.getLong()
        _lat = self.config_obj.getLat()
        
        que = Queue.Queue()
        args_ht = [self.SENSOR, self.PIN, measures]
        ht = threading.Thread(target=lambda q, arg1: q.put(readht.getAll(arg1)), args=(que, measures))
        dust = threading.Thread(target=lambda q, arg1: q.put(readdust.getAll(arg1)), args=(que, measures))
        ht.start()
        dust.start()       
        ht.join()
        dust.join()
        result = que.get()
        humidity, temperature = result[0], result[1]
        result = que.get()
        pm25, pm10 = result[0], result[1]
        self.measure_obj.addFetch(humidity, temperature, pm25, pm10, _id, long=_long, lat=_lat)
        if self.isOnline(_url):
            response = requests.put(url=_url, json=self.measure_obj.getJson())
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
            wait = 15
            waitm = wait/60
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
        

        