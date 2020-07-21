"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, json, request
from flask_cors import CORS
from SkaldBotAPI import app
from Classes.SQL import SQL
import threading
from Models.Models import *

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

@app.route('/api/getForms', methods=['GET'])
def getForms():
    if VerifyConnection():
        #print('Getting Forms')
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

@app.route('/api/getFormSchema', methods=['GET'])
def getFormSchema():
    if VerifyConnection():
        formKey = request.args.get('formKey')
        #print('Getting Form Data for FormKey: {}'.format(formKey))
        
        data = SQL.get_form_schema(formKey)
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

@app.route('/api/getActionLink', methods=['GET'])
def getFormActionLink():
    if VerifyConnection():
        formKey = request.args.get('formKey')

        data = SQL.get_form_actionlink(formKey)
        #print(json.dumps(data))

        response = app.response_class(
            response = json.dumps(data),
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


@app.route('/api/submitstory', methods=['POST'])
def submitStory():
    print('subimt story called')
    req_data = request.get_json()

    suggestion = Suggestion(req_data['title'], req_data['story'], req_data['email'])
    
    isSubmitted = submitSuggestion(1, suggestion);

    if isSubmitted:
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

@app.route('/api/submitwisdom', methods=['POST'])
def submitWisdom():
    print('submit wisdom called')
    req_data = request.get_json()

    suggestion = Suggestion(req_data['title'], req_data['story'], req_data['email'])
    
    isSubmitted = submitSuggestion(2, suggestion);

    if isSubmitted:
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


def submitSuggestion(itemTypeId, suggestion):
    isSubmitted = SQL.submit_item_suggestion(itemTypeId, suggestion);

    if isSubmitted:
        return True
    else:
        return False