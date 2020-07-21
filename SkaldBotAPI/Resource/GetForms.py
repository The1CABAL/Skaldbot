from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json

class GetForms(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            forms = SQL.get_all_forms()
            forms = forms[0]
            response = app.response_class(
                response = json.dumps(forms),
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
