import unittest, time, os, sys
from src import config 

class TestConfig(unittest.TestCase):

    #deactivate print()
    sys.stdout = open(os.devnull, 'w')
    
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
            
    def test_updateConfigFailNoValidJSON(self):
        self.assertFalse(self.c.updateConfig("Blub"))
        
    def test_updateConfigOk(self):
        self.assertTrue(self.c.updateConfig("{}"))    
    

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMeasure)
    unittest.TextTestRunner(verbosity=2).run(suite)