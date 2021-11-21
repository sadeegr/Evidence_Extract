import browserbookmark as bookmark
import browsercookies as cookies
import browserhistory as history
import browserPasswords as passsword
import downloadedhash as hash


if __name__ == '__main__':
    bookmark.write_browserbookmarks_csv()
    cookies.main()
    cookies.EdgeCookies()
    history.write_browserhistory_csv()
    passsword.ChromePasswords()
    hash.write_browserdownloadhash_csv()
    hash.DownloadExtractChrome()
    hash.DownloadExtractEdge()
    