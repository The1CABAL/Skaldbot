
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