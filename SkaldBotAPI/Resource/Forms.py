from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request
from Classes.PaginationHelper import PaginationHelper

class GetFormName(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            formKey = request.args.get('formKey')
            data = SQL.get_form_name(formKey)

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
        
            data = SQL.get_form_schema(formKey)

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
            paginationModel = PaginationHelper(request.args, 'FormKey', ["FormKey", "FormName", "IsActive"]);

            forms = SQL.get_all_forms(paginationModel)

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
            req_data = request.get_json()

            title = ''
            data_dic = json.loads(json.dumps(req_data))
            titleExists = "title" in data_dic

            if titleExists:
                title = req_data['title']
            else:
                title = "NULL"

            suggestion = Suggestion(req_data['typeId'], title, req_data['story'], req_data['ServerId'], req_data['discordUserId'])
    
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
            
            paginationModel = PaginationHelper(request.args, 'CreateDate', ["Title", "CreateDate", "ItemType", "IsApproved", "IsReviewed"])

            items = SQL.get_submitted_items(paginationModel)

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

            if isUpdated:
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
            data = req_data['data']['FieldInfo']
            userId = req_data['userId']
            isNew = req_data['isNew']

            form = FormModel(data['FormKey'], data['FieldSchema'], data['ActionLink'], data['IsActive'], req_data['formName'])
            isUpdated = False;

            if isNew:
                isUpdated = SQL.create_form(form, userId);
            else:
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