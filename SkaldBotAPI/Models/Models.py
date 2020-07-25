import collections

Suggestion = collections.namedtuple('suggestion', ['typeId', 'title', 'story', 'email'])
User = collections.namedtuple('user', ['username', 'firstname', 'lastname', 'password'])
UserProfile = collections.namedtuple('userprofile', ['username', 'firstname', 'lastname', 'isactive', 'islocked', 'role'])