'''Unit tests for client_api.'''

import unittest

from persistence import oauth_models

from unit_tests.common import test_utils
# Disable require.oauth even though it is not used in the module oauth_api.
# It is important because otherwise when run_unit_tests.py is executed it will
# not be disabled.
test_utils.disable_require_oauth()

from persistence import user_models

from api import oauth_api
from utils import constants
import mock
import json


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

  def test_load_token_by_access_token_returns_existing_token(self):
    # Setup.
    token = oauth_models.Token(
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_type='Bearer',
        scopes=['email'],
        client_id=constants.CLIENT_ID,
        user_id=123)

    token.put()

    # Exercise.
    loaded_token = oauth_api.load_token('test_access_token', None)

    # Verify
    self.assertEqual(token.key, loaded_token.key)

  def test_load_token_by_refresh_token_returns_existing_token(self):
    # Setup.
    token = oauth_models.Token(
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        token_type='Bearer',
        scopes=['email'],
        client_id=constants.CLIENT_ID,
        user_id=123)

    token.put()

    # Exercise.
    loaded_token = oauth_api.load_token(None, 'test_refresh_token')

    # Verify
    self.assertEqual(token.key, loaded_token.key)

  def test_save_token_deletes_old_and_saves_new(self):
    # Setup.
    old_token = oauth_models.Token(
        access_token='access_token_1',
        refresh_token='refresh_token_2',
        token_type='Bearer',
        scopes=['email'],
        client_id=constants.CLIENT_ID,
        user_id=123)

    old_token.put()

    request = mock.MagicMock()
    request.client = self.client
    request.user = oauth_models.OAuthUser(id=123)

    token_properties = {'access_token': 'access_token_2',
                        'refresh_token': 'refresh_token_2',
                        'token_type': 'Bearer',
                        'expires_in': 3600,
                        'scope': 'email'}

    # Exercise.
    loaded_token = oauth_api.save_token(token_properties, request)

    # Verify
    user_tokens = oauth_models.Token.find_all_by_client_user_id(constants.CLIENT_ID, 123)
    self.assertEqual(1, len(user_tokens))
    self.assertEqual(loaded_token.key, user_tokens[0].key)

  def test_get_user_returns_existing_user(self):
    # Setup.
    user = user_models.User.create('my@test.com', 'qwerty')
    user.put()

    request = mock.MagicMock()

    # Exercise.
    loaded_user = oauth_api.get_user('my@test.com', 'qwerty', self.client, request)

    # Verify
    self.assertTrue(isinstance(loaded_user, oauth_models.OAuthUser))
    self.assertEqual(loaded_user.id, user.key.id())

  def test_get_user_returns_none_if_no_client(self):
    # Setup.
    user = user_models.User.create('my@test.com', 'qwerty')
    user.put()

    request = mock.MagicMock()
    # Exercise.
    loaded_user = oauth_api.get_user('my@test.com', 'qwerty', None, request)

    # Verify
    self.assertEqual(None, loaded_user)

  def test_get_user_returns_none_if_incorrect_password(self):
    # Setup.
    user = user_models.User.create('my@test.com', 'qwerty')
    user.put()

    request = mock.MagicMock()

    # Exercise.
    loaded_user = oauth_api.get_user('my@test.com', 'xyz', self.client, request)

    # Verify
    self.assertEqual(None, loaded_user)

  def test_token_handler_creates_token(self):
    # Setup.
    headers = test_utils.create_basic_auth_headers()
    user = user_models.User.create('my@test.com', 'qwerty')
    user.put()

    grant_request_data = {'grant_type': 'password',
                          'username': 'my@test.com',
                          'password': 'qwerty',
                          'client_id': constants.CLIENT_ID}

    # Exercise.
    response = self.app.post('/oauth/token',
                             data=grant_request_data,
                             headers=headers)

    # Verify
    self.assertEqual(200, response.status_code)
    token_data = json.loads(response.data)
    self.assertTrue(token_data['access_token'])

if __name__ == "__main__":
  unittest.main()
