
import sqlite3, json, urllib

class SQLITE():
    #Creates database
    def create_dbo():
        pass

    #Populates database from EDDB.io API links
    def populate_dbo():
        pass

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
