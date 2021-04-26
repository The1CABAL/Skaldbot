from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request
from Models.Models import *
from Classes.PaginationHelper import PaginationHelper


class Login(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            req_data = request.get_json()

            user = User(req_data['username'], req_data['password'])
    
            isAuth = SQL.login(user)

            if isAuth:
                response = app.response_class(response = json.dumps(isAuth),
                        status = 200,
                        mimetype='application/json')
                return response
            else:
                response = app.response_class(status=424,
                    mimetype='application/json')
                return response

class Register(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            req_data = request.get_json()
            
            user = RegisterUser(req_data['accountname'], req_data['username'], req_data['firstname'], req_data['lastname'], req_data['discorduserid'], req_data['password'])
    
            isAuth = SQL.register(user)

            if isAuth:
                response = app.response_class(response = json.dumps({"Message": "LoginSuccess"}),
                        status = 200,
                        mimetype='application/json')
                return response
            else:
                response = app.response_class(status=424,
                    mimetype='application/json')
                return response

class RegisterNewUser(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            req_data = request.get_json()

            user = RegisterAccountUser(req_data['accountid'],
            req_data['username'], req_data['firstname'], req_data['lastname'],
            req_data['discorduserid'], req_data['password'])
            isAuth = SQL.registerUser(user)
            
            if isAuth:
                response = app.response_class(response = json.dumps({"Message": "Register Success"}), status=200, mimetype='application/json')
                return response
            else:
                response = app.response_class(response = json.dumps({"Message": "Failure"}), status=200, mimetype='application/json')
                return response
        else:
            response = app.response_class(status=424,
                    mimetype='application/json')
            return response

class GetUserRoles(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            Id = request.args.get('id')
        
            data = SQL.get_user_role(Id)

            response = app.response_class(response = json.dumps(data),
                status=200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response

class GetAllUsers(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            isMaster = request.args.get('isMaster')
            paginationModel = PaginationHelper(request.args, 'Username', ["Id", "Username", "FirstName", "LastName", "IsActive", "CreateDate"]);

            data = SQL.get_all_users(isMaster, paginationModel)

            response = app.response_class(response = json.dumps(data),
                status=200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response

class GetUserForProfile(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            userId = request.args.get('userId')
            data = SQL.get_user_by_id(userId)

            response = app.response_class(response = json.dumps(data),
                status=200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response
    def post(self):
        if SQL.test_connect_to_dbo():
            data = request.get_json()
            data = data[0]
            role = data['r'][0]
            role = role['Role']
            
            discordUserId = None

            data_dic = json.loads(json.dumps(data))
            discordExists = "DiscordUserId" in data_dic

            if discordExists:
                discordUserId = data['DiscordUserId']
            else:
                discordUserId = "NULL"

            userInfo = UserProfile(data['Username'], data['FirstName'], data['LastName'], discordUserId, data['IsActive'], data['IsLocked'], role)
            
            SQL.update_user(userInfo)

            response = app.response_class(response = json.dumps({"Message": "Success"}),
                status=200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response

class ChangePassword(Resource):
    def post(self):
        if SQL.test_connect_to_dbo():
            req_data = request.get_json()

            password = ChangePasswordModel(req_data['userId'], req_data['password'])

            isUpdated = SQL.update_user_password(password)

            if isUpdated:
                response = app.response_class(response = json.dumps({"Message": "Success"}),
                status=200,
                mimetype='application/json')

                return response
            else:
                response = app.response_class(response = json.dumps({"Message": "Fail"}),
                status=424,
                mimetype='application/json')

                return response
        else:
            response = app.response_class(response = json.dumps({"Message": "Fail"}),
                status=424,
                mimetype='application/json')

            return response