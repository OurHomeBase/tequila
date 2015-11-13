'''Unit tests for client_api.'''

import unittest

from utils import constants
from persistence import user_models

from unit_tests.common import common_test
common_test.disable_require_oauth()

from api import user_api

import json


# pylint: disable=missing-docstring
class UserApiTest(common_test.CommonNdbTest):
  '''A class to test client_api model.'''

  def setUp(self):
    common_test.CommonNdbTest.setUp(self)
    self.app = common_test.create_flask_test_client(user_api)

  def test_get_pw_for_client(self):
    # Setup.
    common_test.create_oauth_test_client()

    # Exercise.
    client_secret = user_api.get_pw(constants.CLIENT_ID)

    # Verify
    self.assertEqual(constants.CLIENT_SECRET, client_secret)

  def test_get_user_returns_user_if_not_exists(self):
    # Setup.
    user = user_models.User(username='test_user')
    user.put()
    common_test.mock_get_user_id(self, user.key.id())

    # Exercise.
    response = self.app.get('/api/user/me')

    # Verify
    self.assertEqual(200, response.status_code)
    user_json = json.loads(response.data)
    self.assertEqual('test_user', user_json['username'])


if __name__ == "__main__":
  unittest.main()
