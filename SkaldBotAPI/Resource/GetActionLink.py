from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request

class GetActionLink(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            formKey = request.args.get('formKey')
            data = SQL.get_form_actionlink(formKey)
            #print(json.dumps(data))

            response = app.response_class(
                response = json.dumps(data),
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
