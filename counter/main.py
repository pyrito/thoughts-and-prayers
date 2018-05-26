import accessAPI
import prayersCounter
import searchAPI
import datetime
import sqlite3
import os

api = accessAPI.get_api()
if not os.path.isfile('shootings.db'):
    conn = sqlite3.connect('shootings.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE events (
            shooting_name text,
            tps integer,
            dos date
            )  """)
    c.execute("INSERT INTO events VALUES(?, ?, ?)", ("Noblesville", 0, datetime.datetime(2018,5,25)))
    conn.commit()
pc = prayersCounter.prayersCounter()
search = searchAPI.searchAPI(api, pc)
search.countPrayers()
search.countPrayers(True)