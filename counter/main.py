import accessAPI
import prayersCounter
import searchAPI
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
    api = accessAPI.get_api()
    setup_db()
    pc = prayersCounter.prayers_counter()
    search = searchAPI.search_API(api, pc)
    search.count_prayers()
    search.count_prayers(True)
