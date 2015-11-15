'''Unit tests for user_models.'''

import unittest

from persistence import user_models
from unit_tests.common import test_utils

# pylint: disable=missing-docstring
class UserTest(test_utils.CommonNdbTest):
  '''A class to test User NDB model.'''

  def test_find_by_username_returns_expected_user(self):
    # Setup.
    created_user = user_models.User(username='my_user')
    created_user.put()

    # Exercise.
    found_user = user_models.User.find_by_username('my_user')

    # Verify
    self.assertTrue(found_user)
    self.assertEqual(created_user.key, found_user.key)

  def test_find_by_id_returns_expected_user(self):
    # Setup.
    created_user = user_models.User(username='my_user')
    created_user.put()

    # Exercise.
    found_user = user_models.User.find_by_id(created_user.key.id())

    # Verify
    self.assertTrue(found_user)
    self.assertEqual('my_user', found_user.username)

if __name__ == "__main__":
  unittest.main()
