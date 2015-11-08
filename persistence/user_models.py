'''A module to store data models.'''

from google.appengine.ext import ndb


class User(ndb.Model):
  '''Stores basic user properties.'''
  username = ndb.StringProperty()

  @classmethod
  def find_by_id(cls, key_id):
    return User.query(User.key == ndb.Key(User, key_id)).fetch(1)[0]

  @classmethod
  def find_by_username(cls, username):
    list_users = User.query(User.username == username).fetch(1)

    return list_users[0] if list_users else None

