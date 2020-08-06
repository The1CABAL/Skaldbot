from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request

class Server(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            serverId = request.args.get('id')

            server = SQL.get_server_by_id(serverId)
            
            response = app.response_class(response = json.dumps(server),
                status = 200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response
            
class AccountServers(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            accountId = request.args.get('accountId')

            servers = SQL.get_servers_by_account(accountId)

            response = app.response_class(response = json.dumps(servers),
                status = 200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response
    def post(self):
        if SQL.test_connect_to_dbo():
            req_data = request.get_json()

            id = 0
            data_dic = json.loads(json.dumps(req_data))
            idExists = "Id" in data_dic

            if idExists:
                id = req_data['Id']
            else:
                id = 0

            serverData = AccountServerModel(req_data['Id'], req_data['ServerId'], req_data['AccountId'], req_data['Nickname'])

            isSuccess = SQL.update_server(serverData)

            if isSuccess:
                response = app.response_class(response = json.dumps({"Message": "Success"}), status = 200,
                    mimetype='application/json')

                return response
            else:
                response = app.response_class(response = json.dumps({"Message": "Failure"}), status = 424,
                    mimetype='application/json')

                return response
        else:
            response = app.response_class(response = json.dumps({"Message": "Failure"}), status = 424,
                  mimetype='application/json')

            return response
