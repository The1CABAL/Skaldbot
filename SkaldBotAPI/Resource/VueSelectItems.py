from flask_restful import Resource
from Classes.SQL import SQL
from SkaldBotAPI import app
from Models.Models import *
from flask import json, request
from Classes.Helpers import Helpers


class VueSelectItem(Resource):
    def get(self):
        if SQL.test_connect_to_dbo():
            serverId = request.args.get('id')

            selectItem = SQL.get_select_item(serverId)

            sql = Helpers.built_select_item_query(selectItem)

            items = SQL.execute_built_query(sql)

            nameValueKey = Helpers.get_name_and_value_columns(selectItem)

            itemsToReturn = {"Items": items, "NameValueCols": nameValueKey}
            
            response = app.response_class(response = json.dumps(itemsToReturn),
                status = 200,
                mimetype='application/json')

            return response
        else:
            response = app.response_class(status=424,
                mimetype='application/json')
            return response