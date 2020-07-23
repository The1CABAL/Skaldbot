"""
Routes and views for the flask application.
"""
from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
from SkaldBotAPI import app
from Resource.GetActionLink import GetActionLink
from Resource.GetForms import GetForms
from Resource.GetFormsByPageId import GetFormsByPageId
from Resource.GetFormSchema import GetFormSchema
from Resource.GetFormName import GetFormName
from Resource.SubmitItem import SubmitItem
from Resource.Login import Login
from Resource.Register import Register
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
