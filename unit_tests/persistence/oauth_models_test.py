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
    client = oauth_models.Client(client_id='some_id', client_secret='some secret')

    # Exercise.
    client_type = client.client_type

    # Verify
    self.assertEqual('confidential', client_type)

  def test_redirect_uris_is_empty_list(self):
    # Setup.
    client = oauth_models.Client(client_id='some_id', client_secret='some secret')

    # Exercise.
    redirect_uris = client.redirect_uris

    # Verify
    self.assertListEqual(['unsupported'], redirect_uris)

  def test_find_by_client_id_returns_expected_client_if_exists(self):
    # Setup.
    created_client = oauth_models.Client(client_id='some_id', client_secret='some secret')
    created_client.put()

    # Exercise.
    found_client = oauth_models.Client.find_by_client_id('some_id')

    # Verify
    self.assertTrue(found_client)
    self.assertEqual(created_client.key, found_client.key)

  def test_find_by_client_id_returns_none_if_not_exists(self):
    # Exercise.
    found_client = oauth_models.Client.find_by_client_id('unknown_id')

    # Verify
    self.assertFalse(found_client)


if __name__ == "__main__":
  unittest.main()
