
import sqlite3, json, urllib.request
import pandas as pd
from time import sleep

class SQLITE():
    #Creates database
    def create_dbo():
        conn = sqlite3.connect('SB_EDDB.sqlite3')
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS CodeModules (id INT NOT NULL, group_id INT, class TEXT, rating TEXT, price INT, weapon_mode TEXT, missile_type TEXT, name TEXT, belongs_to TEXT, ed_id TEXT, ed_symbol TEXT, game_context_id TEXT, mass TEXT, ship TEXT, 'group' TEXT, PRIMARY KEY(id, group_id) ON CONFLICT REPLACE)")
        c.execute("CREATE TABLE IF NOT EXISTS CodeStations (id INT NOT NULL, name TEXT, system_id TEXT, updated_at TEXT, max_landing_pad_size TEXT, distance_to_star TEXT, government_id TEXT, government TEXT, allegiance_id TEXT, allegiance TEXT, states TEXT, type_id TEXT, type TEXT, has_blackmarket TEXT, has_market TEXT, has_refuel TEXT, has_repair TEXT, has_rearm TEXT, has_outfitting TEXT, has_shipyard TEXT, has_docking TEXT, has_commodities TEXT, import_commodities TEXT, export_commodities TEXT, prohibited_commodities TEXT, economies TEXT, shipyard_updated_at TEXT, outfitting_updated_at TEXT, market_updated_at TEXT, is_planetary TEXT, selling_ships TEXT, selling_modules TEXT, settlement_size_id TEXT, settlement_size TEXT, settlement_security_id TEXT, settlement_security TEXT, body_id TEXT, controlling_minor_faction_id TEXT, ed_market_id TEXT, PRIMARY KEY(id) ON CONFLICT REPLACE)")
        c.execute("CREATE TABLE IF NOT EXISTS CodeSystems (id INT NOT NULL, edsm_id TEXT, name TEXT, x TEXT, y TEXT, z TEXT, population TEXT, is_populated TEXT, government_id TEXT, government TEXT, allegiance_id TEXT, allegiance TEXT, security_id TEXT, security TEXT, primary_economy_id TEXT, primary_economy TEXT, power TEXT, power_state TEXT, power_state_id TEXT, needs_permit TEXT, updated_at TEXT, simbad_ref TEXT, controlling_minor_faction_id TEXT, controlling_minor_faction TEXT, reserve_type_id TEXT, reserve_type TEXT, ed_system_address, PRIMARY KEY(id) ON CONFLICT REPLACE)")


        conn.commit()
        c.close()
        conn.close()

    #Populates database from EDDB.io API links
    def populate_jsons():
        conn = sqlite3.connect('SB_EDDB.sqlite3')
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
                        key = "'group'"
                    keys.append(key)

                #Iterate through the line and build a list of values associated with those keys
                values = []
                for i in keys:
                    i.replace('Mk.', 'Mk')
                    if i == "'group'":
                        i = 'group'
                    try:
                        values.append(str(line[i]))
                    except:
                        pass


                #Make list of questionmarks
                variable_list = []
                for e in keys:
                    variable_list.append('?')

                #join necessary lists into comma separated string which can be used as the query input
                col_name_string = ', '.join(keys)
                var_string = ', '.join(variable_list)
                val_string = ', '.join(values)

                #Insert values
                try:
                    c.execute('INSERT INTO '+ table +'('+col_name_string+') VALUES ('+val_string + ');')
                except:
                    pass

        conn.commit()
        c.close()
        conn.close()
        sleep(86400)

    def get_all_systems():
        conn = sqlite3.connect('SB_EDDB.sqlite3')
        c = conn.cursor()

        link = 'https://eddb.io/archive/v6/systems.csv'
        print('Getting Data')
        data = pd.read_csv(link, sep=',', dtype={'a': str})
        print('Finally got Data')
        headers = next(data)

        marks = []
        for i in headers:
            marks.append('?')

        col_name_string = ', '.join(headers)
        var_string = ', '.join(marks)

        for row in data:
            values = row
            print(row)
            c.execute('INSERT INTO CodeSystems ('+col_name_string+') VALUES ('+var_string+');', row)

        conn.commit()
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
            conn = sqlite3.connect('SB_EDDB.sqlite3')
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

        except sqlite3.Error as e:
            print("Error getting closest coordinates. Error: " + e)


