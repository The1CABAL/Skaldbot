import collections

Suggestion = collections.namedtuple('suggestion', ['typeId', 'title', 'story', 'serverid', 'email'])
User = collections.namedtuple('user', ['username', 'password'])
RegisterUser = collections.namedtuple('registeruser', ['accountname', 'username', 'firstname', 'lastname', 'discorduserid', 'password'])
RegisterAccountUser = collections.namedtuple('registeraccountuser', ['accountid', 'username', 'firstname', 'lastname', 'discorduserid', 'password'])
UserProfile = collections.namedtuple('userprofile', ['username', 'firstname', 'lastname', 'discorduserid', 'isactive', 'islocked', 'role'])
StoryModel = collections.namedtuple('story', ['id', 'title', 'story', 'serverid', 'isactive'])
WisdomModel = collections.namedtuple('wisdom', ['id', 'title', 'wisdom', 'serverid', 'isactive'])
FormModel = collections.namedtuple('formmodel', ['formkey', 'fieldschema', 'actionlink', 'isactive', 'formname'])
AccountProfile = collections.namedtuple('accountprofile', ['accountid', 'accountname', 'createdate', 'isactive'])
Documentation = collections.namedtuple('documentation', ['helpcontentkey', 'helptitle', 'helpcontent', 'isactive', 'updatebyuserid', 'isadmin'])