'''A module to run unit tests.'''

import unittest

def _run_tests():
  test_suite = unittest.TestLoader().discover(
      start_dir='unit_tests', pattern='*_test.py', top_level_dir='.')

  unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == "__main__":
  _run_tests()
