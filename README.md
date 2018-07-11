[![Build Status](https://travis-ci.org/tavvar/raspiapc.svg?branch=master)](https://travis-ci.org/tavvar/raspiapc)

# raspiapc
Repository for project 'Air Pollution Control'. It only contains code for the Raspberry Pi part e.g. python scripts to retreive data from both implemented sensors (DHT22, SDS011) etc.

Main repository: https://github.com/sweigel1/RichClientApplicationDevelopment


# How to Use
## Requirements:
- Raspberry Pi (Raspberry Pi 3b is recommended) with Raspbian Stretch
- Dustsensor SDS011
- Humidity and Temperature sensor DHT22
## Installation
You can clone the repository or just download the [install.sh](https://github.com/tavvar/raspiapc/blob/master/installer/install.sh) from [/installer/](https://github.com/tavvar/raspiapc/blob/master/installer/).
Open the terminal and make *install.sh* executable and run it:
```bash
chmod +x install.sh && ./install.sh
```
The installer will load the requiered dependencies.
## Run
To run the measuring go to the new created directory and execute *main.py* with Python (not Python3).
```bash
cd ${HOME}/.apc && python main.py
```

# Source Code: Examples
## config.py
Updates the Config file with the new config in json format. Important: parameter *newConfig* is a json string, no python dictionary!
```python
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
```

## measure.py
Generates a new file (standard: queue.json) and fills it with sensor data in json format.
```python
def addFetch(self, humidity, temperature, pm25, pm10, id, long=0.0, lat=0.0, ts=0):
        try:
            float(pm25)
            float(pm10)
            float(humidity)
            float(temperature)
        except ValueError:
            dummy = False
            humidity = temperature = pm25 = pm10 = dummy
            return False
        json2add = {'timestamp':ts,'humidity':humidity,'temperature':temperature,'pm25':pm25,'pm10':pm10,'long':long,'lat':lat}
        json2overwrite = {'id':id,'data':[]}
        json2overwrite['data'].append(json2add)
        data = self.getJson()
        if data == False:
            self.initFile()
            data = json2overwrite
        else:
            try:
                data['data'].append(json2add)
                print("Update File '%s' at '%s'" % (self.filename, os.getcwd()))
            except KeyError as kerr:
                data = json2overwrite
                print("Corrupt data. Create File '%s' at '%s'" % (self.filename, os.getcwd()))
        fo = open(self.filename, 'w+')
        json.dump(data, fo)
        fo.close()
return True 
```
### Example json
```json
{
        "id" : "<id>", 
        "data": [
                        {
                                "humidity":35.5, 
                                "temperature":22.4, 
                                "pm25":1.2, 
                                "pm10":10.3, 
                                "long":40.58, 
                                "lat":68.6, 
                                "timestamp":12345678
                        }
        ]
}
```

## scheduler.py
### function syncConfig()
Does a GET-request to the url of the server with couchDB (read from local config which is synchronized with couchDB). The actual config is in the response as json. If the server is unreachable, the scheduler function uses the local config for next measure instead.
```python
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
```

### function syncMeasures()
Does a PUT-Request with the *queue.json* as data. The target url is extracted from the local *config* file. If the server is unreachable, the function *addFetch* stores the measured data in local file *queue.json* instead.
```python
def syncMeasures(self, measures=5):
        url_t = self.config_obj.getUrl()
        id_t = self.config_obj.getId()
        long_t = self.config_obj.getLong()
        lat_t = self.config_obj.getLat()
        timestamp = int(time.time())
        print("Time: %i" % (timestamp))
        
        dht22 = readht.getAll(measures)
        humidity_t = dht22[0]
        temperature_t = dht22[1]
        
        sds011 = readdust.getAll(measures)
        pm25_t = sds011[0]
        pm10_t = sds011[1]
        
        self.measure_obj.addFetch(humidity=humidity_t, temperature=temperature_t, pm25=pm25_t, pm10=pm10_t, id=id_t, long=long_t, lat=lat_t, ts=timestamp)
        timestamp = int(time.time())
        if self.isOnline(url_t):
            response = requests.put(url=url_t, json=self.measure_obj.getJson())
            if response.status_code == 200:
                print("Success in sending file!")
                self.measure_obj.deleteFile()
                return True
        print("File could not be sent due to failing connectivity. Measures are cached locally in file '%s' instead." % (self.measure_obj.filename))
return False
```

# Tests
