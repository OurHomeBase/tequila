'''Unit tests for oauth_models.'''

import unittest

from unit_tests.persistence import ndb_common_test
from persistence import oauth_models


# pylint: disable=missing-docstring
class OAuthUserTest(ndb_common_test.CommonNdbTest):
  '''A class to test OAuthUser NDB model.'''

  def test_create_oauth_user(self):
    # Exercise.
    created_user = oauth_models.OAuthUser(id=1)
    created_user.put()

    # Verify
    self.assertTrue(created_user.key)


class ClientTest(ndb_common_test.CommonNdbTest):
  '''A class to test Client NDB model.'''

  def test_client_type_confidential(self):
    # Setup.
    client = oauth_models.Client(client_id='some id', client_secret='some secret')

    # Exercise.
    client_type = client.client_type

    # Verify
    self.assertEqual('confidential', client_type)

if __name__ == "__main__":
  unittest.main()
