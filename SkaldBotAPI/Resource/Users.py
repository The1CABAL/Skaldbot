from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request
from Models.Models import *


class Login(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            #print('Authenticating user...')
            req_data = request.get_json()

            user = User(req_data['username'], req_data['password'])
    
            isAuth = SQL.login(user)

            if isAuth:
                response = app.response_class(
                        response = json.dumps({"Message": "LoginSuccess"}),
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

class Register(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            #print('Registering user...')
            req_data = request.get_json()
            
            user = User(req_data['username'], req_data['firstname'], req_data['lastname'], req_data['password'])
    
            isAuth = SQL.register(user)

            if isAuth:
                response = app.response_class(
                        response = json.dumps({"Message": "LoginSuccess"}),
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

class GetAllUsers(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            isMaster = request.args.get('isMaster')
            data = SQL.get_all_users(isMaster)

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

class GetUserForProfile(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            userId = request.args.get('userId')
            data = SQL.get_user_by_id(userId)

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
    def post(self):
        if SQL.test_connect_to_dbo():
            data = request.get_json()
            data = data[0]
            role = data['r'][0]
            role = role['Role']
            
            userInfo = UserProfile(data['Username'], data['FirstName'], data['LastName'], data['IsActive'], data['IsLocked'], role)
            
            SQL.update_user(userInfo)

            response = app.response_class(
                response = json.dumps({"Message": "Success"}),
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