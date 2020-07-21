from flask_restful import Resource
from flask import json, request
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *

class SubmitItem(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            print('subimt story called')
            req_data = request.get_json()

            suggestion = Suggestion(req_data['typeId'], req_data['title'], req_data['story'], req_data['email'])
    
            isSubmitted = SQL.submit_item_suggestion(suggestion);

            if isSubmitted:
                response = app.response_class(
                        response = json.dumps({"Message": "Success"}),
                        status = 200,
                        mimetype='application/json'
                    )
                return response
            else:
                response = app.response_class(
                    response = json.dumps({"Message": "Failure"}),
                    status=424,
                    mimetype='application/json'
                )
                return response
