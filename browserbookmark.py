import chrome_bookmarks
import csv

# for folder in chrome_bookmarks.folders:
#     print(folder.name)
#     print(folder.folders)
    
# for url in chrome_bookmarks.urls:
#     print(url.url, url.name)
    
    
def write_browserbookmarks_csv() -> None:
    """It writes csv files that contain the browser history in
    the current working directory. It will writes csv files base on
    the name of browsers the program detects."""
    try:
        for folder in chrome_bookmarks.urls:
            with open('bookmarks.csv', mode='w') as csv_file:
                for data in chrome_bookmarks.urls:
                    if data.name!=None and data.url !=None:
                        dt="Name : "+data.name+"\t"+"URL :"+data.url
                        csv_file.write(dt)
                        csv_file.write('\n')
    except:
         print("End of data")
                
            
write_browserbookmarks_csv()