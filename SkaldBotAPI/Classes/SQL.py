
import json, urllib.request, pymssql
import pandas as pd
from datetime import datetime
from time import sleep
from Classes.ConfigParser import *
from Classes.Cryptography import Cryptography
from Classes.Helpers import Helpers
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
                        elif "'" in newvalue:
                            newvalue = newvalue.replace("'", "''")
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
        #sleep(86400)

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

    def get_all_forms():
        sql = "SELECT FormKey, FormName FROM CodeVueForms WHERE IsActive = 1 FOR JSON AUTO"
        
        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            forms = c.fetchall()[0]

            c.close()
            conn.close()

            return forms;
        except pymssql.Error as e:
            print("Error getting forms. Error: " + e)
            print("SQL" + sql)

    def get_all_forms_by_pageId(pageId):
        sql = "SELECT FormKey, FormName FROM CodeVueForms WHERE IsActive = 1 AND PageId = @pageId FOR JSON AUTO"
        
        sql = sql.replace("@pageId", pageId)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            forms = c.fetchall()[0]

            c.close()
            conn.close()

            return forms;
        except pymssql.Error as e:
            print("Error getting forms. Error: " + e)
            print("SQL" + sql)

    def get_form_schema(formKey):
        sql = "SELECT FieldSchema FROM VueFormFields WHERE FormKey = '@formKey' AND IsActive = 1"
        sql = sql.replace("@formKey", formKey)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            forms = c.fetchall()
            c.close()
            conn.close()
                
            return forms
        except pymssql.Error as e:
            print("Error getting form for FormKey " + formKey + ". Error: " + e)

    def get_form_actionlink(formKey):
        sql = "SELECT ActionLink FROM VueFormFields WHERE FormKey = '@formKey' AND IsActive = 1 FOR JSON AUTO"
        sql = sql.replace("@formKey", formKey)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            forms = c.fetchall()[0]
            c.close()
            conn.close()
                
            return forms
        except pymssql.Error as e:
            print("Error getting action link for FormKey " + formKey + ". Error: " + e)

    def get_form_name(formKey):
        sql = "SELECT FormName FROM CodeVueForms WHERE FormKey = '@formKey' AND IsActive = 1 FOR JSON AUTO"
        sql = sql.replace("@formKey", formKey)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            forms = c.fetchall()[0]
            c.close()
            conn.close()
                
            return forms
        except pymssql.Error as e:
            print("Error getting action link for FormKey " + formKey + ". Error: " + e)

    def submit_item_suggestion(suggestion):
        sql = "INSERT INTO SubmittedItems (ItemTypeId, Title, ItemText, SubmitterEmail, CreateDate) VALUES ('@itemType', '@title', '@text', '@email', '@date')";
        current_date = datetime.now()

        sql = sql.replace("@itemType", suggestion[0])
        sql = sql.replace("@title", suggestion[1])
        sql = sql.replace("@text", suggestion[2])
        sql = sql.replace("@email", suggestion[3])
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            conn.commit()

            c.close()
            conn.close()

            return True
        except pymssql.Error as e:
            print("Error submitting story. Error {}".format(e))
            print(sql)
            return False

    def login(user):
        sql = "SELECT PasswordHash FROM Users WHERE Username = '@username'";

        sql = sql.replace("@username", user[0])

        username = user[0]
        passedPassword = user[1]

        try:
            conn = SQL.open_connection()
            c = conn.cursor()
            c.execute(sql)

            password = c.fetchone()

            if password:
                password = password[0]
                password = Cryptography.dehashPassword(password)
            else:
                return False

            if passedPassword == password:
                getUserData = "SELECT Id, Username FROM Users WHERE Username = '@username' FOR JSON AUTO"
                getUserData = getUserData.replace("@username", user[0])

                c.execute(getUserData)
                userData = c.fetchone()[0]
                c.close()
                conn.close()
                return userData
            else:
                c.close()
                conn.close()
                return None
        except pymssql.Error as e:
            print("Error authenticating user. Error {}".format(e))
            return None

    def register(user):
        sql = "INSERT INTO Users (Username, FirstName, LastName, PasswordHash, CreateDate) VALUES ('@username', '@firstname', '@lastname', '@password', '@date');"
        insertRole = "INSERT INTO UserRoles (UserId, RoleId) VALUES ((SELECT Id FROM Users WHERE Username = '@username'), 3)"
        
        userExists = SQL.userExists(user[0])

        if userExists == False:
            #print("Starting to create user");
            current_date = datetime.now()
            password = Cryptography.hashPassword(user[3])
        
            sql = sql.replace("@username", user[0])
            insertRole = insertRole.replace("@username", user[0])
            sql = sql.replace("@firstname", user[1])
            sql = sql.replace("@lastname", user[2])
            sql = sql.replace("@password", password.decode())
            sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))

            try:
                conn = SQL.open_connection()
                c = conn.cursor()
                c.execute(sql)

                conn.commit()

                c.execute(insertRole)
                conn.commit()

                c.close()
                conn.close()

                return True
            except pymssql.Error as e:
                print("Error authenticating user. Error {}".format(e))
                return False
        else:
            return False

    def userExists(username):
        sql = "SELECT 1 FROM Users WHERE Username = '@username'"

        sql = sql.replace("@username", username)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()
            c.execute(sql)

            any = c.fetchone()

            #print(any)

            if any == None:
                #print("No matching users exist");
                return False
            else:
                return True
        except pymssql.Error as e:
            print("Error finding if user exists. Error {}".format(e))
            return False

    def get_user_role(username):
        sql = "SELECT r.Role FROM Users u WITH (NOLOCK) JOIN UserRoles ur WITH (NOLOCK) ON ur.UserId = u.Id JOIN Roles r WITH (NOLOCK) ON r.Id = ur.RoleId WHERE u.Username = '@username' FOR JSON AUTO"
        sql = sql.replace('@username', username)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()
            c.execute(sql)

            role = c.fetchall()

            if role != None:
                role = role[0]
                return role
            else:
                return None
        except pymssql.Error as e:
            print("Error getting users roles. Error {}".format(e))
            return None

    def get_all_users(isMaster):
        sql = ''

        if isMaster.lower() == "true":
            sql = "SELECT Id, Username, FirstName, LastName, IsActive, CreateDate FROM Users WITH (NOLOCK) FOR JSON AUTO"
        else:
            sql = "SELECT Id, Username, FirstName, LastName, IsActive, CreateDate FROM Users WITH (NOLOCK) WHERE Id <> '2F5FA286-5644-4AB1-B04F-D2ED451EF33F' FOR JSON AUTO"
            

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            users = c.fetchall()

            c.close()
            conn.close()

            return users
        except pymssql.Error as e:
            print("Error getting all users: Error {}".format(e))
            return None

    def get_user_by_id(userId):
        sql = "SELECT u.Username, u.FirstName, u.LastName, u.IsActive, u.IsLocked, u.CreateDate, r.Role FROM Users u WITH (NOLOCK) JOIN UserRoles ur WITH (NOLOCK) ON u.Id = ur.UserId JOIN Roles r WITH (NOLOCK) ON ur.RoleId = r.Id WHERE u.Id = '@userId' FOR JSON AUTO"

        sql = sql.replace("@userId", userId)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            user = c.fetchall()

            c.close()
            conn.close()

            if user:
                user = user[0]
                return user
            else:
                return None
        except pymssql.Error as e:
            print("Error getting user data. Error {}".format(e))
            return None
        
    def get_all_roles():
        sql = "SELECT Role, RoleName FROM Roles WHERE IsActive = 1 FOR JSON AUTO"

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            roles = c.fetchall()

            c.close()
            conn.close()

            return roles
        except pymssql.Error as e:
            print("Error getting roles. Error {}".format(e))
            return None
   
    def update_user(userprofile):
        username = userprofile[0]
        currentRole = "SELECT r.RoleName FROM Users u WITH (NOLOCK) JOIN UserRoles ur WITH (NOLOCK) ON u.Id = ur.UserId JOIN Roles r WITH (NOLOCK) ON ur.RoleId = r.Id WHERE u.Username = '@username'"
        currentRole = currentRole.replace("@username", username)

        updateUser = "UPDATE Users SET Username = '@username', FirstName = '@firstName', LastName = '@lastName', IsActive = @isActive, IsLocked = @isLocked WHERE Id = (SELECT Id FROM Users WHERE Username = '@username')";
        updateUser = updateUser.replace("@username", username)
        updateUser = updateUser.replace("@firstName", userprofile[1])
        updateUser = updateUser.replace("@lastName", userprofile[2])
        updateUser = updateUser.replace("@isActive", Helpers.bool_to_int(userprofile[3]))
        updateUser = updateUser.replace("@isLocked", Helpers.bool_to_int(userprofile[4]))

        updateRole = "DELETE FROM UserRoles WHERE UserId = (SELECT Id FROM Users WHERE Username = '@username'); INSERT INTO UserRoles (UserId, RoleId) VALUES ((SELECT Id FROM Users WHERE Username = '@username'), (SELECT Id FROM Roles WHERE Role = '@role'))"
        updateRole = updateRole.replace("@username", username)
        updateRole = updateRole.replace("@role", userprofile[5])

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(currentRole)

            userRole = c.fetchone()[0]

            if userRole != userprofile[5]:
                print('Updating Role')
                c.execute(updateRole)
                conn.commit()
            
            print('Updating user')
            c.execute(updateUser)
            conn.commit()

            c.close()
            conn.close()
        except pymssql.Error as e:
            print('Error updating user. Error {}'.format(e))

    def get_submitted_items():
        sql = "SELECT si.Id, 'Blank' as ItemType, luIT.ItemType AS ActualItemType, si.Title, si.ItemText, si.SubmitterEmail, si.CreateDate FROM SubmittedItems si WITH (NOLOCK) JOIN CodeItemType luIT WITH (NOLOCK) ON si.ItemTypeId = luIT.Id WHERE si.IsApproved = 0 FOR JSON AUTO";

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            items = c.fetchall()

            c.close()
            conn.close()

            return items
        except pymssql.Error as e:
            print('Error getting submitted items. Error {}'.format(e))

    def get_submitted_item_by_id(id):
        sql = "SELECT si.Title, si.CreateDate, 'Blank' as ItemType, luIT.ItemType, si.ItemText, si.SubmitterEmail FROM SubmittedItems si WITH (NOLOCK) JOIN CodeItemType luIT WITH (NOLOCK) ON si.ItemTypeId = luIT.Id WHERE si.Id = @id FOR JSON AUTO"
        sql = sql.replace("@id", id);

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            item = c.fetchone()

            if item:
                item = item[0]
                return item
            else:
                return None
        except pymssql.Error as e:
            print('Error getting submitted item. Error {}'.format(e))
            return None

    def update_submitted_item(isApproved, id, userId):
        sql = "EXEC UpdateSubmittedItem @isApproved, @id, '@userId'"

        sql = sql.replace("@isApproved", str(isApproved))
        sql = sql.replace("@id", str(id))
        sql = sql.replace("@userId", userId)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            conn.commit()

            c.close()
            conn.close()

            return True
        except pymssql.Error as e:
            print('Error updating the submitted item. Error {}'.format(e))
            return False

    def get_all_stories():
        sql = "SELECT Id, Title, Story, IsActive FROM Stories WITH (NOLOCK) FOR JSON AUTO"

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            stories = c.fetchall()

            c.close()
            conn.close()

            return stories
        except pymssql.Error as e:
            print("Error getting stories. Error {}".format(e))
            return None

    def get_story_by_id(id):
        sql = "SELECT Id, Title, Story, IsActive FROM Stories WITH (NOLOCK) WHERE Id = @id FOR JSON AUTO"

        sql = sql.replace("@id", str(id));

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            story = c.fetchone()

            c.close()
            conn.close()
            if story:
                story = story[0]
                return story
            else:
                return None
        except pymssql.Error as e:
            print("Error getting story by id. Error {}".format(e))
            return None

    def update_story(story):
        sql = "UPDATE Stories SET Title = '@title', Story = '@story', IsActive = @isActive, UpdateDate = '@date' WHERE Id = @Id"
        current_date = datetime.now()

        sql = sql.replace("@title", story[1])
        sql = sql.replace("@story", story[2])
        sql = sql.replace("@isActive", Helpers.bool_to_int(story[3]))
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        sql = sql.replace("@Id", str(story[0]))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()
            
            return True
        except pymssql.Error as e:
            print("Error updating story. Error {}".format(e))
            return False

    def get_all_wisdoms():
        sql = "SELECT Id, Title, Wisdom, IsActive FROM Wisdoms WITH (NOLOCK) FOR JSON AUTO"

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            stories = c.fetchall()

            c.close()
            conn.close()

            return stories
        except pymssql.Error as e:
            print("Error getting stories. Error {}".format(e))
            return None

    def get_wisdom_by_id(id):
        sql = "SELECT Id, Title, Wisdom, IsActive FROM Wisdoms WITH (NOLOCK) WHERE Id = @id FOR JSON AUTO"

        sql = sql.replace("@id", str(id));

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            wisdom = c.fetchone()

            c.close()
            conn.close()
            if wisdom:
                wisdom = wisdom[0]
                return wisdom
            else:
                return None
        except pymssql.Error as e:
            print("Error getting story by id. Error {}".format(e))
            return None

    def update_wisdom(wisdom):
        sql = "UPDATE Wisdoms SET Title = '@title', Wisdom = '@wisdom', IsActive = @isActive, UpdateDate = '@date' WHERE Id = @Id"
        current_date = datetime.now()

        sql = sql.replace("@title", wisdom[1])
        sql = sql.replace("@wisdom", wisdom[2])
        sql = sql.replace("@isActive", Helpers.bool_to_int(wisdom[3]))
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        sql = sql.replace("@Id", str(wisdom[0]))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()
            
            return True
        except pymssql.Error as e:
            print("Error updating story. Error {}".format(e))
            return False



