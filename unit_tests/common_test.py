'''Module to keep common things about testing the NDB models.'''

import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class CommonNdbTest(unittest.TestCase):
  '''Class that prepares testing for NDB.'''

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    ndb.get_context().clear_cache()

  def tearDown(self):
    self.testbed.deactivate()

def create_test_client(api_module):
  api_module.app.config['TESTING'] = True

  return api_module.app.test_client()
