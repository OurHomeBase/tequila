'''A test for oauth api workflows'''

import unittest
import requests
import time
import base64

from utils import constants

class OAuthApiTest(unittest.TestCase):

  def testGetAccessTokenReturnsCorrectToken(self):
    # Setup.
    client_id_secret = '{}:{}'.format(constants.CLIENT_ID, 
                                      constants.CLIENT_SECRET)  
    
    headers = {'Authorization': 'Basic {}'.format(base64.b64encode(client_id_secret))}
    grant_request_data = {'grant_type': 'password',
                          'username': 'sss',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}
    
    # Execute.
    token_request = requests.post("http://localhost:8080/oauth/token", 
                                  data = grant_request_data,
                                  headers=headers)
    
    token_data = token_request.json() 
    
    # Verify.
    self.assertTrue(token_data)
    self.assertTrue(token_data['access_token'])

  def testGetAccessTokenDeniesIfBasicAuthFails(self):
    # Setup.
    client_id_secret = '{}:{}'.format(constants.CLIENT_ID, 
                                      'wrong password')  
    
    headers = {'Authorization': 'Basic {}'.format(base64.b64encode(client_id_secret))}
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
    client_id_secret = '{}:{}'.format(constants.CLIENT_ID, 
                                      constants.CLIENT_SECRET)  
    
    headers = {'Authorization': 'Basic {}'.format(base64.b64encode(client_id_secret))}
    grant_request_data = {'grant_type': 'password',
                          'username': 'sss',
                          'password': 'A3ddj3w',
                          'client_id': constants.CLIENT_ID}
    
    token_request = requests.post("http://localhost:8080/oauth/token", 
                                  data = grant_request_data,
                                  headers=headers)

    access_token = token_request.json()['access_token']
    
    # Need to wait before using the token to make sure it is saved in cache. 
    time.sleep(1)
     
    # Execute.
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    user_me_request = requests.get('http://localhost:8080/api/user/me', headers=headers)
    user_me_data = user_me_request.json()
    
    # Verify.
    self.assertTrue(user_me_data)
    self.assertEqual('sss', user_me_data['username'])

if __name__ == '__main__':
  unittest.main()
  