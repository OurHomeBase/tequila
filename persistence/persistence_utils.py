'''A model to keep common persistence functions.'''


def fetch_first_or_none(ndb_query):
  '''Returns first entity returned by the ndb_query or None.

  Args:
    ndb_query: an ndb query object. In example:
      oauth_models.Token.query(oauth_models.Token.user_id == 123)

  Returns: a first entity or None.
  '''
  entities = ndb_query.fetch(1)

  return entities[0] if entities else None
