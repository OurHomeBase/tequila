'''A module to store data models.'''

from google.appengine.ext import ndb
from persistence import persistence_utils

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



class User(ndb.Model):
  '''Stores basic user properties.'''
  username = ndb.StringProperty()
  password_hash = ndb.StringProperty()
  
  @classmethod
  def create(cls, username, password):
    password_hash = generate_password_hash(password)
    
    return cls(username=username, password_hash=password_hash)
  
  def check_password(self, password):
    return check_password_hash(str(self.password_hash), password)    

  @classmethod
  def find_by_id(cls, key_id):
    query = User.query(User.key == ndb.Key(User, key_id))

    return persistence_utils.fetch_first_or_none(query)

  @classmethod
  def find_by_username(cls, username):
    query = User.query(User.username == username)

    return persistence_utils.fetch_first_or_none(query)

