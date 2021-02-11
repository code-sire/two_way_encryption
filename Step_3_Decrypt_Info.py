
#Import all the Modules that are needed.
import os
import sqlite3
from sqlite3 import Error
from cryptography.fernet import Fernet


# Finding the path to the Script
ScriptLoc = os.path.split(__file__)
ScriptHome = ScriptLoc[0]


# Setting Relative Paths
DBPath = ScriptHome + '/' + "settings.db"


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


# Creating a a Function to run SQL Statements
def runsql(def_conn, def_sql, def_message):
    try:
        cur = def_conn.cursor()
        cur.execute(def_sql)
        print(def_message)
        return cur
    except Error as e:
        print(e)


# Pulling the Value Based on Key
def ReadValue(def_conn, def_key, def_message):
    sql_read = """SELECT PII_Value FROM pii_details where PII_Key = '""" + def_key + """'; """
    cursor = runsql(def_conn, sql_read, def_message)
    rawvalue = cursor.fetchall()
    muddyvalue = rawvalue[0]
    cleanvalue = muddyvalue[0]
    return cleanvalue


# Pulling the Hash Key
def PullCryptHash(def_conn):
    crypthash = ReadValue(def_conn, 'hash_key', 'Pulling Encryption Hash')
    return crypthash

# Pulling the Username
def PullUser(def_conn):
    user = ReadValue(def_conn, 'username', 'Pulling Username')
    return user

# Pulling the Password
def PullPassHash(def_conn):
    hashkey = PullCryptHash(def_conn)
    encodehashkey = hashkey.encode("utf-8")
    cipher_suite = Fernet(encodehashkey)
    passhash = ReadValue(def_conn, 'encrypted_password', 'Pulling Encrypted Password')
    encodepasshash = passhash.encode("utf-8")
    uncipher_text = cipher_suite.decrypt(encodepasshash)
    password = bytes(uncipher_text).decode("utf-8")
    return password


### Run ###

# Establishing the Database Connection
conn = create_connection(DBPath)

# Running Functions
username = PullUser(conn)
password = PullPassHash(conn)

# Output of the info
print('The username is:', username)
print('The password is:', password)