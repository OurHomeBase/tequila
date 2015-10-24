'''A module to store data models.'''

from google.appengine.ext import ndb


class User(ndb.Model):
    #id = ndb.IntegerProperty()
    username = ndb.StringProperty()
    
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
        return User.query(User.username == username).fetch(1)[0]    

    