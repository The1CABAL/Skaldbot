import collections

Suggestion = collections.namedtuple('suggestion', ['typeId', 'title', 'story', 'email'])
User = collections.namedtuple('user', ['username', 'password'])
RegisterUser = collections.namedtuple('registeruser', ['username', 'firstname', 'lastname', 'password'])
UserProfile = collections.namedtuple('userprofile', ['username', 'firstname', 'lastname', 'isactive', 'islocked', 'role'])
StoryModel = collections.namedtuple('story', ['id', 'title', 'story', 'isactive'])
WisdomModel = collections.namedtuple('wisdom', ['id', 'title', 'wisdom', 'isactive'])
FormModel = collections.namedtuple('formmodel', ['formkey', 'fieldschema', 'actionlink', 'isactive', 'formname'])