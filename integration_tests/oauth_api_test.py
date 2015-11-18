'''A test for oauth api workflows'''

import unittest
import requests
import time
import base64
import json

from utils import constants
from unit_tests.common import test_utils

# pylint: disable=missing-docstring
def _wait_caching():
  # NDB needs time to store data in Cache.
  time.sleep(0.1)

class OAuthApiTest(unittest.TestCase):

  def setUp(self):
    self._create_client()
    _wait_caching()

    self._create_user()
    _wait_caching()

  def _create_client(self):
    client_request = requests.get("http://localhost:8080/api/client/create",
                                  headers=test_utils.create_basic_auth_headers())
    self.assertEqual(200, client_request.status_code)
    self.assertEqual(constants.CLIENT_ID, client_request.json()['client_id'])

  def _create_user(self):
    headers = test_utils.create_basic_auth_headers()
    headers['Content-Type'] = 'application/json'
    user_request = requests.post("http://localhost:8080/api/user/",
                                 headers=headers,
                                 data=json.dumps({'email': 'my@test.com'}))

    self.assertEqual(200, user_request.status_code)
    self.assertEqual('my@test.com', user_request.json()['email'])

  def test_get_access_token_returns_correct_token(self):
    # Setup.
    grant_request_data = {'grant_type': 'password',
                          'username': 'my@test.com',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}

    # Execute.
    token_request = requests.post("http://localhost:8080/oauth/token",
                                  data=grant_request_data,
                                  headers=test_utils.create_basic_auth_headers())

    token_data = token_request.json()

    # Verify.
    self.assertTrue(token_data)
    self.assertTrue(token_data['access_token'])

  def test_get_access_token_denies_if_basic_auth_fails(self):
    client_id_secret = '{}:{}'.format(constants.CLIENT_ID, 'some password')

    headers = {'Authorization': 'Basic {}'.format(base64.b64encode(client_id_secret))}

    # Setup.
    grant_request_data = {'grant_type': 'password',
                          'username': 'my@test.com',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}

    # Execute.
    token_request = requests.post("http://localhost:8080/oauth/token",
                                  data=grant_request_data,
                                  headers=headers)

    # Verify.
    self.assertEqual(401, token_request.status_code)

  def test_access_protected_api_returns_correct_data_when_authorized(self):
    # Setup.
    grant_request_data = {'grant_type': 'password',
                          'username': 'my@test.com',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}

    token_request = requests.post("http://localhost:8080/oauth/token",
                                  data=grant_request_data,
                                  headers=test_utils.create_basic_auth_headers())

    access_token = token_request.json()['access_token']

    # Need to wait before using the token to make sure it is saved in cache.
    _wait_caching()

    # Execute.
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    user_me_request = requests.get('http://localhost:8080/api/user/me', headers=headers)
    user_me_data = user_me_request.json()

    # Verify.
    self.assertTrue(user_me_data)
    self.assertEqual('my@test.com', user_me_data['email'])

if __name__ == '__main__':
  unittest.main()
