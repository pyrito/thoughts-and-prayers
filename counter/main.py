from .accessAPI import *
from .prayersCounter import *
from .searchAPI import *
import datetime
import sqlite3
import os

# Setup shooting database with inaugural shooting event if file not detected
def setup_db():
    if not os.path.isfile('shootings.db'):
        conn = sqlite3.connect('shootings.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE events (
                shooting_name text,
                tps integer,
                dos date
                )  """)
        c.execute("INSERT INTO events VALUES(?, ?, ?)", ("Noblesville", 0, datetime.datetime(2018, 5, 25)))
        conn.commit()

# Begin running the tweet scraping process and updating database values
def run_main():
    api = get_api()
    setup_db()
    pc = prayers_counter()
    search = search_API(api, pc)
    search.count_prayers()
    search.count_prayers(True)

if __name__ == '__main__':
    run_main()
