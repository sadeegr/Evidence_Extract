import os
import sqlite3

# execute a query on sqlite cursor
def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except Exception as error:
        print(str(error) + "\n " + query)
# get bookmarks from firefox sqlite database file and print all
def get_bookmarks(cursor):
    bookmarks_query = """select url, moz_places.title, rev_host, frecency,
    last_visit_date from moz_places  join  \
    moz_bookmarks on moz_bookmarks.fk=moz_places.id where visit_count>0
    and moz_places.url  like 'http%'
    order by dateAdded desc;"""
    # execute_query(cursor, bookmarks_query)
    cursor.execute(bookmarks_query)
    
    print()
    for row in cursor:
        
        link = row[0]
        title = row[1]
        print(link,title)
# set the path of firefox folder with databases
bookmarks_path = os.path.expanduser('~')+"\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
# get firefox profile

profiles = [i for i in os.listdir(bookmarks_path)]
# get sqlite database of firefox bookmarks
sqlite_path = bookmarks_path+ profiles[0]+'/places.sqlite'
#
if os.path.exists(sqlite_path):
    firefox_connection = sqlite3.connect(sqlite_path)
cursor = firefox_connection.cursor()
bookmarks_query = """select url, moz_places.title, rev_host, frecency,
    last_visit_date from moz_places  join  \
    moz_bookmarks on moz_bookmarks.fk=moz_places.id where visit_count>0
    and moz_places.url  like 'http%'
    order by dateAdded desc;"""
# execute_query(cursor, bookmarks_query)
cursor.execute(bookmarks_query)
cur=cursor.fetchall()
for i in cur:
    print(i)
    
# get_bookmarks(cursor)
cursor.close()