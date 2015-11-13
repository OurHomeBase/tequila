'''Module to keep common things about testing the NDB models.'''

import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from flask_oauthlib import provider
from mock import patch

from api import common
from utils import constants
from persistence import oauth_models

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

def create_flask_test_client(api_module):
  api_module.app.config['TESTING'] = True

  return api_module.app.test_client()

def create_oauth_test_client():
  '''Creates test OAuth Client'''
  client = oauth_models.Client(client_id=constants.CLIENT_ID,
                               client_secret=constants.CLIENT_SECRET)
  client.put()

  return client

def disable_require_oauth():
  '''Disables oauth.require_oauth decorator.

  Please note: the function should be called in a test before corresponding an api
  module is imported in the test.
  '''
  class StubbedOAuth2Provider(provider.OAuth2Provider):
    def require_oauth(self, *scopes): # pylint: disable=unused-argument
      return lambda x: x

  patch.object(provider, 'OAuth2Provider', StubbedOAuth2Provider).start()

def mock_get_user_id(test_case, user_id):
  '''Mocks api.common.get_user_id with a given user_id.

  Args:
    test_object: instance of unittest.TestCase.
    user_id: an int.
  '''
  patcher = patch.object(common, 'get_user_id', return_value=user_id)
  patcher.start()
  test_case.addCleanup(patcher.stop)
