import unittest, time, os, sys
from src import measure 

class TestMeasure(unittest.TestCase):

    #deactivate print()
    sys.stdout = open(os.devnull, 'w')
    
    @classmethod
    def setUp(cls):
        cls.m = measure.Measure("test_queue.json")
        cls.ts = time.time()
        
    @classmethod    
    def tearDown(cls):
        os.remove(cls.m.filename)
            
    def test_addFetchFailWrongParam(self):
        self.assertFalse(self.m.addFetch(humidity="String", temperature=25.5, pm25=5.0, pm10=10.0, id="abc123", ts=self.ts))
        
        
    def test_addFetchOK(self):
        self.assertTrue(self.m.addFetch(humidity=50.0, temperature=25.5, pm25=5.0, pm10=10.0, id="abc123", ts=self.ts))
        
    

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMeasure)
    unittest.TextTestRunner(verbosity=2).run(suite)