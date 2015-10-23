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
                                                                 


class Client(ndb.Model):
    client_id = ndb.StringProperty()
    client_secret = ndb.StringProperty()

    user_id = ndb.IntegerProperty()
    user = ndb.StructuredProperty(User)

    p_redirect_uris = ndb.StringProperty()
    p_defaultscopes = ndb.StringProperty()

    @property
    def client_type(self):
        return 'public'

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


class Grant(ndb.Model):
    id = ndb.IntegerProperty()

    user_id = ndb.IntegerProperty()
    user = ndb.StructuredProperty(User)

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


class Token(ndb.Model):
    id = ndb.IntegerProperty()
    client_id = ndb.StringProperty()
    client = ndb.StructuredProperty(Client)

    user_id = ndb.IntegerProperty()
    user = ndb.StructuredProperty(User)

    # currently only bearer is supported
    token_type = ndb.StringProperty()

    access_token = ndb.StringProperty()
    refresh_token = ndb.StringProperty()
    expires = ndb.DateTimeProperty()

    p_scopes = ndb.StringProperty()

    @property
    def p_user(self):
        return self.user
        
    @property
    def scopes(self):
        if self.p_scopes:
            return self.p_scopes.split()
        return []