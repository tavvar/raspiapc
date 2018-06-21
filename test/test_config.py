import unittest, time, os, sys, json
from src import config 

class TestConfig(unittest.TestCase):

    #deactivate print()
    #sys.stdout = open(os.devnull, 'w')
    
    @classmethod
    def setUp(cls):
        cls.c = config.Config("test_config")
        cls.ts = time.time()
        
    @classmethod    
    def tearDown(cls):
        try:
            file = open(cls.c.filename, 'r')
            os.remove(cls.c.filename)
        except IOError as io:
            print("ok")
            
    def test_updateConfig_NoValidJSON(self):
        self.assertFalse(self.c.updateConfig("Blub"))
        
    def test_updateConfig_Ok(self):
        self.assertTrue(self.c.updateConfig("{}"))
        
    def test_getConfig_Ok(self):
        conf1 = {'id':"12345",'url':'http://wasdabyx.de:8080','interval':30}
        conf1 = json.dumps(conf1)
        conf2 = json.dumps(self.c.getConfig())
        self.assertEqual(conf1,conf2)
    
    def test_getId_Ok(self):
        self.assertEqual("12345",self.c.getId())
    
    def test_getUrl_Ok(self):
        self.assertEqual("http://wasdabyx.de:8080",self.c.getUrl())
        
    def test_getInterval_Ok(self):
        self.assertEqual(30,self.c.getInterval())
    

if __name__ == '__main__':
    unittest.main()