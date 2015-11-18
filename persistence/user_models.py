'''A module to store data models.'''

from google.appengine.ext import ndb
from persistence import persistence_utils
from google.appengine.api import datastore_errors

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


_ADDR_DEFAULT_TYPE = 'home'
_ACCOUNT_STATUS_CHOICES = [1, 2] #1=active, 2=locked
_WORK_STATUS_CHOICES = ['Full Time', 'Part Time', 'None']

class TimeProfile(ndb.Model):
  '''Stores user defined time profile information.'''
  def week_validator(self, value):
    if not value <= 7*24:
      raise datastore_errors.BadValueError('expect value <= 168, got %s.' % repr(value))

  hasChildren = ndb.BooleanProperty()
  workStatus = ndb.StringProperty(choices=_WORK_STATUS_CHOICES)
  choreHrs = ndb.FloatProperty(validator=week_validator)

class Address(ndb.Model):
  '''Stores user's address'''
  addr_type = ndb.StringProperty(default=_ADDR_DEFAULT_TYPE)
  street = ndb.StringProperty()
  city = ndb.StringProperty()
  country = ndb.StringProperty()
  zip = ndb.StringProperty()

class User(ndb.Model):
  '''Stores basic user properties.'''
  username = ndb.StringProperty()
  password_hash = ndb.StringProperty()
  
  email = ndb.StringProperty()
  emailVerified = ndb.BooleanProperty()
  name = ndb.StringProperty()

  time_profile = ndb.StructuredProperty(TimeProfile)
  addresses = ndb.StructuredProperty(Address, repeated=True)

  lastLogin = ndb.DateTimeProperty()
  accountStatus = ndb.IntegerProperty(choices=_ACCOUNT_STATUS_CHOICES, default=1)

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

  @classmethod
  def find_by_email(cls, email):
    list_users = User.query(User.email == email).fetch(1)

    return list_users[0] if list_users else None

  def find_address_by_type(self, addr_type=_ADDR_DEFAULT_TYPE):
    for addr in self.addresses:
      if addr.addr_type == addr_type:
        return addr
    return None

