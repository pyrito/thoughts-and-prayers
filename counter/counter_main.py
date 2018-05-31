from accessAPI import *
from prayersCounter import *
from searchAPI import *

# Begin running the tweet scraping process and updating database values
def run_main():
    api = get_api()
    db = get_db()
    pc = prayers_counter(db)
    search = search_API(api, pc)
    if pc.past == True:
    	search.count_prayers()
    	pc.finished_past()
    search.count_prayers(True)

if __name__ == '__main__':
    run_main()
