'''The module stores user_models for authentication and authorization.'''
from google.appengine.ext import ndb

# pylint: disable=too-few-public-methods
class OAuthUser(ndb.Model):
  '''A class to represent OAuth User.'''
  id = ndb.IntegerProperty() # pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

class Client(ndb.Model):
  '''Class to represent OAuth Client. It is typically one per platform.'''

  client_id = ndb.StringProperty()
  client_secret = ndb.StringProperty()

  @property
  def client_type(self):
    return 'confidential'

  @property
  def default_redirect_uri(self):
    return 'unsupported'

  @property
  def redirect_uris(self):
    return [self.default_redirect_uri]

  @property
  def default_scopes(self):
    return ['email']

  @classmethod
  def find_by_client_id(cls, client_id):
    client_list = Client.query(Client.client_id == client_id).fetch(1)

    return client_list[0] if client_list else None


class Grant(ndb.Model):
  '''Class to store OAuth Grant.'''
  id = ndb.IntegerProperty() # pylint: disable=invalid-name

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
  def find_by_client_id_and_code(cls, client_id, code):
    return Grant.query(Grant.client_id == client_id, Grant.code == code).fetch(1)[0]


class Token(ndb.Model):
  '''Class to store OAuth Access and Refresh Tokens'''
  id = ndb.IntegerProperty() # pylint: disable=invalid-name
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
  def find_all_by_client_user_id(cls, client_id, user_id):
    return Token.query(Token.client_id == client_id, Token.user_id == user_id).fetch()

  @classmethod
  def find_by_access_code(cls, access_token):
    return Token.query(Token.access_token == access_token).fetch(1)[0]

  @classmethod
  def find_by_refresh_code(cls, refresh_token):
    return Token.query(Token.refresh_token == refresh_token).fetch(1)[0]
