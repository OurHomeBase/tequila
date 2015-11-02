'''A test for oauth api workflows'''

import unittest
import requests
import time
import base64
import json

from utils import constants

class OAuthApiTest(unittest.TestCase):
  
  def setUp(self):
    self._CreateClient()
    self.waitToCache()

    self._CreateUser()
    self.waitToCache()
    
  def waitToCache(self):  
    # NDB needs time to store data in Cache. 
    time.sleep(0.1)
  
  def _CreateClient(self):
    client_request = requests.get("http://localhost:8080/api/client/create", 
                                  headers=self._CreateBasicAuthHeaders())
    self.assertEqual(200, client_request.status_code)    
    self.assertEqual(constants.CLIENT_ID, client_request.json()['client_id'])
  
  def _CreateUser(self):
    headers = self._CreateBasicAuthHeaders()
    headers['Content-Type'] = 'application/json'
    user_request = requests.post("http://localhost:8080/api/user/", 
                                  headers=headers,
                                  data=json.dumps({'username': 'sss'}))
    
    self.assertEqual(200, user_request.status_code)    
    self.assertEqual('sss', user_request.json()['username'])
  
  def _CreateBasicAuthHeaders(self):
    client_id_secret = '{}:{}'.format(constants.CLIENT_ID, 
                                      constants.CLIENT_SECRET)  
    
    return {'Authorization': 'Basic {}'.format(base64.b64encode(client_id_secret))}

  def testGetAccessTokenReturnsCorrectToken(self):
    # Setup.
    grant_request_data = {'grant_type': 'password',
                          'username': 'sss',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}
    
    # Execute.
    token_request = requests.post("http://localhost:8080/oauth/token", 
                                  data = grant_request_data,
                                  headers=self._CreateBasicAuthHeaders())
    
    token_data = token_request.json() 
    
    # Verify.
    self.assertTrue(token_data)
    self.assertTrue(token_data['access_token'])

  def testGetAccessTokenDeniesIfBasicAuthFails(self):
    client_id_secret = '{}:{}'.format(constants.CLIENT_ID, 'some passwors')  
    
    headers = {'Authorization': 'Basic {}'.format(base64.b64encode(client_id_secret))}
    
    # Setup.
    grant_request_data = {'grant_type': 'password',
                          'username': 'sss',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}
    
    # Execute.
    token_request = requests.post("http://localhost:8080/oauth/token", 
                                  data = grant_request_data,
                                  headers=headers)
    
    # Verify.
    self.assertEqual(401, token_request.status_code)

  def testAccessProtectedApiReturnsCorrectDataWhenAuthorized(self):
    # Setup.
    grant_request_data = {'grant_type': 'password',
                          'username': 'sss',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}
    
    token_request = requests.post("http://localhost:8080/oauth/token", 
                                  data = grant_request_data,
                                  headers=self._CreateBasicAuthHeaders())

    access_token = token_request.json()['access_token']
    
    # Need to wait before using the token to make sure it is saved in cache. 
    self.waitToCache()
     
    # Execute.
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    user_me_request = requests.get('http://localhost:8080/api/user/me', headers=headers)
    user_me_data = user_me_request.json()
    
    # Verify.
    self.assertTrue(user_me_data)
    self.assertEqual('sss', user_me_data['username'])

if __name__ == '__main__':
  unittest.main()
  