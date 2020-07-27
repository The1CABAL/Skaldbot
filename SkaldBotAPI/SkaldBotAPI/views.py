"""
Routes and views for the flask application.
"""
from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
from SkaldBotAPI import app
from Resource.Forms import *
from Resource.Users import *
from Resource.Roles import *
from Resource.Items import *
from Resource.GenerateFernetKey import GenerateFernetKey

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api.add_resource(GetForms, '/getForms')
api.add_resource(GetFormsByPageId, '/getFormByPageId')
api.add_resource(GetFormSchema, '/getFormSchema')
api.add_resource(GetActionLink, '/getActionLink')
api.add_resource(GetFormName, '/getFormName')
api.add_resource(SubmitItem, '/submititem')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(GenerateFernetKey, '/generatefernetkey')
api.add_resource(GetUserRoles, '/roles')
api.add_resource(GetAllUsers, '/getUsers')
api.add_resource(GetUserForProfile, '/getUser')
api.add_resource(GetAllRoles, '/getRoles')
api.add_resource(ManageSubmittedItems, '/submittedItems')
api.add_resource(Stories, '/getStories')
api.add_resource(Story, '/story')
api.add_resource(Wisdoms, '/getWisdoms')
api.add_resource(Wisdom, '/wisdom')