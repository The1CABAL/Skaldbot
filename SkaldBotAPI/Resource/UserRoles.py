from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request


class GetUserRoles(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            username = request.args.get('username')
            #print('Getting Form Data for FormKey: {}'.format(formKey))
        
            data = SQL.get_user_role(username)
            #print(data)

            response = app.response_class(
                response = json.dumps(data),
                status=200,
                mimetype='application/json'
              )

            return response
        else:
            response = app.response_class(
                status=424,
                mimetype='application/json'
            )
            return response

