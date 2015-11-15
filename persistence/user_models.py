'''A module to store data models.'''

from google.appengine.ext import ndb
from persistence import persistence_utils


class User(ndb.Model):
  '''Stores basic user properties.'''
  username = ndb.StringProperty()

  @classmethod
  def find_by_id(cls, key_id):
    query = User.query(User.key == ndb.Key(User, key_id))

    return persistence_utils.fetch_first_or_none(query)

  @classmethod
  def find_by_username(cls, username):
    query = User.query(User.username == username)

    return persistence_utils.fetch_first_or_none(query)

