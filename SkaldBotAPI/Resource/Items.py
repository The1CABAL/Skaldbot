from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request

class Stories(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():

            stories = SQL.get_all_stories()

            response = app.response_class(
                response = json.dumps(stories),
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

class Story(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            id = request.args.get('id')

            story = SQL.get_story_by_id(id)

            response = app.response_class(
                response = json.dumps(story),
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

            story = StoryModel(req_data[0]['Id'], req_data[0]['Title'], req_data[0]['Story'], req_data[0]['IsActive'])

            updated = SQL.update_story(story)

            if updated:
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

class Wisdoms(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():

            wisdoms = SQL.get_all_wisdoms()

            response = app.response_class(
                response = json.dumps(wisdoms),
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

class Wisdom(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            id = request.args.get('id')

            wisdom = SQL.get_wisdom_by_id(id)

            response = app.response_class(
                response = json.dumps(wisdom),
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

            wisdom = WisdomModel(req_data[0]['Id'], req_data[0]['Title'], req_data[0]['Wisdom'], req_data[0]['IsActive'])

            updated = SQL.update_wisdom(wisdom)

            if updated:
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

