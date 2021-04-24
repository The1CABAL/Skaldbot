
import json
import urllib.request
import pymssql
import pandas as pd
from datetime import datetime
from time import sleep
from Classes.ConfigParser import *
from Classes.Cryptography import Cryptography
from Classes.Helpers import Helpers
class SQL():
    def get_total_records(data, conn):
       sql = "SELECT COUNT(*) FROM #temp DROP TABLE #temp"

       c = conn.cursor()
       c.execute(sql)

       totalRecords = c.fetchone()

       if (totalRecords):
           totalRecords = totalRecords[0]
       else: 
           totalRecords = "0"

       totalRecords = '{"TotalRecords": ' + str(totalRecords) + "}"

       data.append(totalRecords)

       return data

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
            conn = None;

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

                #Iterate through the line and build a list of values associated
                #with those keys
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
                            values.append("N'" + newvalue + "'")
                    except:
                        pass


                #Convert NoneTypes to NULLtype for SQL Server
                for n, i in enumerate(values):
                    if i == "N'None'":
                        values[n] = 'NULL'

                #join necessary lists into comma separated string which can be
                #used as the query input
                #col_name_string = ', '.join(keys)
                val_string = ', '.join(values)

                upsertTable = 'Upsert' + table

                #Insert values
                try:
                    sqlstring = ('EXEC ' + upsertTable + ' ' + val_string + '')
                    #sqlstring = ('INSERT INTO '+ table +'('+col_name_string+')
                    #VALUES ('+val_string + ')')
                    c.execute(sqlstring)
                    values = []
                    keys = []
                    #col_name_string = ''
                    val_string = ''
                except pymssql.Error as ex:
                    print('Error Inserting JSON!')
                    print('')
                    print('SQL:    ' + sqlstring)
                    print('')
                    print('ERROR:    ' + str(ex))
                    values = []
                    keys = []
                    #col_name_string = ''
                    val_string = ''
                conn.commit()

            print('Done with ' + table)
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
                                                                            }):
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
                c.execute('INSERT INTO CodeSystems (' + col_name_string + ') VALUES (' + var_string + ');', row)

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

    def get_all_forms(pagination):
        sql = """
                DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                DECLARE @IsAscending BIT = @Ascending

                SELECT
                    FormKey,
                    FormName,
                    IsActive
                INTO #temp
                FROM
                    CodeVueForms WITH (NOLOCK)
                WHERE
                    ('@SearchTerm' = ''
                        OR (
                            FormName LIKE '%' + '@SearchTerm' + '%'
                            )
                    )
            
                SELECT
                    *
                FROM
                    #temp
                ORDER BY
                    CASE WHEN @OrderBy = 'FormKey' AND @IsAscending = 1 THEN FormKey END ASC,
                    CASE WHEN @OrderBy = 'FormKey' AND @IsAscending <> 1 THEN FormKey END DESC,
                    CASE WHEN @OrderBy = 'FormName' AND @IsAscending = 1 THEN FormName END ASC,
                    CASE WHEN @OrderBy = 'FormName' AND @IsAscending <> 1 THEN FormName END DESC,
                    CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                    CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC
                OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                FOR JSON AUTO
        """
        
        sql = pagination.replaceParams(sql)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            forms = c.fetchall()

            forms = SQL.get_total_records(forms, conn);

            c.close()
            conn.close()

            return forms
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

            return forms
        except pymssql.Error as e:
            print("Error getting forms. Error: " + e)
            print("SQL" + sql)

    def get_form(formKey):
        sql = "SELECT luVF.FormName, vff.ActionLink, vff.FieldSchema, luFV.ShowFormName FROM CodeVueForms luVF JOIN VueFormFields vff WITH (NOLOCK) ON luVF.FormKey = vff.FormKey WHERE luVF.FormKey = '@formKey' AND luVF.IsActive = 1"
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

    #def get_form_actionlink(formKey):
    #    sql = "SELECT ActionLink FROM VueFormFields WHERE FormKey = '@formKey' AND IsActive = 1 FOR JSON AUTO"
    #    sql = sql.replace("@formKey", formKey)

    #    try:
    #        conn = SQL.open_connection()
    #        c = conn.cursor()

    #        c.execute(sql)
    #        forms = c.fetchall()[0]
    #        c.close()
    #        conn.close()
                
    #        return forms
    #    except pymssql.Error as e:
    #        print("Error getting action link for FormKey " + formKey + ". Error: " + e)

    #def get_form_name(formKey):
    #    sql = "SELECT FormName FROM CodeVueForms WHERE FormKey = '@formKey' AND IsActive = 1 FOR JSON AUTO"
    #    sql = sql.replace("@formKey", formKey)

    #    try:
    #        conn = SQL.open_connection()
    #        c = conn.cursor()

    #        c.execute(sql)
    #        forms = c.fetchall()[0]
    #        c.close()
    #        conn.close()
                
    #        return forms
    #    except pymssql.Error as e:
    #        print("Error getting action link for FormKey " + formKey + ". Error: " + e)

    def submit_item_suggestion(suggestion):
        sql = "INSERT INTO SubmittedItems (ItemTypeId, Title, ItemText, ServerId, DiscordUserId, CreateDate) VALUES ('@itemType', '@title', '@text', @serverId, @discordId, '@date')"
        current_date = datetime.now()

        text = suggestion[2]
        text = text.replace("'", "''");

        sql = sql.replace("@itemType", suggestion[0])
        sql = sql.replace("@title", suggestion[1])
        sql = sql.replace("@text", text)
        sql = sql.replace("@serverId", str(suggestion[3]))
        sql = sql.replace("@discordId", str(suggestion[4]))
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
        sql = "SELECT PasswordHash FROM Users WHERE Username = '@username'"

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

            if True:
                getUserData = "SELECT Id, AccountId, Username FROM Users WHERE Username = '@username' FOR JSON AUTO"
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

    def registerUser(user):
        sql = "INSERT INTO Users (Username, AccountId, FirstName, LastName, DiscordUserId, PasswordHash, CreateDate) VALUES ('@username', @accountId, '@firstname', '@lastname', '@discord', '@password', '@date');"
        insertRole = "INSERT INTO UserRoles (UserId, RoleId) VALUES ((SELECT Id FROM Users WHERE Username = '@username'), 4)"
        userExists = SQL.userExists(user[1])

        if userExists == False:
            current_date = datetime.now()
            password = Cryptography.hashPassword(user[5])

            sql = sql.replace("@accountId", str(user[0]))
            sql = sql.replace("@username", user[1])
            sql = sql.replace("@firstname", user[2])
            sql = sql.replace("@lastname", user[3])
            sql = sql.replace("@discord", str(user[4]))
            sql = sql.replace("@password", password.decode())
            sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
            insertRole = insertRole.replace("@username", user[1])

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
                print("Error creating account user. Error {}".format(e))
                return False

    def register(user):
        sql = "INSERT INTO Users (Username, AccountId, FirstName, LastName, DiscordUserId, PasswordHash, CreateDate) VALUES ('@username', @accountId, '@firstname', '@lastname', '@discord', '@password', '@date');"
        insertRole = "INSERT INTO UserRoles (UserId, RoleId) VALUES ((SELECT Id FROM Users WHERE Username = '@username'), 3)"
        createAccount = "INSERT INTO Accounts (AccountName) VALUES ('@account'); SELECT CAST(scope_identity() as int)"
        
        userExists = SQL.userExists(user[1])

        if userExists == False:
            current_date = datetime.now()
            password = Cryptography.hashPassword(user[5])
        
            sql = sql.replace("@username", user[1])
            insertRole = insertRole.replace("@username", user[1])
            sql = sql.replace("@firstname", user[2])
            sql = sql.replace("@lastname", user[3])
            sql = sql.replace("@discord", str(user[4]))
            sql = sql.replace("@password", password.decode())
            sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
            createAccount = createAccount.replace("@account", user[0])

            try:
                conn = SQL.open_connection()
                c = conn.cursor()
                
                c.execute(createAccount)
                accountId = c.fetchone()
                conn.commit()

                
                sql = sql.replace("@accountId", str(accountId[0]))
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

    def get_user_role(Id):
        sql = "SELECT r.Role FROM UserRoles ur WITH (NOLOCK) JOIN Roles r WITH (NOLOCK) ON r.Id = ur.RoleId WHERE ur.UserId = '@userId' FOR JSON AUTO"
        sql = sql.replace('@userId', Id)

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

    def get_all_users(isMaster, pagination):
        sql = ''

        if isMaster.lower() == "true":
            sql = """
                    DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                    DECLARE @IsAscending BIT = @Ascending

                    SELECT 
	                    Id, 
	                    Username, 
	                    FirstName, 
	                    LastName, 
	                    IsActive, 
	                    CreateDate
                    INTO #temp
                    FROM 
                    	Users WITH (NOLOCK)
                    WHERE
                        ('@SearchTerm' = '' 
                            OR (
                                UserName LIKE '%' + '@SearchTerm' + '%' 
                                OR FirstName LIKE '%' + '@SearchTerm' + '%' 
                                OR LastName LIKE '%' + '@SearchTerm' + '%'
                                )
                        )
                        
                    SELECT
                    	*
                    FROM
                    	#temp
                    ORDER BY
                    	CASE WHEN @OrderBy = 'Id' AND @IsAscending = 1 THEN Id END ASC,
                    	CASE WHEN @OrderBy = 'Id' AND @IsAscending <> 1 THEN Id END DESC,
                        CASE WHEN @OrderBy = 'Username' AND @IsAscending = 1 THEN Username END ASC,
                    	CASE WHEN @OrderBy = 'Username' AND @IsAscending <> 1 THEN Username END DESC,
                        CASE WHEN @OrderBy = 'FirstName' AND @IsAscending = 1 THEN FirstName END ASC,
                    	CASE WHEN @OrderBy = 'FirstName' AND @IsAscending <> 1 THEN FirstName END DESC,
                        CASE WHEN @OrderBy = 'LastName' AND @IsAscending = 1 THEN LastName END ASC,
                    	CASE WHEN @OrderBy = 'LastName' AND @IsAscending <> 1 THEN LastName END DESC,
                        CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                    	CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC,
                        CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending = 1 THEN CreateDate END ASC,
                    	CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending <> 1 THEN CreateDate END DESC
                    OFFSET ((@CurrentPage - 1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                    FOR JSON AUTO
                """
        else:
            sql = """
                    DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                    DECLARE @IsAscending BIT = @Ascending

                    SELECT 
	                    Id, 
	                    Username, 
	                    FirstName, 
	                    LastName, 
	                    IsActive, 
	                    CreateDate
                    INTO #temp
                    FROM 
                    	Users WITH (NOLOCK)
                    WHERE
                        ('@SearchTerm' = '' 
                            OR (
                                UserName LIKE '%' + '@SearchTerm' + '%' 
                                OR FirstName LIKE '%' + '@SearchTerm' + '%' 
                                OR LastName LIKE '%' + '@SearchTerm' + '%'
                                )
                        )
                        AND Id <> '2F5FA286-5644-4AB1-B04F-D2ED451EF33F'
                        
                    SELECT
                    	*
                    FROM
                    	#temp
                    ORDER BY
                    	CASE WHEN @OrderBy = 'Id' AND @IsAscending = 1 THEN Id END ASC,
                    	CASE WHEN @OrderBy = 'Id' AND @IsAscending <> 1 THEN Id END DESC,
                        CASE WHEN @OrderBy = 'Username' AND @IsAscending = 1 THEN Username END ASC,
                    	CASE WHEN @OrderBy = 'Username' AND @IsAscending <> 1 THEN Username END DESC,
                        CASE WHEN @OrderBy = 'FirstName' AND @IsAscending = 1 THEN FirstName END ASC,
                    	CASE WHEN @OrderBy = 'FirstName' AND @IsAscending <> 1 THEN FirstName END DESC,
                        CASE WHEN @OrderBy = 'LastName' AND @IsAscending = 1 THEN LastName END ASC,
                    	CASE WHEN @OrderBy = 'LastName' AND @IsAscending <> 1 THEN LastName END DESC,
                        CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                    	CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC,
                        CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending = 1 THEN CreateDate END ASC,
                    	CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending <> 1 THEN CreateDate END DESC
                    OFFSET ((@CurrentPage - 1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                    FOR JSON AUTO
                   """
        
        sql = pagination.replaceParams(sql);

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            users = c.fetchall()

            users = SQL.get_total_records(users, conn)

            c.close()
            conn.close()

            return users
        except pymssql.Error as e:
            print("Error getting all users: Error {}".format(e))
            return None

    def get_user_by_id(userId):
        sql = "SELECT u.Username, u.FirstName, u.LastName, u.DiscordUserId, u.IsActive, u.IsLocked, u.CreateDate, r.Role FROM Users u WITH (NOLOCK) JOIN UserRoles ur WITH (NOLOCK) ON u.Id = ur.UserId JOIN Roles r WITH (NOLOCK) ON ur.RoleId = r.Id WHERE u.Id = '@userId' FOR JSON AUTO"

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
        currentRole = "SELECT r.Role FROM Users u WITH (NOLOCK) JOIN UserRoles ur WITH (NOLOCK) ON u.Id = ur.UserId JOIN Roles r WITH (NOLOCK) ON ur.RoleId = r.Id WHERE u.Username = '@username'"
        currentRole = currentRole.replace("@username", username)

        updateUser = "UPDATE Users SET Username = '@username', FirstName = '@firstName', LastName = '@lastName', DiscordUserId = @discord, IsActive = @isActive, IsLocked = @isLocked WHERE Id = (SELECT Id FROM Users WHERE Username = '@username')"
        updateUser = updateUser.replace("@username", username)
        updateUser = updateUser.replace("@firstName", userprofile[1])
        updateUser = updateUser.replace("@lastName", userprofile[2])
        updateUser = updateUser.replace("@discord", str(userprofile[3]))
        updateUser = updateUser.replace("@isActive", Helpers.bool_to_int(userprofile[4]))
        updateUser = updateUser.replace("@isLocked", Helpers.bool_to_int(userprofile[5]))

        updateRole = "DELETE FROM UserRoles WHERE UserId = (SELECT Id FROM Users WHERE Username = '@username'); INSERT INTO UserRoles (UserId, RoleId) VALUES ((SELECT Id FROM Users WHERE Username = '@username'), (SELECT Id FROM Roles WHERE Role = '@role'))"
        updateRole = updateRole.replace("@username", username)
        updateRole = updateRole.replace("@role", userprofile[6])

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(currentRole)

            userRole = c.fetchone()[0]

            if userRole != userprofile[6]:
                c.execute(updateRole)
                conn.commit()
            
            c.execute(updateUser)
            conn.commit()

            c.close()
            conn.close()
        except pymssql.Error as e:
            print('Error updating user. Error {}'.format(e))

    def get_submitted_items(pagination):
        sql = """
                DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                DECLARE @IsAscending BIT = @Ascending

                SELECT
                    si.Id,
                    'Blank' as ItemType,
                    luIT.ItemType as ActualItemType,
				    si.Title,
				    si.ItemText,
				    si.DiscordUserId,
				    si.CreateDate,
				    si.IsApproved,
				    si.IsReviewed
                INTO #temp
                FROM
                    SubmittedItems si WITH (NOLOCK)
				    JOIN CodeItemType luIT WITH (NOLOCK) ON si.ItemTypeId = luIT.Id
                WHERE
				    si.IsApproved = 0
                    AND ('@SearchTerm' = ''
                        OR (
                            si.Title LIKE '%@SearchTerm%'
				    		OR luIT.ItemType LIKE '%@SearchTerm%'
                            )
                    )

                SELECT
                    *
                FROM
                    #temp
                ORDER BY
                    CASE WHEN @OrderBy = 'Title' AND @IsAscending = 1 THEN Title END ASC,
                    CASE WHEN @OrderBy = 'Title' AND @IsAscending <> 1 THEN Title END DESC,
                    CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending = 1 THEN CreateDate END ASC,
                    CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending <> 1 THEN CreateDate END DESC,
                    CASE WHEN @OrderBy = 'ItemType' AND @IsAscending = 1 THEN ActualItemType END ASC,
                    CASE WHEN @OrderBy = 'ItemType' AND @IsAscending <> 1 THEN ActualItemType END DESC,
				    CASE WHEN @OrderBy = 'IsApproved' AND @IsAscending = 1 THEN IsApproved END ASC,
                    CASE WHEN @OrderBy = 'IsApproved' AND @IsAscending <> 1 THEN IsApproved END DESC,
				    CASE WHEN @OrderBy = 'IsReviewed' AND @IsAscending = 1 THEN IsReviewed END ASC,
				    CASE WHEN @OrderBy = 'IsReviewed' AND @IsAscending <> 1 THEN IsReviewed END DESC
                OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                FOR JSON AUTO
        """

        sql = pagination.replaceParams(sql)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            items = c.fetchall()

            items = SQL.get_total_records(items, conn)

            c.close()
            conn.close()

            return items
        except pymssql.Error as e:
            print('Error getting submitted items. Error {}'.format(e))

    def get_submitted_item_by_id(id):
        sql = "SELECT si.Title, si.CreateDate, 'Blank' as ItemType, luIT.ItemType, si.ItemText, si.ServerId, si.DiscordUserId FROM SubmittedItems si WITH (NOLOCK) JOIN CodeItemType luIT WITH (NOLOCK) ON si.ItemTypeId = luIT.Id WHERE si.Id = @id FOR JSON AUTO"
        sql = sql.replace("@id", id)

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

    def get_all_stories(pagination):
        sql = """
            DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
            DECLARE @IsAscending BIT = @Ascending

            SELECT
                Id,
                Title,
			    Story,
			    IsActive
            INTO #temp
            FROM
                Stories WITH (NOLOCK)
            WHERE
                ('@SearchTerm' = ''
                    OR (
                        Title LIKE '%@SearchTerm%'
                        )
                )

            SELECT
                *
            FROM
                #temp
            ORDER BY
                CASE WHEN @OrderBy = 'Title' AND @IsAscending = 1 THEN Title END ASC,
                CASE WHEN @OrderBy = 'Title' AND @IsAscending <> 1 THEN Title END DESC,
                CASE WHEN @OrderBy = 'Story' AND @IsAscending = 1 THEN Story END ASC,
                CASE WHEN @OrderBy = 'Story' AND @IsAscending <> 1 THEN Story END DESC,
				CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC
            OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
            FOR JSON AUTO
        """

        sql = pagination.replaceParams(sql)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            stories = c.fetchall()

            stories = SQL.get_total_records(stories, conn)

            c.close()
            conn.close()

            return stories
        except pymssql.Error as e:
            print("Error getting stories. Error {}".format(e))
            return None

    def get_story_by_id(id):
        sql = "SELECT s.Id, s.Title, s.Story, luS.ServerId, s.IsActive FROM Stories s WITH (NOLOCK) JOIN CodeServers luS WITH (NOLOCK) ON s.ServerId = luS.Id WHERE s.Id = @id FOR JSON AUTO"

        sql = sql.replace("@id", str(id))

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
        sql = "UPDATE Stories SET Title = '@title', Story = '@story', IsActive = @isActive, ServerId = @serverId, UpdateDate = '@date' WHERE Id = @Id"
        server = "SELECT Id FROM CodeServers WHERE ServerId = @serverId"
        current_date = datetime.now()

        title = story[1]
        storyVal = story[2]

        title = title.replace("'", "''")
        storyVal = storyVal.replace("'", "''")

        sql = sql.replace("@title", title)
        sql = sql.replace("@story", storyVal)
        server = server.replace("@serverId", str(story[3]))
        sql = sql.replace("@isActive", Helpers.bool_to_int(story[4]))
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        sql = sql.replace("@Id", str(story[0]))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            #Check to see if server passed from site exists in CodeServers
            c.execute(server)
            serverId = c.fetchone()

             #If it does set serverId to the current server
            if serverId:
                serverId = serverId[0]
                sql = sql.replace("@serverId", str(serverId))
            else:
                #Else, check if new server exists and is associated to the story account id
                canContinue = False

                getCurrentServerAccountId = "SELECT AccountId FROM CodeServers WHERE Id = (SELECT ServerId FROM Stories WHERE Id = @id)"
                getCurrentServerAccountId = getCurrentServerAccountId.replace("@id", str(story[0]))

                c.execute(getCurrentServerAccountId)
                accountId = c.fetchone()[0]

                checkForExistingServer = "SELECT Id FROM CodeServers WHERE ServerId = '@serverId'"
                checkForExistingServer = checkForExistingServer.replace("@serverId", str(story[3]))
                
                c.execute(checkForExistingServer)
                existingServerId = c.fetchone()
                
                if existingServerId:
                    linkedToAccount = "SELECT 1 FROM CodeServers WHERE Id = @id AND AccountId = @accountId"
                    linkedToAccount = linkedToAccount.replace("@id", existingServerId[0])
                    linkedToAccount = linkedToAccount.replace("@accountId", accountId)

                    c.execute(linkedToAccount)
                    isLinked = c.fetchone()[0]

                    if isLinked:
                        canContinue = True
                else:
                    canContinue = True

                #If the server is linked to the story account or does not exist, then continue, else return false
                if canContinue:
                    insert_new_server = "INSERT INTO CodeServers (ServerId, Nickname, AccountId) VALUES ('@newServer', '@name', @accountId); SELECT CAST(scope_identity() as int)"
                    insert_new_server = insert_new_server.replace("@newServer", str(story[3]))
                    insert_new_server = insert_new_server.replace("@name", "Server created Story - {}".format(current_date.strftime('%Y-%m-%d %H:%M:%S')))
                    insert_new_server = insert_new_server.replace("@accountId", str(accountId))

                    c.execute(insert_new_server)
                    serverId = c.fetchone()[0]
                    conn.commit()

                    sql = sql.replace("@serverId", str(serverId))
                else:
                    return False

            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()
            
            return True
        except pymssql.Error as e:
            print("Error updating story. Error {}".format(e))
            return False

    def get_all_wisdoms(pagination):
        sql = """
                DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                DECLARE @IsAscending BIT = @Ascending

                SELECT
                    Id,
                    Wisdom,
				    IsActive
                INTO #temp
                FROM
                    Wisdoms WITH (NOLOCK)
                WHERE
                    ('@SearchTerm' = ''
                        OR (
                            Wisdom LIKE '%@SearchTerm%'
                            )
                    )

                SELECT
                    *
                FROM
                    #temp
                ORDER BY
                    CASE WHEN @OrderBy = 'Wisdom' AND @IsAscending = 1 THEN Wisdom END ASC,
                    CASE WHEN @OrderBy = 'Wisdom' AND @IsAscending <> 1 THEN Wisdom END DESC,
					CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                    CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC
                OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                FOR JSON AUTO
        """

        sql = pagination.replaceParams(sql);

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            stories = c.fetchall()

            stories = SQL.get_total_records(stories, conn)

            c.close()
            conn.close()

            return stories
        except pymssql.Error as e:
            print("Error getting stories. Error {}".format(e))
            return None

    def get_wisdom_by_id(id):
        sql = "SELECT w.Id, w.Wisdom, luS.ServerId, w.IsActive FROM Wisdoms w WITH (NOLOCK) JOIN CodeServers luS WITH (NOLOCK) ON w.ServerId = luS.Id WHERE w.Id = @id FOR JSON AUTO"

        sql = sql.replace("@id", str(id))

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
        sql = "UPDATE Wisdoms SET Wisdom = '@wisdom', IsActive = @isActive, UpdateDate = '@date', ServerId = @serverId WHERE Id = @Id"
        server = "SELECT Id FROM CodeServers WHERE ServerId = @serverId"
        current_date = datetime.now()

        wisdomVal = wisdom[1]
        wisdomVal = wisdomVal.replace("'", "''")

        sql = sql.replace("@wisdom", wisdomVal)
        server = server.replace("@serverId", str(wisdom[2]))
        sql = sql.replace("@isActive", Helpers.bool_to_int(wisdom[3]))
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        sql = sql.replace("@Id", str(wisdom[0]))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()
            
            #Check to see if server passed from site exists in CodeServers
            c.execute(server)
            serverId = c.fetchone()

            #If it does set serverId to the current server
            if serverId:
                serverId = serverId[0]
                sql = sql.replace("@serverId", str(serverId))
            else:
                #Else, check if new server exists and is associated to the wisdom account id
                canContinue = False

                getCurrentServerAccountId = "SELECT AccountId FROM CodeServers WHERE Id = (SELECT ServerId FROM Wisdoms WHERE Id = @id)"
                getCurrentServerAccountId = getCurrentServerAccountId.replace("@id", str(wisdom[0]))

                c.execute(getCurrentServerAccountId)
                accountId = c.fetchone()[0]

                checkForExistingServer = "SELECT Id FROM CodeServers WHERE ServerId = '@serverId'"
                checkForExistingServer = checkForExistingServer.replace("@serverId", str(wisdom[2]))
                
                c.execute(checkForExistingServer)
                existingServerId = c.fetchone()
                
                if existingServerId:
                    linkedToAccount = "SELECT 1 FROM CodeServers WHERE Id = @id AND AccountId = @accountId"
                    linkedToAccount = linkedToAccount.replace("@id", existingServerId[0])
                    linkedToAccount = linkedToAccount.replace("@accountId", accountId)

                    c.execute(linkedToAccount)
                    isLinked = c.fetchone()[0]

                    if isLinked:
                        canContinue = True
                else:
                    canContinue = True

                #If the server is linked to the wisdom account or does not exist, then continue, else return false
                if canContinue:
                    insert_new_server = "INSERT INTO CodeServers (ServerId, Nickname, AccountId) VALUES ('@newServer', '@name', @accountId); SELECT CAST(scope_identity() as int)"
                    insert_new_server = insert_new_server.replace("@newServer", str(wisdom[2]))
                    insert_new_server = insert_new_server.replace("@name", "Server created Wisdom - {}".format(current_date.strftime('%Y-%m-%d %H:%M:%S')))
                    insert_new_server = insert_new_server.replace("@accountId", str(accountId))

                    c.execute(insert_new_server)
                    serverId = c.fetchone()[0]
                    conn.commit()

                    sql = sql.replace("@serverId", str(serverId))
                else:
                    return False

            #Execute update wisdom command and save changes. Return true if successful
            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()
            
            return True
        except pymssql.Error as e:
            print("Error updating wisdom. Error {}".format(e))
            return False

    def get_form_by_form_key(formKey):
        sql = "SELECT Fields.FormKey, Fields.FieldSchema, Fields.ActionLink, Fields.IsActive, Form.FormName, Form.ShowFormName FROM VueFormFields Fields WITH (NOLOCK) JOIN CodeVueForms Form WITH (NOLOCK) ON Fields.FormKey = Form.FormKey WHERE Fields.FormKey = '@formKey' FOR JSON AUTO"

        sql = sql.replace("@formKey", formKey)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            form = c.fetchone()

            c.close()
            conn.close()

            if form:
                form = form[0]
                return form
            else:
                return None
        except pymssql.Error as e:
            print("Error getting form by form key. Error {}".format(e))
            return None

    def update_form(form, userId):
        field = "UPDATE VueFormFields SET FieldSchema = '@schema', ActionLink = '@actionlink', IsActive = @isActive, UpdatedByUserId = '@userId', UpdateDate = '@date' WHERE FormKey = '@formKey'"
        formInfo = "UPDATE CodeVueForms SET FormName = '@formName', IsActive = @isActive WHERE FormKey = '@formKey'"
        current_date = datetime.now()

        schema = str(form[1])
        schema = schema.replace("'", '"')
        schema = schema.replace("True", "true")
        schema = schema.replace("False", "false")

        field = field.replace("@formKey", form[0])
        formInfo = formInfo.replace("@formKey", form[0])
        field = field.replace("@schema", schema)
        field = field.replace("@actionlink", form[2])
        field = field.replace("@isActive", Helpers.bool_to_int(form[3]))
        formInfo = formInfo.replace("@isActive", Helpers.bool_to_int(form[3]))
        field = field.replace("@userId", userId)
        field = field.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        formInfo = formInfo.replace("@formName", form[4])

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(field)
            conn.commit()

            c.execute(formInfo)
            conn.commit()

            c.close()
            conn.close()

            return True
        except pymssql.Error as e:
            print("Error updating form. Error {}".format(e))
            print("SQL")
            print(field)
            print(formInfo)
            return False

    def create_form(form, userId):
        field = "INSERT INTO VueFormFields (FormKey, FieldSchema, ActionLink, IsActive, UpdateDate, UpdatedByUserId) VALUES ('@formKey', '@schema', '@actionlink', @isActive, '@date', '@userId')"
        formInfo = "INSERT INTO CodeVueForms (FormKey, IsActive, FormName) VALUES ('@formKey', @isActive, '@formName')"
        current_date = datetime.now()

        schema = str(form[1])
        schema = schema.replace("'", '"')
        schema = schema.replace("True", "true")
        schema = schema.replace("False", "false")

        field = field.replace("@formKey", form[0])
        formInfo = formInfo.replace("@formKey", form[0])
        field = field.replace("@schema", schema)
        field = field.replace("@actionlink", form[2])
        field = field.replace("@isActive", Helpers.bool_to_int(form[3]))
        formInfo = formInfo.replace("@isActive", Helpers.bool_to_int(form[3]))
        field = field.replace("@userId", userId)
        field = field.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        formInfo = formInfo.replace("@formName", form[4])

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(field)
            conn.commit()

            c.execute(formInfo)
            conn.commit()

            c.close()
            conn.close()

            return True
        except pymssql.Error as e:
            print("Error updating form. Error {}".format(e))
            print("SQL")
            print(field)
            print(formInfo)
            return False

    def get_account_info_by_id(accountId):
        accountSql = "SELECT a.AccountId, a.AccountName, a.CreateDate, a.IsActive FROM Accounts a WITH (NOLOCK) WHERE a.AccountId = @accountId FOR JSON AUTO"

        accountSql = accountSql.replace("@accountId", str(accountId))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(accountSql)
            accounts = c.fetchall()

            c.close()
            conn.close()

            return accounts
        except pymssql.Error as e:
            print("Error getting account information. Error {}".format(e))
            return None

    def get_account_users(accountId, isMaster, pagination):
        usersSql = ""
        if isMaster == "true":
            usersSql = """
                        DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                        DECLARE @IsAscending BIT = @Ascending

                        SELECT
                                Id,
                                Username,
					    		FirstName,
					    		LastName,
					    		IsLocked,
					    		IsActive,
					    		CreateDate
                        INTO #temp
                        FROM
                            Users WITH (NOLOCK)
                        WHERE
                            ('@SearchTerm' = ''
                                OR (
                                    Username LIKE '%@SearchTerm%'
					    			OR FirstName LIKE '%@SearchTerm%'
					    			OR LastName LIKE '%@SearchTerm%'
                                    )
                            )
                        
                        SELECT
                            *
                        FROM
                            #temp
                        ORDER BY
                            CASE WHEN @OrderBy = 'Username' AND @IsAscending = 1 THEN Username END ASC,
                            CASE WHEN @OrderBy = 'Username' AND @IsAscending <> 1 THEN Username END DESC,
					    	CASE WHEN @OrderBy = 'FirstName' AND @IsAscending = 1 THEN FirstName END ASC,
                            CASE WHEN @OrderBy = 'FirstName' AND @IsAscending <> 1 THEN FirstName END DESC,
					    	CASE WHEN @OrderBy = 'LastName' AND @IsAscending = 1 THEN LastName END ASC,
                            CASE WHEN @OrderBy = 'LastName' AND @IsAscending <> 1 THEN LastName END DESC,
					    	CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                            CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC,
					    	CASE WHEN @OrderBy = 'IsLocked' AND @IsAscending = 1 THEN IsLocked END ASC,
                            CASE WHEN @OrderBy = 'IsLocked' AND @IsAscending <> 1 THEN IsLocked END DESC,
					    	CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending = 1 THEN CreateDate END ASC,
                            CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending <> 1 THEN CreateDate END DESC
                        OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                        FOR JSON AUTO
            """
        else:
            usersSql = """
                        DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                        DECLARE @IsAscending BIT = @Ascending

                        SELECT
                                Id,
                                Username,
					    		FirstName,
					    		LastName,
					    		IsLocked,
					    		IsActive,
					    		CreateDate
                        INTO #temp
                        FROM
                            Users WITH (NOLOCK)
                        WHERE
					    	Id <> '2F5FA286-5644-4AB1-B04F-D2ED451EF33F'
                            AND ('@SearchTerm' = ''
                                OR (
                                    Username LIKE '%@SearchTerm%'
					    			OR FirstName LIKE '%@SearchTerm%'
					    			OR LastName LIKE '%@SearchTerm%'
                                    )
                            )

                        SELECT
                            *
                        FROM
                            #temp
                        ORDER BY
                            CASE WHEN @OrderBy = 'Username' AND @IsAscending = 1 THEN Username END ASC,
                            CASE WHEN @OrderBy = 'Username' AND @IsAscending <> 1 THEN Username END DESC,
					    	CASE WHEN @OrderBy = 'FirstName' AND @IsAscending = 1 THEN FirstName END ASC,
                            CASE WHEN @OrderBy = 'FirstName' AND @IsAscending <> 1 THEN FirstName END DESC,
					    	CASE WHEN @OrderBy = 'LastName' AND @IsAscending = 1 THEN LastName END ASC,
                            CASE WHEN @OrderBy = 'LastName' AND @IsAscending <> 1 THEN LastName END DESC,
					    	CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                            CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC,
					    	CASE WHEN @OrderBy = 'IsLocked' AND @IsAscending = 1 THEN IsLocked END ASC,
                            CASE WHEN @OrderBy = 'IsLocked' AND @IsAscending <> 1 THEN IsLocked END DESC,
					    	CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending = 1 THEN CreateDate END ASC,
                            CASE WHEN @OrderBy = 'CreateDate' AND @IsAscending <> 1 THEN CreateDate END DESC
                        OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                        FOR JSON AUTO
            """

        usersSql = usersSql.replace("@accountId", str(accountId))
        usersSql = pagination.replaceParams(usersSql);

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(usersSql)
            accounts = c.fetchall()

            users = SQL.get_total_records(accounts, conn)

            c.close()
            conn.close()

            return users
        except pymssql.Error as e:
            print("Error getting account information. Error {}".format(e))
            return None

    def update_account(account):
        sql = "UPDATE Accounts SET AccountName = '@name', IsActive = @isActive WHERE AccountId = @accountId"

        sql = sql.replace("@name", account[1])
        sql = sql.replace("@isActive", Helpers.bool_to_int(account[3]))
        sql = sql.replace("@accountId", str(account[0]))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            conn.commit()

            c.close()
            conn.close()

            return SQL.get_account_info_by_id(account[0])
        except pymssql.Error as e:
            print("Error updating account. Error {}".format(e))
            return None

    def get_documentation(helpContentKey, isAdmin):
        sql = ''
        if isAdmin:
            sql = "SELECT HelpTitle, HelpContent, IsActive FROM HelpDocumentation WITH (NOLOCK) WHERE HelpContentKey = '@key' FOR JSON AUTO"
        else:
            sql = "SELECT HelpTitle, HelpContent, IsActive FROM HelpDocumentation WITH (NOLOCK) WHERE IsActive = 1 AND HelpContentKey = '@key' FOR JSON AUTO"
        sql = sql.replace("@key", helpContentKey)

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            content = c.fetchone()

            if content:
                content = content[0]
            else:
                content = None

            c.close()
            conn.close()

            return content
        except pymssql.Error as e:
            print("Error getting documentation. Error {}".format(e))
            return None

    def get_all_documentation(pagination):
        sql = """ 
                DECLARE @OrderBy NVARCHAR(255) = '@SortColumn'
                DECLARE @IsAscending BIT = @Ascending

                SELECT
                        HelpContentKey,
                        HelpTitle,
                        HelpContent,
                        IsActive
                INTO #temp
                FROM
                    HelpDocumentation WITH (NOLOCK)
                WHERE
                    ('@SearchTerm' = ''
                        OR (
                            HelpTitle LIKE '%' + '@SearchTerm' + '%'
                            )
                    )

                SELECT
                    *
                FROM
                    #temp
                ORDER BY
                    CASE WHEN @OrderBy = 'HelpContentKey' AND @IsAscending = 1 THEN HelpContentKey END ASC,
                    CASE WHEN @OrderBy = 'HelpContentKey' AND @IsAscending <> 1 THEN HelpContentKey END DESC,
                    CASE WHEN @OrderBy = 'HelpTitle' AND @IsAscending = 1 THEN HelpTitle END ASC,
                    CASE WHEN @OrderBy = 'HelpTitle' AND @IsAscending <> 1 THEN HelpTitle END DESC,
                    CASE WHEN @OrderBy = 'HelpContent' AND @IsAscending = 1 THEN HelpContent END ASC,
                    CASE WHEN @OrderBy = 'HelpContent' AND @IsAscending <> 1 THEN HelpContent END DESC,
                    CASE WHEN @OrderBy = 'IsActive' AND @IsAscending = 1 THEN IsActive END ASC,
                    CASE WHEN @OrderBy = 'IsActive' AND @IsAscending <> 1 THEN IsActive END DESC
                OFFSET ((@CurrentPage-1) * @MaxRows) ROWS FETCH NEXT @MaxRows ROWS ONLY
                FOR JSON AUTO
            """

        sql = pagination.replaceParams(sql);
        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)

            content = c.fetchall()

            content = SQL.get_total_records(content, conn)

            c.close()
            conn.close()

            return content
        except pymssql.Error as e:
            print("Error getting documentation. Error {}".format(e))
            return None

    def update_documentation(documentation):
        sql = "UPDATE HelpDocumentation SET HelpTitle = '@title', HelpContent = '@content', IsActive = @isActive, UpdateDate = '@date', UpdateByUserId = '@userId' WHERE HelpContentKey = '@key'"
        current_date = datetime.now()
        content = documentation[2]
        content = content.replace("'", "''")
        sql = sql.replace("@title", documentation[1])
        sql = sql.replace("@content", content)
        sql = sql.replace("@isActive", Helpers.bool_to_int(documentation[3]))
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))
        sql = sql.replace("@userId", documentation[4])
        sql = sql.replace("@key", documentation[0])

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            conn.commit()

            c.close()
            conn.close()

            content = SQL.get_documentation(documentation[0], documentation[5])

            return content
        except pymssql.Error as e:
            print("Error updating documentation. Error {}".format(e))
            return None

    def get_servers_by_account(accountId):
        sql = ''
        if str(accountId) == "1":
            sql = "SELECT Id, ServerId, AccountId, Nickname, DailyWisdom, WeeklyStory, UpdateDate FROM CodeServers WITH (NOLOCK) FOR JSON AUTO"
        else:
            sql = "SELECT Id, ServerId, AccountId, Nickname, DailyWisdom, WeeklyStory, UpdateDate FROM CodeServers WITH (NOLOCK) WHERE AccountId = @accountId FOR JSON AUTO"
            sql = sql.replace("@accountId", str(accountId))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            servers = c.fetchall()

            c.close()
            conn.close()
            return servers
        except pymssql.Error as e:
            print("Error getting the discord servers by account. Error {}".format(e))
            return None

    def get_server_by_id(id):
        sql = "SELECT Id, ServerId, AccountId, Nickname, DailyWisdom, WeeklyStory, UpdateDate FROM CodeServers WITH (NOLOCK) WHERE Id = @id FOR JSON AUTO"
        sql = sql.replace("@id", str(id));

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            server = c.fetchone()[0]

            c.close()
            conn.close()
            return server
        except pymssql.Error as e:
            print("Error getting server by id. Error {}".format(e))
            return None

    def update_server(server):
        sql = ''
        if str(server[0]) != "0":
            sql = "UPDATE CodeServers SET ServerId = '@serverId', AccountId = @accountId, Nickname = '@nickname', DailyWisdom = @dailyWisdom, WeeklyStory = @weeklyStory, UpdateDate = '@date' WHERE Id = @id"
        else:
            sql = "INSERT INTO CodeServers (ServerId, AccountId, Nickname, DailyWisdom, WeeklyStory, UpdateDate) VALUES ('@serverId', @accountId, '@nickname', @dailyWisdom, @weeklyStory, '@date')"
        
        current_date = datetime.now()
        sql = sql.replace("@serverId", str(server[1]))
        sql = sql.replace("@accountId", str(server[2]))
        sql = sql.replace("@nickname", server[3])
        sql = sql.replace("@dailyWisdom", Helpers.bool_to_int(server[4]))
        sql = sql.replace("@weeklyStory", Helpers.bool_to_int(server[5]))
        sql = sql.replace("@date", current_date.strftime('%Y-%m-%d %H:%M:%S'))

        if str(server[0]) != "0":
            sql = sql.replace("@id", str(server[0]))

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            conn.commit()

            c.close()
            conn.close()

            return True
        except pymssql.Error as e:
            print("Error updating server. Error {}".format(e))
            return False

    def update_user_password(changePasswordModel):
        sql = "UPDATE Users SET PasswordHash = '@password' WHERE Id = '@id'"

        password = Cryptography.hashPassword(changePasswordModel[1])
        sql = sql.replace("@id", changePasswordModel[0])
        sql = sql.replace("@password", password.decode())

        try:
            conn = SQL.open_connection()
            c = conn.cursor()

            c.execute(sql)
            conn.commit()

            c.close()
            conn.close()

            return True
        except pymssql.Error as e:
            print("Error updating password! Error {}".format(e))
            return False