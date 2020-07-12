
import json, urllib.request, pymssql
import pandas as pd
from time import sleep
from Classes.ConfigParser import *

class SQL():
    #Creates database
    #def create_dbo():
    #    conn = sqlite3.connect('SB_EDDB.sqlite3')
    #    c = conn.cursor()

    #    c.execute("CREATE TABLE IF NOT EXISTS CodeModules (id INT NOT NULL, group_id INT, class TEXT, rating TEXT, price INT, weapon_mode TEXT, missile_type TEXT, name TEXT, belongs_to TEXT, ed_id TEXT, ed_symbol TEXT, game_context_id TEXT, mass TEXT, ship TEXT, 'group' TEXT, PRIMARY KEY(id, group_id) ON CONFLICT REPLACE)")
    #    c.execute("CREATE TABLE IF NOT EXISTS CodeStations (id INT NOT NULL, name TEXT, system_id TEXT, updated_at TEXT, max_landing_pad_size TEXT, distance_to_star TEXT, government_id TEXT, government TEXT, allegiance_id TEXT, allegiance TEXT, states TEXT, type_id TEXT, type TEXT, has_blackmarket TEXT, has_market TEXT, has_refuel TEXT, has_repair TEXT, has_rearm TEXT, has_outfitting TEXT, has_shipyard TEXT, has_docking TEXT, has_commodities TEXT, import_commodities TEXT, export_commodities TEXT, prohibited_commodities TEXT, economies TEXT, shipyard_updated_at TEXT, outfitting_updated_at TEXT, market_updated_at TEXT, is_planetary TEXT, selling_ships TEXT, selling_modules TEXT, settlement_size_id TEXT, settlement_size TEXT, settlement_security_id TEXT, settlement_security TEXT, body_id TEXT, controlling_minor_faction_id TEXT, ed_market_id TEXT, PRIMARY KEY(id) ON CONFLICT REPLACE)")
    #    c.execute("CREATE TABLE IF NOT EXISTS CodeSystems (id INT NOT NULL, edsm_id TEXT, name TEXT, x TEXT, y TEXT, z TEXT, population TEXT, is_populated TEXT, government_id TEXT, government TEXT, allegiance_id TEXT, allegiance TEXT, security_id TEXT, security TEXT, primary_economy_id TEXT, primary_economy TEXT, power TEXT, power_state TEXT, power_state_id TEXT, needs_permit TEXT, updated_at TEXT, simbad_ref TEXT, controlling_minor_faction_id TEXT, controlling_minor_faction TEXT, reserve_type_id TEXT, reserve_type TEXT, ed_system_address, PRIMARY KEY(id) ON CONFLICT REPLACE)")


    #    conn.commit()
    #    c.close()
    #    conn.close()

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
            'CodeModules': 'https://eddb.io/archive/v6/modules.json',
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
                            newvalue.replace("'", "''''")
                        elif newvalue == None:
                            newvalue = 'None'

                        '''
                        The following nightmare is designed to check 
                        for integers and add them to the list appropriately
                        '''
                        try:
                            newvalue +=1
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
                col_name_string = ', '.join(keys)
                val_string = ', '.join(values)

                #Insert values
                try:
                    sqlstring = ('INSERT INTO '+ table +'('+col_name_string+') VALUES ('+val_string + ')')
                    c.execute(sqlstring)
                    values = []
                    keys = []
                    col_name_string = ''
                    val_string = ''
                    print('Inserted row!')
                except pymssql.OperationalError as ex:
                    print('Error Inserting JSON!')
                    print('')
                    print('SQL:    '+sqlstring)
                    print('')
                    print('ERROR:    '+str(ex))

        conn.commit()
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


