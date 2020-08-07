from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request

class Account(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            accountId = request.args.get('accountId')

            accountInformation = SQL.get_account_info_by_id(accountId)

            response = app.response_class(
                response = json.dumps(accountInformation),
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

            profile = AccountProfile(req_data['AccountId'], req_data['AccountName'], req_data['CreateDate'], req_data['IsActive'])

            data = SQL.update_account(profile);

            if data:
                response = app.response_class(
                    response = json.dumps(data),
                    status = 200,
                    mimetype='application/json'
                )

                return response
            else:
                response = app.response_class(
                    status = 200,
                    mimetype='application/json'
                )

                return response
        else:
            response = app.response_class(
                response = json.dumps({"Message": "Failure"}),
                status = 200,
                mimetype='application/json'
            )

            return response