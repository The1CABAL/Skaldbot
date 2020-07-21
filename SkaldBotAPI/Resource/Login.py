from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request
from Models.Models import *


class Login(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            print('Authenticating user...')
            req_data = request.get_json()

            user = User(req_data['username'], req_data['password'])
    
            isAuth = SQL.login(user)

            if isAuth:
                response = app.response_class(
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
