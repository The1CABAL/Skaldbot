import collections

Suggestion = collections.namedtuple('suggestion', ['typeId', 'title', 'story', 'email'])
User = collections.namedtuple('user', ['username', 'password'])