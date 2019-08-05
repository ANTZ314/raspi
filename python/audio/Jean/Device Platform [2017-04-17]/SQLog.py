# -*- coding: utf-8 -*-
#
#Created on Mon Mar 13 11:36:27 2017
#
#@author: Jean Louw

#-------------------------------------IMPORTS----------------------------------
import sqlite3
import threading
#------------------------------------------------------------------------------

#--------------------------------SQLOG CLASS START-----------------------------
class SQLog(object):
    
    #-------------------------------------------------------------------------#
    # Name: SQLog                                                             #
    # Function: Contains methods with which to log and retrieve the gunshot   #
    #           application data into and from a SQLite database.             #
    # Dependencies: SQLite3 (comes pre-installed with Python)                 #
    #-------------------------------------------------------------------------#
    
    __version__ = "2017.3"
    
#- - - - - - - - - - - - - - COMMON DATABASE FUNCTIONS- - - - - - - - - - - - -
    
    #<summary> Constructor checks for existing db or creates new one     </summary>
    #<param> Receives name/path of database to be used as filename = STRING</param>
    def __init__(self, **kwargs):
        self.data = kwargs
        self.sql_thread_lock = threading.Lock()
        filename = self.data.get('filename', None)
        if filename != None: self.connect_to_DB(filename)
        else: self.connect_to_DB("gunshot_db.db")
        
    #<summary> Closing function to be called before deleting the class instance. </summary> 
    def close(self):
        self._db.close()
        
    #<summary> Generator function for fetching all tables in a database file </summary>
    #<retuns> The string name of each table in the database sequentially     </returns>    
    def list_tables(self):
        list_of_tables = self.sql_do("SELECT tbl_name AS 'Table:' FROM sqlite_master WHERE type='table';")
        for table in list_of_tables:
            yield table[0]
    
    #<summary> Helper function for performing and commiting change actions in the database  </summary>
    #<param name="sql_string"> This is the SQL format string that is to be executed by the db </param>
    def sql_do(self, sql_string):
        with self.sql_thread_lock:
            res = self._db.execute(sql_string)
            self._db.commit() # to commit is to save the change in the db
            return res

    #<summary>Conects to the .db file in the filename path and looks for essential tables.
    #         If the tables are not found it re-directs to create the tables                </summary>
    #<param name="filename"> filename is a mandatory STRING and houses the database file path </param>
    def connect_to_DB(self, filename):
        self._db = sqlite3.connect(filename, check_same_thread = False)
        self._db.row_factory = sqlite3.Row
        if 'Event_Log' not in self.list_tables(): self.create_Event_Log_table()
        if 'Status_Log' not in self.list_tables(): self.create_Status_Log_table()
        if 'Error_Log' not in self.list_tables(): self.create_Error_Log_table()
        if 'Update_Log' not in self.list_tables(): self.create_Update_Log_table()
        
    def set_thread_lock(self,sql_lock):
        self.sql_thread_lock = sql_lock
    
    def get_thread_lock(self):
        return self.api_thread_lock
        
#- - - - - - - - - - - - - TABLE SPECIFIC FUNCTIONS - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - -  EVENT LOG TABLE - - - - - - - - - - - - - - - -   
    
    #<summary> Creates a brand new table in the connected db with the name "Event_Log" </summary>
    def create_Event_Log_table(self):
        print("No event log found. Creating Event_Log table.")
        self.sql_do('DROP TABLE IF EXISTS Event_Log')#this is to ensure no duplicates if possible
        self.sql_do('''CREATE TABLE Event_Log ( event_id INTEGER PRIMARY KEY NOT NULL, 
                                                gunshot_event STRING, 
                                                filepath STRING, 
                                                api_response INTEGER DEFAULT 0 );''')
    
    #<summary>Generator that returns all of the records of the Event_Log table</summary>
    #<returns>Returns a dictionary with the current record's information      </returns>    
    def fetch_all_from_Event_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Event_Log')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Generator that returns all of the records of the Event_Log table 
    #         whose api repsonse is not equal to 201 (success)          </summary>
    #<returns>Returns a dictionary with the current record's information</returns>          
    def fetch_unsent_from_Event_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Event_Log WHERE api_response != 201')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Fetches the information of a specific Event_Log record by its event_id  </summary>
    #<param name="event_id">An INTEGER that identifies the record to be fetched       </param>
    #<returns>A dictionary item with the record's information if it exists, else None </returns>
    def fetch_row_from_Event_Log_table(self, event_id):
        sql_string = 'SELECT * FROM Event_Log WHERE event_id = {}'.format(event_id)
        rowdata = self.sql_do(sql_string)
        rowdata = rowdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if rowdata!= None: return dict(rowdata)
        else: return rowdata #return None if the result is empty
    
    #<summary> Fetches the information of the last record in Event_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>   
    def fetch_last_from_Event_Log_table(self):
        lastdata = self.sql_do('SELECT * FROM Event_Log ORDER BY event_id DESC LIMIT 1;')
        lastdata = lastdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if lastdata != None: return dict(lastdata)
        else: return lastdata #return None if the result is empty
    
    #<summary>Updates a specific column of a specific record in Event_Log with
    #         a specific value, and saves the changes.                           </summary>
    #<param name="event_id"> An INTEGER that identifies the record to be updated </param>
    #<param name="key"> A STRING name value of the column to update              </param>
    #<param name="value"> The value of any accepted type to be the updated value </param>
    def update_Event_Log_table(self, event_id, key, value):
        #if the value passed is a string, it should be encapsulated in quotes before execution.
        if isinstance(value, basestring): sql_string = "UPDATE Event_Log SET {0} = '{1}' where event_id = {2}".format(key, value, event_id)
        else: sql_string = 'UPDATE Event_Log SET {0} = {1} where event_id = {2}'.format(key, value, event_id)
        self.sql_do(sql_string)
    
    # <summary> Inserts a single record into the Event_Log table</summary>
    # <param name="**kwargs"> Receives coinciding parameters to the table column names: 
    #  event_data = json parsed string or dictionary object to be parsed of all the event data
    #  event_file_location = a string showing the cross-platform location of the event sound clip file
    #  api_response (optional) = the returned integer value from the attempt to upload to the API endpoint
    # </param>
    # <returns> Returns the SQL string that was processed. </returns>
    def insert_Event_Log_table(self, insert_data):
        acceptable_data = ('gunshot_event', 'filepath', 'api_response')
        value_names = "INSERT INTO Event_Log ( "
        value_data = " ) VALUES ( "
        #create two strings for the dictionary and its values
        for column in insert_data:
            if column in acceptable_data:
                value_names += column + ","
                #if the value passed into column is of string type, encapsulate in quotes for SQL processing
                if isinstance(insert_data[column], basestring): value_data +=  "'" + insert_data[column] + "',"
                else: value_data +=  str(insert_data[column]) + "," #else pass the value directly
        #combine the two strings
        value_names = value_names[:-1] #trim the last ','
        value_data = value_data[:-1] #trim the last ','
        sql_string = value_names + value_data + " );"
        #pass the string to be processed    
        self.sql_do(sql_string)
        return sql_string
    
#- - - - - - - - - - - - - - - STATUS LOG TABLE - - - - - - - - - - - - - - - -   
    
    #<summary> Creates a brand new table in the connected db with the name "Status_Log" </summary>
    def create_Status_Log_table(self):
        print("No status log found. Creating Status_Log table.")
        self.sql_do('DROP TABLE IF EXISTS Status_Log')#this is to ensure no duplicates if possible
        self.sql_do('''CREATE TABLE Status_Log ( event_id INTEGER PRIMARY KEY NOT NULL, 
                                                 dts STRING, 
                                                 gps_status INTEGER, 
                                                 gps_signal INTEGER, 
                                                 status_3g INTEGER, 
                                                 signal_3g INTEGER, 
                                                 mic_status INTEGER, 
                                                 snr STRING, 
                                                 battery_status STRING, 
                                                 cover_status INTEGER,
                                                 api_response INTEGER DEFAULT 0);''')
    
    #<summary>Generator that returns all of the records of the Status_Log table</summary>
    #<returns>Returns a dictionary with the current record's information       </returns>    
    def fetch_all_from_Status_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Status_Log')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Generator that returns all of the records of the Status_Log table 
    #         whose api repsonse is not equal to 201 (success)          </summary>
    #<returns>Returns a dictionary with the current record's information</returns>          
    def fetch_unsent_from_Status_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Status_Log WHERE api_response != 201')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Fetches the information of a specific Status_Log record by its event_id </summary>
    #<param name="event_id">An INTEGER that identifies the record to be fetched       </param>
    #<returns>A dictionary item with the record's information if it exists, else None </returns>
    def fetch_row_from_Status_Log_table(self, event_id):
        sql_string = 'SELECT * FROM Status_Log WHERE event_id = {}'.format(event_id)
        rowdata = self.sql_do(sql_string)
        rowdata = rowdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if rowdata!= None: return dict(rowdata)
        else: return rowdata #return None if the result is empty
    
    #<summary> Fetches the information of the last record in Status_Log                </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>   
    def fetch_last_from_Status_Log_table(self):
        lastdata = self.sql_do('SELECT * FROM Status_Log ORDER BY event_id DESC LIMIT 1;')
        lastdata = lastdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if lastdata != None: return dict(lastdata)
        else: return lastdata #return None if the result is empty
    
    #<summary>Updates a specific column of a specific record in Status_Log with
    #         a specific value, and saves the changes.                           </summary>
    #<param name="event_id"> An INTEGER that identifies the record to be updated </param>
    #<param name="key"> A STRING name value of the column to update              </param>
    #<param name="value"> The value of any accepted type to be the updated value </param>
    def update_Status_Log_table(self, event_id, key, value):
        #if the value passed is a string, it should be encapsulated in quotes before execution.
        if isinstance(value, basestring): sql_string = "UPDATE Status_Log SET {0} = '{1}' where event_id = {2}".format(key, value, event_id)
        else: sql_string = 'UPDATE Status_Log SET {0} = {1} where event_id = {2}'.format(key, value, event_id)
        self.sql_do(sql_string)
    
    # <summary> Inserts a single record into the Status_Log table</summary>
    # <param name="**kwargs"> Receives coinciding parameters to the table column names: 
    #   status_log_date_time = STRING that states when the data was logged and relevant
    #   gps_status = BOOLEAN INTEGER indicating working (1) or not (0) 
    #   gps_signal = INTEGER that houses the signal strenght value
    #   net_3g_status  = BOOLEAN INTEGER indicating working (1) or not (0) 
    #   net_3g_signal = INTEGER that houses the signal strenght value
    #   microphone_status = BOOLEAN INTEGER indicating working (1) or not (0) 
    #   signal_to_noise_ratio = STRING that is the passed float ratio value
    #   power_status = STRING indicating if empty, charging or full or AC powered
    #   cover_status = BOOLEAN INTEGER indication open (0) or covered (1)
    #   api_response (optional) = the returned integer value from the attempt to upload to the API endpoint
    # </param>
    # <returns> Returns the SQL string that was processed. </returns>
    def insert_Status_Log_table(self, insert_data):
        acceptable_data = ('dts', 'gps_status', 'gps_signal', 
                           'status_3g', 'signal_3g', 'mic_status', 
                           'snr', 'battery_status', 'cover_status',
                           'api_response')
        value_names = "INSERT INTO Status_Log ( "
        value_data = " ) VALUES ( "
        #create two strings for the dictionary and its values
        for column in insert_data:
            if column in acceptable_data:
                value_names += column + ","
                #if the value passed into column is of string type, encapsulate in quotes for SQL processing
                if isinstance(insert_data[column], basestring): value_data +=  "'" + insert_data[column] + "',"
                else: value_data +=  str(insert_data[column]) + "," #else pass the value directly
        #combine the two strings
        value_names = value_names[:-1] #trim the last ','
        value_data = value_data[:-1] #trim the last ','
        sql_string = value_names + value_data + " );"
        #pass the string to be processed    
        self.sql_do(sql_string)
        return sql_string
    
#- - - - - - - - - - - - - - - ERROR LOG TABLE - - - - - - - - - - - - - - - -   
    
    #<summary> Creates a brand new table in the connected db with the name "Error_Log" </summary>
    def create_Error_Log_table(self):
        print("No error log found. Creating Error_Log table.")
        self.sql_do('DROP TABLE IF EXISTS Error_Log')
        self.sql_do('''CREATE TABLE Error_Log ( event_id INTEGER PRIMARY KEY NOT NULL, 
                                                error_details STRING, 
                                                error_date_time STRING, 
                                                api_response INTEGER DEFAULT 0);''')
        
    
    #<summary>Generator that returns all of the records of the Error_Log table</summary>
    #<returns>Returns a dictionary with the current record's information</returns>    
    def fetch_all_from_Error_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Error_Log')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Generator that returns all of the records of the Error_Log table 
    #         whose api repsonse is not equal to 201 (success)          </summary>
    #<returns>Returns a dictionary with the current record's information</returns>          
    def fetch_unsent_from_Error_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Error_Log WHERE api_response != 201')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Fetches the information of a specific Error_Log record by its event_id  </summary>
    #<param name="event_id">An INTEGER that identifies the record to be fetched       </param>
    #<returns>A dictionary item with the record's information if it exists, else None </returns>
    def fetch_row_from_Error_Log_table(self, event_id):
        sql_string = 'SELECT * FROM Error_Log WHERE event_id = {}'.format(event_id)
        rowdata = self.sql_do(sql_string)
        rowdata = rowdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if rowdata!= None: return dict(rowdata)
        else: return rowdata #return None if the result is empty
    
    #<summary> Fetches the information of the last record in Error_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>   
    def fetch_last_from_Error_Log_table(self):
        lastdata = self.sql_do('SELECT * FROM Error_Log ORDER BY event_id DESC LIMIT 1;')
        lastdata = lastdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if lastdata != None: return dict(lastdata)
        else: return lastdata #return None if the result is empty
    
    #<summary>Updates a specific column of a specific record in Error_Log with
    #         a specific value, and saves the changes.                           </summary>
    #<param name="event_id"> An INTEGER that identifies the record to be updated </param>
    #<param name="key"> A STRING name value of the column to update              </param>
    #<param name="value"> The value of any accepted type to be the updated value </param>
    def update_Error_Log_table(self, event_id, key, value):
        #if the value passed is a string, it should be encapsulated in quotes before execution.
        if isinstance(value, basestring): sql_string = "UPDATE Error_Log SET {0} = '{1}' where event_id = {2}".format(key, value, event_id)
        else: sql_string = 'UPDATE Error_Log SET {0} = {1} where event_id = {2}'.format(key, value, event_id)
        self.sql_do(sql_string)
    
    # <summary> Inserts a single record into the Error_Log table</summary>
    # <param name="**kwargs"> Receives coinciding parameters to the table column names: 
    #  error_description = STRING with all of the error info.
    #  error_date_time = a string with the time and date of the error occuring
    #  api_response (optional) = the returned integer value from the attempt to upload to the API endpoint
    # </param>
    # <returns> Returns the SQL string that was processed. </returns>
    def insert_Error_Log_table(self, insert_data):
        acceptable_data = ('error_details', 'error_date_time', 'api_response')
        value_names = "INSERT INTO Error_Log ( "
        value_data = " ) VALUES ( "
        #create two strings for the dictionary and its values
        for column in insert_data:
            if column in acceptable_data:
                value_names += column + ","
                #if the value passed into column is of string type, encapsulate in quotes for SQL processing
                if isinstance(insert_data[column], basestring): value_data +=  "'" + insert_data[column] + "',"
                else: value_data +=  str(insert_data[column]) + "," #else pass the value directly
        #combine the two strings
        value_names = value_names[:-1] #trim the last ','
        value_data = value_data[:-1] #trim the last ','
        sql_string = value_names + value_data + " );"
        #pass the string to be processed    
        self.sql_do(sql_string)
        return sql_string
        
    
#- - - - - - - - - - - - - - - UPDATE LOG TABLE - - - - - - - - - - - - - - - -   
    
    #<summary> Creates a brand new table in the connected db with the name "Update_Log" </summary>
    def create_Update_Log_table(self):
        print("No update log found. Creating Update_Log table.")
        self.sql_do('DROP TABLE IF EXISTS Update_Log')
        self.sql_do('''CREATE TABLE Update_Log ( event_id INTEGER PRIMARY KEY NOT NULL, 
                                                 updated_file_name STRING,
                                                 module_previous_version STRING,
                                                 module_version STRING, 
                                                 update_version STRING,
                                                 update_start_date_time STRING, 
                                                 update_stop_date_time STRING, 
                                                 update_status STRING, 
                                                 api_response INTEGER DEFAULT 0);''')
      
    
    #<summary>Generator that returns all of the records of the Update_Log table</summary>
    #<returns>Returns a dictionary with the current record's information</returns>    
    def fetch_all_from_Update_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Update_Log')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Generator that returns all of the records of the Update_Log table 
    #         whose api repsonse is not equal to 201 (success)          </summary>
    #<returns>Returns a dictionary with the current record's information</returns>          
    def fetch_unsent_from_Update_Log_table(self):
        alldata = self.sql_do('SELECT * FROM Update_Log WHERE api_response != 201')
        for record in alldata.fetchall():
            yield dict(record)
    
    #<summary>Fetches the information of a specific Update_Log record by its event_id  </summary>
    #<param name="event_id">An INTEGER that identifies the record to be fetched       </param>
    #<returns>A dictionary item with the record's information if it exists, else None </returns>
    def fetch_row_from_Update_Log_table(self, event_id):
        sql_string = 'SELECT * FROM Update_Log WHERE event_id = {}'.format(event_id)
        rowdata = self.sql_do(sql_string)
        rowdata = rowdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if rowdata!= None: return dict(rowdata)
        else: return rowdata #return None if the result is empty
    
    #<summary> Fetches the information of the last record in Update_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>   
    def fetch_last_from_Update_Log_table(self):
        lastdata = self.sql_do('SELECT * FROM Update_Log ORDER BY event_id DESC LIMIT 1;')
        lastdata = lastdata.fetchone()  #HINT: never run fetchone() twice, it returns a null value
        if lastdata != None: return dict(lastdata)
        else: return lastdata #return None if the result is empty
    
    #<summary>Updates a specific column of a specific record in Update_Log with
    #         a specific value, and saves the changes.                           </summary>
    #<param name="event_id"> An INTEGER that identifies the record to be updated </param>
    #<param name="key"> A STRING name value of the column to update              </param>
    #<param name="value"> The value of any accepted type to be the updated value </param>
    def update_Update_Log_table(self, event_id, key, value):
        #if the value passed is a string, it should be encapsulated in quotes before execution.
        if isinstance(value, basestring): sql_string = "UPDATE Update_Log SET {0} = '{1}' where event_id = {2}".format(key, value, event_id)
        else: sql_string = 'UPDATE Update_Log SET {0} = {1} where event_id = {2}'.format(key, value, event_id)
        self.sql_do(sql_string)
    
    # <summary> Inserts a single record into the Update_Log table</summary>
    # <param name="**kwargs"> Receives coinciding parameters to the table column names: 
    #   updated_file_name = the STRING name value of the file that was updated
    #   current_version = the STRING value of the class' original version
    #   update_version = the STRING value of the class' updated version
    #   update_start_date_time = STRING value of when the download started
    #   update_stop_date_time = STRING value of whent the download ended
    #   update_status = STRING stating if download has started, is busy or successful
    #   api_response = the returned integer value from the attempt to upload to the API endpoint
    # </param>
    # <returns> Returns the SQL string that was processed. </returns>
    def insert_Update_Log_table(self, insert_data):
        acceptable_data = ('updated_file_name', 'module_previous_version','module_version', 'update_version',
                           'update_start_date_time', 'update_stop_date_time',
                           'update_status', 'api_response')
        value_names = "INSERT INTO Event_Log ( "
        value_data = " ) VALUES ( "
        #create two strings for the dictionary and its values
        for column in insert_data:
            if column in acceptable_data:
                value_names += column + ","
                #if the value passed into column is of string type, encapsulate in quotes for SQL processing
                if isinstance(insert_data[column], basestring): value_data +=  "'" + insert_data[column] + "',"
                else: value_data +=  str(insert_data[column]) + "," #else pass the value directly
        #combine the two strings
        value_names = value_names[:-1] #trim the last ','
        value_data = value_data[:-1] #trim the last ','
        sql_string = value_names + value_data + " );"
        #pass the string to be processed    
        self.sql_do(sql_string)
        return sql_string
       
#- - - - - - - - - - - - - - - - - -DECORATORS- - - - - - - - - - - - - - - - -        
     
    #<summary> Exposes the information of the last record in Event_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>  
    @property
    def last_Event_entry(self):
        return self.fetch_last_from_Event_Log_table()
        
    #<summary> Exposes the information of the last record in Satus_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>  
    @property
    def last_Satus_entry(self):
        return self.fetch_last_from_Satus_Log_table()
        
    #<summary> Exposes the information of the last record in Error_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>  
    @property
    def last_Error_entry(self):
        return self.fetch_last_from_Error_Log_table()
        
    #<summary> Exposes the information of the last record in Update_Log                 </summary>
    #<returns> A dictionary item with the record's information if it exists, else None </returns>  
    @property
    def last_Update_entry(self):
        return self.fetch_last_from_Update_Log_table()
        
    @property
    def thread_lock(self):
        return self.get_thread_lock()
        
    @thread_lock.setter
    def thread_lock(self, sqlock):
        self.set_thread_lock(sqlock)

#---------------------------------SQLOG CLASS END------------------------------



#<summary>Test code for the class</summary>
def SQLogClassTestCode():
    
    #-----------------------------------------------------------#
    # Here I will only try to show the function of the Event_Log#
    # table in a test file of our own creation. Please note that#
    #    the same functions are available for all the tables.   #
    #-----------------------------------------------------------#
    # First we create an instance of the SQLog class within which we
    # create or connect to a database with a specific file name
    instance_of_SQLog = SQLog(filename = "bubblez.db")
    
    # Simply, we need to first create a dictionary that holds all the data
    event_information = {
                         "gunshot_event" : "JSON EVENT DATA",
                         "filepath" : "../SOUND_FILES/1.wav",
                         "api_response" : 202
                         }
    
    
    #create a new event entry
    instance_of_SQLog.insert_Event_Log_table(event_information)
                                             
    #the problem is that an event takes a JSON string as event_data
    #to achieve this, you merely import JSON as follows:
    import json
    #good. now we have the dictionary of values:
    gunshot_event_data = { 'gun' : 'bazooka',   #note how the squiggly bracket is how we make dictionaries
                       'shots_fired':100,
                       'screams_in_agony' : True
                      }    
    print("gunshot_event_data is of type: " + str(type(gunshot_event_data))) #just to prove it's a dictionary
    #finally we parse the values into JSON format
    gunshot_event_data = json.dumps(gunshot_event_data)
    #amazing! Now it is a JSON string! We then create a dictionary just like above:
    event_information = {
                         "gunshot_event" : gunshot_event_data,
                         "filepath" : "../SOUND_FILES/1.wav",
                         "api_response" : 202
                         }
    #Then we pass it into the event logging function                     
    instance_of_SQLog.insert_Event_Log_table(event_information)
    
    #if we want to display the last inserted record of event_data
    print("\n\nlast data value:")
    last_entry_is_a_dictionary = instance_of_SQLog.last_Event_entry
    if last_entry_is_a_dictionary != None:  #if the table is empty, it returns None
        for each_item in last_entry_is_a_dictionary:
            print(str(each_item) + " = " + str(last_entry_is_a_dictionary[each_item]))
            
    #if we want to display the a specific record of event_data
    print("\n\nvalue at event_id = 1:")
    specific_entry_is_a_dictionary = instance_of_SQLog.fetch_row_from_Event_Log_table(event_id = 1) #the records start at 1 and not at 0 like arrays
    if specific_entry_is_a_dictionary != None:  #if the table is empty, it returns None
        for each_item in specific_entry_is_a_dictionary:
            print(str(each_item) + " = " + str(specific_entry_is_a_dictionary[each_item]))
            
    #now if we have detected a change and want to change a specific value in a table
    instance_of_SQLog.update_Event_Log_table(event_id = 2,   #the record to change
                                             key = 'api_response', #the item to change
                                             value = 201)            #its new value
    
    #just as easily, again, we can change the last record value like so:
    instance_of_SQLog.update_Event_Log_table(event_id = instance_of_SQLog.last_Event_entry['event_id'],   #the record to change
                                             key = 'api_response', #the item to change
                                             value = 201)            #its new value
    
    #if we want to list all of the entries that have not been updated to the server we say (api_response != 201):
    print("\n\nAll unsent records:")
    for each_unupdated_record in instance_of_SQLog.fetch_unsent_from_Event_Log_table():
        print("->")
        for each_item in each_unupdated_record:
            print("  " + str(each_item) + " = " + str(each_unupdated_record[each_item]))
    
    #finally, we can list all of the data in the entire table
    print("\n\nAll records ever:")
    for each_record in instance_of_SQLog.fetch_all_from_Event_Log_table():
        print("->")
        for each_item in each_record:
            print("  " + str(each_item) + " = " + str(each_record[each_item]))                                
                            
        
if __name__ == "__main__": SQLogClassTestCode()
