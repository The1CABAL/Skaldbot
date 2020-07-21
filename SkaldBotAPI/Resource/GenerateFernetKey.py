from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from flask import json, request
from cryptography.fernet import Fernet
from Classes.Cryptography import Cryptography

class GenerateFernetKey(Resource):
    def post(self):
        req_data = request.get_json()

        if req_data['token'] == "30hJtsCWVXRR6qX_vOx1YHmm6guK9tq_YUa_nJqu-4Q=":
            key = Fernet.generate_key();

            returnVal = {"Key" : key}

            response = app.response_class(
                    data = json.dumps(returnVal),
                    status=200,
                    mimetype='application/json'
                  )
            return response
        else:
            response = app.response_class(
                    status=401,
                    mimetype='application/json'
                  )
            return response
        

