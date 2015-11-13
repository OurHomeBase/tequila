'''Unit tests for persistence_utils.'''

import unittest
from persistence import persistence_utils
from persistence import oauth_models

from unit_tests.common import common_test

# pylint: disable=missing-docstring
class PersistenceUtilsTest(common_test.CommonNdbTest):
  '''Tests for persistence utils. '''

  def test_fetch_first_or_none_returns_first_if_exists(self):
    # Setup.
    token1 = oauth_models.Token(user_id=123)
    token1.put()

    query = oauth_models.Token.query(oauth_models.Token.user_id == 123)

    # Exercise.
    found_token = persistence_utils.fetch_first_or_none(query)

    # Verify.
    self.assertTrue(found_token)
    self.assertEqual(token1.key, found_token.key)

  def test_fetch_first_or_none_returns_none_if_not_exists(self):
    # Setup.
    query = oauth_models.Token.query(oauth_models.Token.user_id == 123)

    # Exercise.
    found_token = persistence_utils.fetch_first_or_none(query)

    # Verify.
    self.assertFalse(found_token)


if __name__ == "__main__":
  unittest.main()
