from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request
from Classes.PaginationHelper import PaginationHelper

class HelpDocumentation(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            helpContentKey = request.args.get('helpContentKey')
            isAdmin = request.args.get('isAdmin')

            #do something here
            helpContent = SQL.get_documentation(helpContentKey, isAdmin)

            response = app.response_class(
                response = json.dumps(helpContent),
                status = 200,
                mimetype='application/json'
            )

            return response
        else:
            response = app.response_class(
                status=424,
                mimetype='application/json'
            )
            return response

    def post(self):
        if SQL.test_connect_to_dbo():
            req_data = request.get_json()

            #do something here
            
            documentation = Documentation(req_data['helpContentKey'], req_data['helpTitle'], req_data['helpContent'], req_data['isActive'], req_data['userId'], req_data['isAdmin'])

            helpContent = SQL.update_documentation(documentation)

            response = app.response_class(
                response = json.dumps(helpContent),
                status = 200,
                mimetype='application/json'
            )

            return response
        else:
            response = app.response_class(
                status=424,
                mimetype='application/json'
            )
            return response

class GetAllDocumentation(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            paginationModel = PaginationHelper(request.args, 'HelpContentKey', ["HelpContentKey", "HelpTitle", "HelpContent", "IsActive"])

            content = SQL.get_all_documentation(paginationModel)

            response = app.response_class(
                response = json.dumps(content),
                status = 200,
                mimetype='application/json'
            )

            return response
        else:
            response = app.response_class(
                status=424,
                mimetype='application/json'
            )
            return response