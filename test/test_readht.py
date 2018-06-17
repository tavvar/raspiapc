import unittest, time, os, sys, mock
from mock_import import mock_import
#from unittest.mock import patch
#from src import readht 

class TestReadht(unittest.TestCase):

    #deactivate print()
    #sys.stdout = open(os.devnull, 'w')
    
    @classmethod
    def setUp(cls):
        print('')
        
    @classmethod    
    def tearDown(cls):
        print('')
    
    def test_Test(self):
        print('')
        with mock_import():
            from src import readht
            mock.patch('readht.getAll', return_value=(22.3,30.2))
            #a,b = readht.getAll(22,4)
            #print("blub: %f %f" % (readht.getAll()))
            #self.assertEqual(readht.getAll(22,4), (22.3,30.2))
        

if __name__ == '__main__':
    unittest.main()