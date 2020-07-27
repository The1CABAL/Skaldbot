from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request

class GetFormName(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            formKey = request.args.get('formKey')
            data = SQL.get_form_name(formKey)
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

class GetFormSchema(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
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

class GetForms(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
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

class GetActionLink(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
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
    def get(self):
        if SQL.test_connect_to_dbo():
            id = request.args.get('id')

            suggestion = SQL.get_submitted_item_by_id(id)

            if suggestion:
                response = app.response_class(
                        response = json.dumps(suggestion),
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
        else:
            response = app.response_class(
                    status=424,
                    mimetype='application/json'
                )
            return response

class ManageSubmittedItems(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            
            items = SQL.get_submitted_items()

            response = app.response_class(
                response = json.dumps(items),
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

            isApproved = req_data['IsApproved']
            id = req_data['Id']
            userId = req_data['UserId']

            isUpdated = SQL.update_submitted_item(isApproved, id, userId)

            response = app.response_class(
                response = json.dumps({"Message": "Success"}),
                status = 200,
                mimetype='application/json')
            
            return response
        else:
            response = app.response_class(
                response = json.dumps({"Message": "Failure"}), 
                status=424, 
                mimetype='application/json')
            return response

class Form(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            formKey = request.args.get('formKey')

            form = SQL.get_form_by_form_key(formKey)
            
            response = app.response_class(
                response = json.dumps(form),
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
            data = req_data['data']
            userId = req_data['userId']
            form = FormModel(data['FormKey'], data['FieldSchema'], data['ActionLink'], data['IsActive'], data['luVF'][0]['FormName'])

            isUpdated = SQL.update_form(form, userId);

            if isUpdated:
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
        else:
            response = app.response_class(
                    response = json.dumps({"Message": "Failure"}),
                    status=424,
                    mimetype='application/json'
                )
            return response