'''A test for oauth api workflows'''

import unittest
import requests

class OAuthApiTest(unittest.TestCase):

  def testGetAccessTokenAndAccessProtectedAPI(self):
    r = requests.get('http://localhost:8080/api/user/she')
    
    print r.text 

if __name__ == '__main__':
  unittest.main()