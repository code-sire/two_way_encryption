
#Import all the Modules that are needed.
import os
import sqlite3
from sqlite3 import Error


# Finding the path to the Script
ScriptLoc = os.path.split(__file__)
ScriptHome = ScriptLoc[0]


# Setting Relative Paths
DBPath = ScriptHome + '/' + "settings.db"


# Creating a a Function to run SQL Statements
def runsql(def_conn, def_sql, def_message):
    try:
        cur = def_conn.cursor()
        cur.execute(def_sql)
        print(def_message)
        return cur
    except Error as e:
        print(e)


# Connecting to the SQLite Database.
# If the database is not present it will be created.
def create_connection(def_dbfile):
    conn = None
    try:
        conn = sqlite3.connect(def_dbfile)
        print('Database Location:',def_dbfile)
    except Error as e:
        print(e)
        input('Press Enter to close this window.')
        quit()

    return conn


### Run ###

# Establishing the Database Connection
conn = create_connection(DBPath)

# Defining a Table to be Created
sql_create_table = """ CREATE TABLE IF NOT EXISTS pii_details (
                            RecordID integer PRIMARY KEY,
                            PII_Key text NOT NULL,
                            PII_Value text NULL); """

# This is the SQL to do a record count
sql_record_count = """ SELECT Count(*) FROM pii_details; """

# The next few lines are to add some rows to the table.
sql_table_insert_1 = """ INSERT INTO pii_details (PII_Key) VALUES ('hash_key'); """
sql_table_insert_2 = """ INSERT INTO pii_details (PII_Key) VALUES ('username'); """
sql_table_insert_3 = """ INSERT INTO pii_details (PII_Key) VALUES ('encrypted_password'); """


# Creating the Table if it needs to be.
runsql(conn, sql_create_table, 'Table Present or Added')

# Checking if needed rows are present.
# If they are not then they will be added.
cursor = runsql(conn, sql_record_count, 'Checking Record Count')
rawrecordcount = cursor.fetchall()
rawrecordcount = rawrecordcount[0]
recordcount = rawrecordcount[0]

if recordcount == 0:
    print('There were no rows in the table, so the needed rows are being added.')
    runsql(conn, sql_table_insert_1, 'Adding Row 1')
    runsql(conn, sql_table_insert_2, 'Adding Row 2')
    runsql(conn, sql_table_insert_3, 'Adding Row 3')

# Sealing Things Up
conn.commit()
conn.close()