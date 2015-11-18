'''Unit tests for user_models.'''

import unittest

from persistence import user_models
from unit_tests.common import test_utils
from google.appengine.api import datastore_errors

# pylint: disable=missing-docstring
class UserTest(test_utils.CommonNdbTest):
  '''A class to test User NDB model.'''

  def test_find_by_id_returns_expected_user(self):
    # Setup.
    created_user = user_models.User(email='my@test.com')
    created_user.put()

    # Exercise.
    found_user = user_models.User.find_by_id(created_user.key.id())

    # Verify
    self.assertTrue(found_user)
    self.assertEqual('my@test.com', found_user.email)

  def test_create_user_check_hash_saved(self):
    # Exercise.
    created_user = user_models.User.create(email='my@test.com',
                                           password='my_pass')
    created_user.put()

    # Verify
    user = user_models.User.find_by_email('my@test.com')
    password_hash = user.password_hash
    self.assertTrue(password_hash)
    self.assertTrue(user.check_password('my_pass'))

  def test_find_by_email_returns_expected_user(self):
    # Setup.
    created_user = user_models.User(email='my_user@gmail.com')
    created_user.put()

    # Exercise.
    found_user = user_models.User.find_by_email('my_user@gmail.com')

    # Verify
    self.assertTrue(found_user)
    self.assertEqual('my_user@gmail.com', found_user.email)

  def test_find_address_by_type_returns_expected_address(self):
    # Setup.
    created_user_no_address = user_models.User(email='no_address@gmail.com')
    created_user_no_address.put()

    created_user_one_address = user_models.User(email='one_address@gmail.com')
    created_user_one_address.addresses = [user_models.Address(city='San Jose')]
    created_user_one_address.put()

    created_user_multi_addresses = user_models.User(email='multi_addresses@gmail.com')
    addr1 = user_models.Address(addr_type='work', city='Amsterdam')
    addr2 = user_models.Address(addr_type='home', city='Campbell')
    created_user_multi_addresses.addresses = [addr1, addr2]
    created_user_multi_addresses.put()

    # Exercise.
    found_user_no_addr = user_models.User.find_by_email('no_address@gmail.com')
    found_user_one_addr = user_models.User.find_by_email('one_address@gmail.com')
    found_user_multi_addr = user_models.User.find_by_email('multi_addresses@gmail.com')

    # Verify
    self.assertTrue(found_user_no_addr)
    self.assertIsNone(found_user_no_addr.find_address_by_type())

    self.assertTrue(found_user_one_addr)
    self.assertEqual('San Jose', found_user_one_addr.find_address_by_type().city)

    self.assertTrue(found_user_multi_addr)
    self.assertEqual('Amsterdam', found_user_multi_addr.find_address_by_type('work').city)
    self.assertEqual('Campbell', found_user_multi_addr.find_address_by_type('home').city)

  def test_time_profile_validations_and_defaults(self):
    # Setup.
    # Exercise.
    user_models.TimeProfile(hasChildren=True, workStatus='Full Time', choreHrs=20)

    # Verify
    with self.assertRaises(datastore_errors.BadValueError):
      user_models.TimeProfile(hasChildren=True, workStatus='nonsense', choreHrs=20)

    with self.assertRaises(datastore_errors.BadValueError):
      user_models.TimeProfile(hasChildren=True, workStatus='Full Time', choreHrs=170)

if __name__ == "__main__":
  unittest.main()
