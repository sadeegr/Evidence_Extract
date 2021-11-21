import glob
import hashlib
import os
import sqlite3
import sys
from datetime import datetime

path=os.path.expanduser('~')+"\Downloads"
files=os.listdir(path)
result=[]
for file in files:
    try:
        with open(path+"\\"+file, 'rb') as inputfile:
            data = inputfile.read()
            dt="File:"+file+"====="+"Hash:"+hashlib.md5(data).hexdigest()
            print("pending..")
            result.append(dt)
            break
    except:
        continue
    
def write_browserdownloadhash_csv() -> None:
    """It writes csv files that contain the browser history in
    the current working directory. It will writes csv files base on
    the name of browsers the program detects."""
    try:
                   
        with open('downloadedAndHash.csv', mode='w') as csv_file:
            for file in result:
                csv_file.write(file)
                csv_file.write('\n')
    except:
         print("End of data")
                
                
#Chrome download            
def DownloadExtractChrome() -> None:
        
    if os.name == "nt":
        # This is the Windows Path
        PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
        if not os.path.isdir(PathName):
            print('[!] Chrome Doesn\'t exists')
            sys.exit(0)
    elif (os.name == "posix") and (sys.platform == "darwin"):
        # This is the OS X Path
        PathName = os.getenv('HOME') + "/Library/Application Support/Google/Chrome/Default/"
        if not os.path.isdir(PathName):
            print('[!] Chrome Doesn\'t exists')
            sys.exit(0)
    elif os.name == "posix":
        # This is the Linux Path
        PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
        if not os.path.isdir(PathName):
            print('[!] Chrome Doesn\'t exists')
            sys.exit(0)

    # PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\History'
    history_db = PathName + 'History'
    c1 = sqlite3.connect(history_db)
    cursor1 = c1.cursor()

    # Extract Data

    select_statement_downloads = "SELECT downloads.id,downloads.current_path,downloads.target_path,downloads.referrer,downloads.received_bytes," \
                                "downloads.total_bytes,datetime(downloads.start_time / 1000000 + (strftime('%s', '1601-01-01'))," \
                                " 'unixepoch', 'localtime')," \
                                "datetime(downloads.end_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')," \
                                "downloads.state,downloads.opened,downloads.danger_type,downloads.interrupt_reason FROM downloads;"

    cursor1.execute(select_statement_downloads)
    results = cursor1.fetchall()


    #Write data to CSV file
    with open('ChromeDownload.csv', "w", encoding="utf-8") as file:
        file.write('id,current_path,target_path,referrer,received_bytes,total_bytes,start_time,end_time,state,opened,danger_type,interrupt_reason\n')
        for i in results:
            file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}\n".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]))
            
            

#EDGE Download    
#Track Downloads
def DownloadExtractEdge() -> None:

    history_db =os.path.expanduser('~')+'\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default'
   
    history_db = history_db + '\History'
    print(history_db)
    c1 = sqlite3.connect(history_db)
    cursor1 = c1.cursor()

    #Extract Data
    select_statement_downloads = "SELECT downloads.id,downloads.current_path,downloads.target_path,downloads.referrer,downloads.received_bytes,downloads.total_bytes,datetime(downloads.start_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime')," \
                                "datetime(downloads.end_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime'),downloads.state,downloads.opened,downloads.danger_type,downloads.interrupt_reason FROM downloads;"
    cursor1.execute(select_statement_downloads)
    results = cursor1.fetchall()


    #Write data to CSV file
    with open('EdgeDownload.csv', "w", encoding="utf-8") as file:
        file.write('id,current_path,target_path,referrer,received_bytes,total_bytes,start_time,end_time,state,opened,danger_type,interrupt_reason\n')
        for i in results:
            file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}\n".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]))



    
            
write_browserdownloadhash_csv()
DownloadExtractChrome()
DownloadExtractEdge()


