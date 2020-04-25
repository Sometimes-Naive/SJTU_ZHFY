import sys, pprint
sys.path.append('/var/www/CourtDataVisualization')
# import unittest
from django.test import TestCase
from core.drivers import *
from mongoengine import *

class TestDrivers(TestCase):
    """Test mathfuc.py"""

    @classmethod
    def setUpClass(cls):
        print ("this setupclass() method only called once.\n")

    @classmethod
    def tearDownClass(cls):
        print ("this teardownclass() method only called once too.\n")

    def setUp(self):
        print ("do something before test : prepare environment.\n")

    def tearDown(self):
        print ("do something after test : clean up.\n")

    def test_connect_mongo(self):

        @connect_mongo('app_test')
        def fetch_mongo_version():
            doc = MongoConnectionSettingsDoc.objects.all()
            print(doc)
            print(111111)
            return doc.mode
        try:    
            mongo_mode = fetch_mongo_version()
            self.assertEqual(mongo_mode, 'single')
        except Exception as err:
            print('exception', err)
            return False


    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

class MongoConnectionSettingsDoc(Document):
    meta = {
        'collection': 'connection_settings'
    }
    mode = StringField()

# if __name__ == '__main__':

#     print(__file__)
#     print(sys.builtin_module_names, sys.path)
#     unittest.main()