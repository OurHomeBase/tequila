'''Unit tests for user_models.'''

import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from persistence import user_models

# pylint: disable=missing-docstring
class UserModelsTest(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    ndb.get_context().clear_cache()

  def tearDown(self):
    self.testbed.deactivate()

  def test_find_by_username_returns_expected_user(self):
    # Setup.
    created_user = user_models.User(username='my_user')
    created_user.put()

    # Exercise.
    found_user = user_models.User.find_by_username('my_user')

    # Verify
    self.assertTrue(found_user)
    self.assertEqual(created_user.key, found_user.key)

if __name__ == "__main__":
  unittest.main()
