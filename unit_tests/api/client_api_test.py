'''Unit tests for client_api.'''

import unittest

from utils import constants
from unit_tests import common_test
from persistence import oauth_models
from api import client_api
import json


# pylint: disable=missing-docstring
class ClientApiTest(common_test.CommonNdbTest):
  '''A class to test client_api model.'''

  def setUp(self):
    common_test.CommonNdbTest.setUp(self)
    self.app = common_test.create_test_client(client_api)

  def test_create_client_creates_if_not_exists(self):
    # Exercise.
    response = self.app.get('/api/client/create')

    # Verify
    client_json = json.loads(response.data)
    self.assertEqual(constants.CLIENT_ID, client_json['client_id'])

  def test_create_client_reads_if_exists(self):
    # Setup.
    client = oauth_models.Client(client_id=constants.CLIENT_ID,
                                 client_secret=constants.CLIENT_SECRET)
    client.put()

    # Exercise.
    response = self.app.get('/api/client/create')

    # Verify
    client_json = json.loads(response.data)
    clients_with_client_id = oauth_models.Client.query(
        oauth_models.Client.client_id == constants.CLIENT_ID).fetch()

    self.assertEqual(constants.CLIENT_ID, client_json['client_id'])
    self.assertEqual(1, len(clients_with_client_id))
    self.assertEqual(client.key, clients_with_client_id[0].key)

if __name__ == "__main__":
  unittest.main()
