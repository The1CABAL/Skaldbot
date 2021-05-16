class Helpers():
    def bool_to_int(value):
        if value:
            return "1"
        else:
            return "0"

    def built_select_item_query(selectItem):
        table = selectItem["TableName"]
        itemCol = selectItem["ItemColumn"]
        valueCol = selectItem["ValueColumn"]
        where = selectItem["WhereClause"]

        sql = ""

        if not where:
            sql = "SELECT @ItemCol AS name, @ValueCol AS value FROM @Table FOR JSON AUTO"    
        else:
            sql = "SELECT @ItemCol AS name, @ValueCol AS value FROM @Table WHERE @Where FOR JSON AUTO"
            sql = sql.replace("@Where", where)


        sql = sql.replace("@ItemCol", itemCol)
        sql = sql.replace("@ValueCol", valueCol)
        sql = sql.replace("@Table", table)

        return sql;

    def get_name_and_value_columns(selectItem):
        itemCol = selectItem["ItemColumn"]
        valueCol = selectItem["ValueColumn"]

        return {"nameCol": itemCol, "valueCol": valueCol}
