'''A module to store data models.'''

from google.appengine.ext import ndb
from google.appengine.api import datastore_errors

class TimeProfile(ndb.Model):
  def weeklyValidation(self, value):
    if not value <= 7*24:
      raise datastore_errors.BadValueError('expect value <= 168, got %s.' % repr(value))

  def dailyValidation(self, value):
    if not value <= 24:
      raise datastore_errors.BadValueError('expect value <= 24, got %s.' % repr(value))
    
  hasChildren = ndb.BooleanProperty()
  workStatus = ndb.StringProperty(choices=['Full Time', 'Part Time', 'None'])
  workHrs = ndb.FloatProperty(validator=weeklyValidation)
  commuteHrs = ndb.FloatProperty(validator=dailyValidation)
  daysCommuting = ndb.IntegerProperty()
  sleepHrs = ndb.FloatProperty(validator=dailyValidation)
  personalHrs = ndb.FloatProperty(validator=dailyValidation)
  bondingHrs = ndb.FloatProperty(validator=weeklyValidation)
  choreHrs = ndb.FloatProperty(validator=weeklyValidation)

class Address(ndb.Model):
  type = ndb.StringProperty() # E.g., 'home', 'work'
  street = ndb.StringProperty()
  city = ndb.StringProperty()
  country = ndb.StringProperty()
  zip = ndb.StringProperty()
  
class NotifPreference(ndb.Model):
  type = ndb.StringProperty() # E.g., 'high5', 'comment'
  push = ndb.BooleanProperty()
  frequency = ndb.StringProperty()

class User(ndb.Model):
  _ADDR_DEFAULT_TYPE = 'home'
  
  #id = ndb.IntegerProperty()
  username = ndb.StringProperty()
  email = ndb.StringProperty()
  emailVerified = ndb.BooleanProperty()
  name = ndb.StringProperty()
  
  #addresses = ndb.StructuredProperty(Address, repeated=True)
  addresses = ndb.PickleProperty()
  notificationPrefs = ndb.StructuredProperty(Notification, repeated=True)
  timeProfile = ndb.StructuredProperty(TimeProfile)

  lastLogin = ndb.DateTimeProperty()
  accountStatus = ndb.IntegerProperty(choices=[1, 2], default=1) #1=active, 2=locked
  
  @property
  def id(self):
    if self.key:
      return self.key.id()
    else:
      return None
        
  @classmethod
  def findById(cls, id):
    return User.query(User.key == ndb.Key(User, id)).fetch(1)[0]  
                                 
  @classmethod
  def findByUsername(cls, username):
    list_users = User.query(User.username == username).fetch(1)
     
    return list_users[0] if list_users else None  

  @classmethod
  def findByEmail(cls, email):
    list_users = User.query(User.email == email).fetch(1)
     
    return list_users[0] if list_users else None 
  
  '''def findAddressByType(self, addrType):
    for addr in self.addresses:
      if addr.type == addrType : 
        return addr
    return None   
  ''' 
  def findAddressByType(self, addrType):
    if self.addresses:
      return self.addresses[addrType]
    else:
      return None   

  

    
  