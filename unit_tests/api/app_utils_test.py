'''Module to keep common things about testing the NDB models.'''

import unittest
from utils import constants
from api import app_utils
from persistence import oauth_models
from unit_tests.common import test_utils
import mock


# pylint: disable=missing-docstring
class CommonTest(test_utils.CommonNdbTest):

  def test_get_user_id_returns_from_oauth(self):
    # Setup.
    request = mock.MagicMock()
    request.oauth = mock.MagicMock()
    request.oauth.access_token = oauth_models.Token(user_id=123)

    # Exercise.
    actual = app_utils.get_user_id(request)

    # Verify.
    self.assertEqual(123, actual)

  def test_get_pw_for_client(self):
    # Setup.
    test_utils.create_oauth_test_client()

    # Exercise.
    client_secret = app_utils.get_client_secret(constants.CLIENT_ID)

    # Verify
    self.assertEqual(constants.CLIENT_SECRET, client_secret)

if __name__ == "__main__":
  unittest.main()
