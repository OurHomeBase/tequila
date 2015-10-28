'''The module stores user_models for authentication and authorization.'''
from google.appengine.ext import ndb

class OAuthUser(ndb.Model):
  id = ndb.IntegerProperty()


class Client(ndb.Model):
  client_id = ndb.StringProperty()
  client_secret = ndb.StringProperty()
  
  p_redirect_uris = ndb.StringProperty()
  p_defaultscopes = ndb.StringProperty()

  @property
  def client_type(self):
    return 'confidential'

  @property
  def redirect_uris(self):
    if self.p_redirect_uris:
      return self.p_redirect_uris.split()
    return []

  @property
  def default_redirect_uri(self):
    return self.p_redirect_uris[0]

  @property
  def default_scopes(self):
    if self.p_defaultscopes:
      return self.p_defaultscopes.split()
    return []

  @classmethod
  def findByClientId(cls, client_id):
    client_list = Client.query(Client.client_id == client_id).fetch(1)
    if client_list:
      return client_list[0]
    else:
      return None  
                                 

class Grant(ndb.Model):
  id = ndb.IntegerProperty()

  user_id = ndb.IntegerProperty()
  user = ndb.StructuredProperty(OAuthUser)

  client_id = ndb.StringProperty()
  client = ndb.StructuredProperty(Client)

  code = ndb.StringProperty()

  redirect_uri = ndb.StringProperty()
  expires = ndb.DateTimeProperty()

  p_scopes = ndb.StringProperty()

  def delete(self):
    self.key.delete()
    return self

  @property
  def scopes(self):
    if self.p_scopes:
      return self.p_scopes.split()
    return []
  
  @classmethod
  def findByClientIdAndCode(cls, client_id, code):
    return Grant.query(Grant.client_id == client_id, Grant.code==code).fetch(1)[0]


class Token(ndb.Model):
  id = ndb.IntegerProperty()
  client_id = ndb.StringProperty()
  client = ndb.StructuredProperty(Client)

  user_id = ndb.IntegerProperty()
  user = ndb.StructuredProperty(OAuthUser)

  # currently only bearer is supported
  token_type = ndb.StringProperty()

  access_token = ndb.StringProperty()
  refresh_token = ndb.StringProperty()
  expires = ndb.DateTimeProperty()

  p_scopes = ndb.StringProperty()

  @property
  def scopes(self):
    if self.p_scopes:
      return self.p_scopes.split()
    return []
  
  @classmethod
  def findAllByClientIdAndUserId(cls, client_id, user_id):
    return Token.query(Token.client_id==client_id, Token.user_id==user_id).fetch()
  
  @classmethod
  def findByAccessCode(cls, access_token):
    return Token.query(Token.access_token == access_token).fetch(1)[0]
  
  @classmethod
  def findByRefreshCode(cls, refresh_token):
    return Token.query(Token.refresh_token == refresh_token).fetch(1)[0]
  