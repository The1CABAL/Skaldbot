from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request


class GetFormSchema(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            formKey = request.args.get('formKey')
            #print('Getting Form Data for FormKey: {}'.format(formKey))
        
            data = SQL.get_form_schema(formKey)
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
