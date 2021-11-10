import glob
import hashlib
import os
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
                
            
write_browserdownloadhash_csv()