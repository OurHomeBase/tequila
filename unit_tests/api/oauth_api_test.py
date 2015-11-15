'''Unit tests for client_api.'''

import unittest

from persistence import oauth_models

from unit_tests.common import test_utils
# Disable require.oauth even though it is not used in the module oauth_api.
# It is important because otherwise when run_unit_tests.py is executed it will
# not be disabled.
test_utils.disable_require_oauth()

from api import oauth_api
from utils import constants
import mock


# pylint: disable=missing-docstring
class OAuthApiTest(test_utils.CommonNdbTest):
  '''A class to test client_api model.'''

  def setUp(self):
    test_utils.CommonNdbTest.setUp(self)
    self.client = test_utils.create_oauth_test_client()
    self.app = test_utils.create_flask_test_client(oauth_api)

  def test_load_client_returns_existed(self):
    # Exercise.
    found_client = oauth_api.load_client(constants.CLIENT_ID)

    # Verify
    self.assertEqual(self.client.key, found_client.key)

  def test_load_grant_returns_existed(self):
    # Setup.
    grant = oauth_models.Grant(client_id=constants.CLIENT_ID,
                               code='test_grant')
    grant.put()

    # Exercise.
    loaded_grant = oauth_api.load_grant(constants.CLIENT_ID, 'test_grant')

    # Verify
    self.assertEqual(grant.key, loaded_grant.key)

  def test_save_grant_saves_to_db(self):
    # Setup.
    request = mock.MagicMock()
    request.scopes = 'email'

    code_dict = {'code': 'test_grant'}

    # Exercise.
    saved_grant = oauth_api.save_grant(constants.CLIENT_ID, code_dict, request)

    # Verify
    found_grant = oauth_api.load_grant(constants.CLIENT_ID, 'test_grant')
    self.assertEqual(saved_grant.key, found_grant.key)

if __name__ == "__main__":
  unittest.main()
