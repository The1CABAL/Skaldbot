from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request

class GetFormsByPageId(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            pageId = request.args.get('pageId')
            forms = SQL.get_all_forms_by_pageId(pageId)
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

