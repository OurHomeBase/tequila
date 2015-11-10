'''Unit tests for oauth_models.'''

import unittest

from unit_tests import common_test
from persistence import oauth_models


# pylint: disable=missing-docstring
class OAuthUserTest(common_test.CommonNdbTest):
  '''A class to test OAuthUser NDB model.'''

  def test_create_oauth_user(self):
    # Exercise.
    created_user = oauth_models.OAuthUser(id=1)
    created_user.put()

    # Verify
    self.assertTrue(created_user.key)


class ClientTest(common_test.CommonNdbTest):
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
    self.assertEqual(('unsupported', ), redirect_uris)

  def test_default_scopes_is_email(self):
    # Setup.
    client = oauth_models.Client(client_id='some_id', client_secret='some secret')

    # Exercise.
    default_scopes = client.default_scopes

    # Verify.
    self.assertEqual(('email', ), default_scopes)

  def test_find_by_client_id_returns_expected_client(self):
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


class GrantTest(common_test.CommonNdbTest):
  '''A class to test Grant NDB model.'''

  def test_find_by_client_id_and_code_returns_expected(self):
    # Setup.
    created_grant = oauth_models.Grant(client_id='some_id', code='xyz')
    created_grant.put()

    # Exercise.
    found_grant = oauth_models.Grant.find_by_client_id_and_code('some_id', 'xyz')

    # Verify
    self.assertTrue(found_grant)
    self.assertEqual(created_grant.key, found_grant.key)

  def test_delete_removes_grant(self):
    # Setup.
    created_grant = oauth_models.Grant(client_id='some_id', code='xyz')
    created_grant.put()
    created_grant.delete()

    # Exercise.
    found_grant = oauth_models.Grant.find_by_client_id_and_code('some_id', 'xyz')

    # Verify
    self.assertFalse(found_grant)


class TokenTest(common_test.CommonNdbTest):
  '''A class to test Token NDB model.'''

  def test_find_all_by_client_user_id_returns_expected(self):
    # Setup.
    token1 = oauth_models.Token(client_id='c_id', user_id=123, access_token='ABC')
    token1.put()
    token2 = oauth_models.Token(client_id='c_id', user_id=123, access_token='DEF')
    token2.put()

    # Exercise.
    list_tokens = oauth_models.Token.find_all_by_client_user_id('c_id', 123)

    # Verify
    self.assertTrue(list_tokens)
    self.assertEqual(2, len(list_tokens))

  def test_find_by_access_code_returns_expected(self):
    # Setup.
    created_token = oauth_models.Token(
        client_id='c_id', user_id=123, access_token='XYZ')

    created_token.put()

    # Exercise.
    found_token = oauth_models.Token.find_by_access_code('XYZ')

    # Verify
    self.assertTrue(found_token)
    self.assertEqual(created_token.key, found_token.key)

  def test_find_by_refresh_token_returns_expected(self):
    # Setup.
    created_token = oauth_models.Token(
        client_id='c_id', user_id=123, refresh_token='XYZ')

    created_token.put()

    # Exercise.
    found_token = oauth_models.Token.find_by_refresh_code('XYZ')

    # Verify
    self.assertTrue(found_token)
    self.assertEqual(created_token.key, found_token.key)

if __name__ == "__main__":
  unittest.main()
