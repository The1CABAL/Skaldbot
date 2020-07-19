"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, json
from flask_cors import CORS
from SkaldBotAPI import app
from Classes.SQL import SQL
import threading

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def VerifyConnection():
    conSuccess = SQL.test_connect_to_dbo()
    return conSuccess

@app.route('/')
@app.route('/api/populatedbo', methods=['GET'])
def populatedbo():
    if VerifyConnection():
        print('Starting Thread')
        SQL.populate_jsons()
        data = {'Status': 'Pass'}
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        data = {'Status': 'Fail'}
        response = app.response_class(
            response=json.dumps(data),
            status=424,
            mimetype='application/json'
        )
        return response
