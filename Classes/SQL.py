
import json, urllib.request, pymssql, random
import pandas as pd
from time import sleep
from Classes.ConfigParser import *

class SQL():

    #Test connection to database
    def test_connect_to_dbo():
        conn = SQL.open_connection()
        if conn:
            try:
                conn.close()
                return True
            except pymssql.Error as conn_er:
                print("Error in test_connect_to_dbo")
                print(conn_er)
                return False

    #Build Connection String
    def open_connection():
        config = LoadConfig('config.ini')

        if config:
            integrated = config['database.integratedsecurity']

            if (integrated.lower() == "true"):
                try:
                    conn = pymssql.connect(server = config['database.server'], database=config['database.name'])
                except pymssql.Error as conn_er:
                    print("Connection Error!")
                    print(conn_er)
            else:
                try:
                    conn = pymssql.connect(server = config['database.server'], user=config['database.user'], password=config['database.password'], database=config['database.name'])
                except pymssql.Error as conn_er:
                    print("Connection Error!")
                    print(conn_er)

            return conn
        else:
            return None

    #Populates database from EDDB.io API links
    def populate_jsons():
        conn = SQL.open_connection()
        c = conn.cursor()

        JSON_urls = {
            #'CodeModules': 'https://eddb.io/archive/v6/modules.json',
            #'CodeCommodities': 'https://eddb.io/archive/v6/commodities.json',
            'CodeStations': 'https://eddb.io/archive/v6/stations.json'
            }

        #Iterate through the URLS and Collect JSON data
        for table in JSON_urls:
            link = JSON_urls[table]
            openedlink = urllib.request.urlopen(link)
            data = json.loads(openedlink.read())

            #iterate trhough the line to build a list of keys
            keys = []
            for line in data:
                for key in line:
                    if key == 'group':
                        #key = '[group]'
                        pass
                    else:
                        keys.append(key)

                #Iterate through the line and build a list of values associated with those keys
                values = []
                for i in keys:
                    if i == "[group]":
                        i = 'group'
                    try:
                        newvalue = str(line[i])
                        if '{' in newvalue:
                            newvalue = newvalue.replace("'", "''''")
                        elif '[' in newvalue:
                            newvalue = newvalue.replace("'", "''''")
                        elif newvalue == None:
                            newvalue = 'None'

                        '''
                        The following nightmare is designed to check 
                        for integers and add them to the list appropriately
                        '''
                        try:
                            newvalue + 1
                            values.append(newvalue)
                        except:
                            values.append("N'"+newvalue+"'")
                    except:
                        pass


                #Convert NoneTypes to NULLtype for SQL Server
                for n, i in enumerate(values):
                    if i == "N'None'":
                        values[n] = 'NULL'

                #join necessary lists into comma separated string which can be used as the query input
                #col_name_string = ', '.join(keys)
                val_string = ', '.join(values)

                upsertTable = 'Upsert' + table

                #Insert values
                try:
                    sqlstring = ('EXEC ' + upsertTable + ' ' + val_string + '')
                    #sqlstring = ('INSERT INTO '+ table +'('+col_name_string+') VALUES ('+val_string + ')')
                    c.execute(sqlstring)
                    values = []
                    keys = []
                    #col_name_string = ''
                    val_string = ''
                except pymssql.Error as ex:
                    print('Error Inserting JSON!')
                    print('')
                    print('SQL:    '+sqlstring)
                    print('')
                    print('ERROR:    '+str(ex))
                    values = []
                    keys = []
                    #col_name_string = ''
                    val_string = ''
                conn.commit()

            print('Done with '+table)
        c.close()
        conn.close()
        sleep(86400)

    def get_all_systems():
        conn = SQL.open_connection()
        c = conn.cursor()
        chunksize = 10 ** 6

        link = 'https://eddb.io/archive/v6/systems.csv'
        print('Getting Data')
        for chunk in pd.read_csv(link, sep=',', chunksize=chunksize, dtype={'id': int, 'edsm_id':str,'name':str,'x':str,'y':str,'z':str,'population':str,'is_populated':str,'government_id':str,
                                                                            'government':str,'allegiance_id':str,'allegiance':str,'security_id':str,'security':str,'primary_economy_id':str,
                                                                            'primary_economy':str,'power':str,'power_state':str,'power_state_id':str,'needs_permit':str,'updated_at':str,
                                                                            'simbad_ref':str,'controlling_minor_faction_id':str,'controlling_minor_faction':str,'reserve_type_id':str,'reserve_type	ed_system_address':str
                                                                            }
                                 ):
            df = chunk
            print('Got a chunk of data!')
            headers = df.columns

            marks = []
            for i in headers:
                marks.append('?')

            col_name_string = ', '.join(headers)
            var_string = ', '.join(marks)

            for iterant, row in df.iterrows():
                values = []
                for h in headers:
                    values.append(df.at[iterant, h])
                c.execute('INSERT INTO CodeSystems ('+col_name_string+') VALUES ('+var_string+');', row)

            conn.commit()
            print('Done with Chunk')
        conn.close()
        c.close()

    '''
    This function will find modules based on a "like" search submitted by the user.
    And return all the posibilities regarding what the user might have meant for the user to pick from
    '''
    def get_modules_names(search):
        ModuleDict = {}
        pass

        for r in result:
            ModuleDict.update({r[0]:r[1]})

        return ModuleDict

    #This function gets a list of stations that contain the module selected
    def find_station_by_module(ModuleId):
        pass

    #This function gets the closest coordinates 
    def find_closest_coordinates(id):
        sql = 'SELECT x, y, z FROM CodeSystems WHERE Id <> @id GROUP BY x, y, z ORDER BY ABS((SUM(x + y + z) / 3) - (SELECT (SUM(x + y + z) / 3) FROM CodeSystems WHERE id = @id)) LIMIT 1'
        sql = sql.replace('@id', id)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            coordinates = c.fetchall()

            if coordinates == None:
                return None
            else:
                coordinates = c.fetchall()[0]
                c.close()
                conn.close()

                return coordinates

        except pymssql.Error as e:
            print("Error getting closest coordinates. Error: " + e)


    def open_master_connection():
        config = LoadConfig('config.ini')

        if config:
            integrated = config['database.integratedsecurity']

            if (integrated.lower() == "true"):
                try:
                    conn = pymssql.connect(server = config['database.server'], database='master')
                except pymssql.Error as conn_er:
                    print("Connection Error!")
                    print(conn_er)
            else:
                try:
                    conn = pymssql.connect(server = config['database.server'], user=config['database.user'], password=config['database.password'], database='master')
                except pymssql.Error as conn_er:
                    print("Connection Error!")
                    print(conn_er)

            return conn
        else:
            return None

    def get_stories(serverid):
        options = []
        id_query = "SELECT lu.ServerId, s.Id FROM Stories s JOIN CodeServers lu on lu.Id = s.ServerId WHERE lu.ServerId = "+str(serverid)
       
        conn = SQL.open_connection()
        c = conn.cursor()

        c.execute(id_query)
        result = c.fetchall()
        for row in result:
            options.append(row[1])

        max_int = len(options)
        max_int -= 1 

        choice = random.randint(0,max_int)
        decision = options[choice]
        ts_query = "SELECT Title, Story FROM Stories WHERE Id = " + str(decision)

        c.execute(ts_query)
        result = c.fetchall()
        for row in result:
            title, story = row[0], row[1]

        return title, story

    def get_wisdoms(channelid):
        options = []
        id_query = 'SELECT lu.ServerId, w.Id FROM Wisdoms w JOIN CodeServers lu on lu.Id = w.ServerId WHERE lu.ServerId = ' + str(channelid)

        conn = SQL.open_connection()
        c = conn.cursor()

        c.execute(id_query)
        result = c.fetchall()
        for row in result:
            options.append(row[1])

        max_int = ((len(options))-1)
        choice = random.randint(0,max_int)
        decision = options[choice]

        w_query = 'SELECT Wisdom FROM Wisdoms WHERE Id = '+ str(decision)
        c.execute(w_query)
        result = c.fetchall()

        for row in result:
            wisdom = row[0]

        return wisdom

    def get_daily_wisdom_channels():
        channels=[]
        query = 'SELECT ServerId FROM CodeServers WHERE DailyWisdom = 1'

        conn = SQL.open_connection()
        c = conn.cursor()

        c.execute(query)
        result = c.fetchall()

        for row in result:
            channels.append(row[0])

        return channels
