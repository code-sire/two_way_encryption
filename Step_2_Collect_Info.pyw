
#Import all the Modules that are needed.
import os
import sqlite3
from sqlite3 import Error
from cryptography.fernet import Fernet
import tkinter as tk


# Finding the path to the Script
ScriptLoc = os.path.split(__file__)
ScriptHome = ScriptLoc[0]


# Setting Relative Paths
DBPath = ScriptHome + '/' + "settings.db"


# Defining the GUI
apptitle = "Get Credentials"
root = tk.Tk()
root.title(apptitle)

# Define GUI window size
guiwidth = 500
guiheight = 145

# This gets the screen resolution
window_x = root.winfo_screenwidth()
window_y = root.winfo_screenheight()

# Defines the center of the screen
# and then has the GUI open there.
x = (window_x /2) - (guiwidth /2)
y = (window_y /2) - (guiheight /2)
root.geometry('%dx%d+%d+%d' % (guiwidth, guiheight, x, y))

# Declares that the GUI is not Resizable
root.resizable(False, False)

# Setting GUI Variables
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()

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

# Set a New Value Based on Key
def WriteValue(def_conn, def_key, def_value, def_message):
    sql_update = """UPDATE pii_details SET PII_Value = '""" + def_value + """' WHERE PII_Key = '""" + def_key + """'; """
    runsql(def_conn, sql_update, def_message)
    def_conn.commit()

# Pulling Scripts
def PullCryptHash(def_conn):
    crypthash = ReadValue(def_conn, 'hash_key', 'Pulling Encryption Hash')
    return crypthash


# Writing Encryption Hash to the Database.
def SetCryptHash(def_conn):
    keybytes = Fernet.generate_key()
    keystring = bytes(keybytes).decode("utf-8")
    WriteValue(def_conn, 'hash_key', keystring, 'Setting Encryption Hash')

# Writing Username to the Database.
def SetUser(def_conn, def_value):
    WriteValue(def_conn, 'username', def_value, 'Setting Username')

# Writing Password Hash to the Database.
def SetPassHash(def_conn, def_value):
    hashkey = PullCryptHash(def_conn)
    encodedpass = def_value.encode("utf-8")
    cipher_suite = Fernet(hashkey)
    ciphered_text = cipher_suite.encrypt(encodedpass)
    keystring = bytes(ciphered_text).decode("utf-8")
    WriteValue(def_conn, 'encrypted_password', keystring, 'Setting Encrypted Password')

# This is what happens when "Submit" is clicked in the GUI.
def SubmitData():
    if USERNAME.get().strip() == "" or PASSWORD.get().strip() == "":
        print('You need to fill both fields.')

    else:
        # Pulling in trimmed values from the form.
        entered_username = USERNAME.get().strip()
        entered_password = PASSWORD.get().strip()

        # Calling Functions
        SetUser(conn, entered_username)
        SetPassHash(conn, entered_password)

        # Close the GUI
        root.destroy()

### Run ###

# Establishing the Database Connection
conn = create_connection(DBPath)

# Checking to see if there is an Encryption Hash.
# If there isn't one will be created and saved.
crypthashcheck = PullCryptHash(conn)
if crypthashcheck is None:
    SetCryptHash(conn)

# Defining the form fields
tk.Label(root, text="Username: ").grid(sticky="W", row=0, column=0, padx=10)
entered_value1 = tk.Entry(root, textvariable=USERNAME, width=40)
entered_value1.grid(row=0, column=1, padx=10, pady=10, sticky="W")

tk.Label(root, text="Password: ").grid(sticky="W", row=1, column=0, padx=10, pady=10)
entered_value2 = tk.Entry(root, textvariable=PASSWORD, width=40, show="*")
entered_value2.grid(row=1, column=1, padx=10, pady=10, sticky="W")

# Buttons to Take Action
quit_button = tk.Button(root, text="Cancel", command=root.destroy, padx=12)
quit_button.grid(row=5, column=0, sticky="W", padx=10, pady=10)
submit_button = tk.Button(root, text="Submit", command=SubmitData, padx=5)
submit_button.grid(row=5, column=1, sticky="E", padx=10, pady=10)

# Start the GUI event loop
root.mainloop()