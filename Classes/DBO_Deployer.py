
import pymssql
from Classes.SQL import SQL
from Classes.ConfigParser import *

def deploy_database():
    conn = SQL.open_master_connection()
    c = conn.cursor()

    try:
        sql = 'CREATE DATABASE SkaldBot.Database'
        c.execute(sql)

    except pymssql.Error as sqlerr:
        if 'already' in sqlerr:
            pass
        else:
            print('Error Creating Database!')
            print('')
            print(str(sqlerr))