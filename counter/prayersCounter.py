import datetime
import sqlite3

# Class to count the number of shootings
class prayers_counter():
    def __init__(self):
        # Database connection
        self.conn = sqlite3.connect('shootings.db')
        self.c = self.conn.cursor()

        # setup classic keywords that make a difference
        self.tweetsChecked = 0
        self.KEY_WORDS = ['thoughts', 'prayers', 'shooting']
        self.words = ' AND '.join(self.KEY_WORDS)

        # obtain current values database if it exists
        self.c.execute("SELECT * FROM events")
        all_shootings = self.c.fetchall()

        latest = all_shootings[len(all_shootings)-1]
        self.current_shooting = latest[0]
        self.total = latest[1]
        self.shooting_date = datetime.datetime.strptime(latest[2],"%Y-%m-%d %H:%M:%S")

    # process the tweet text if to see if its a real thought and/or prayer
    def process_tweet(self, text):
        text = text.lower()
        self.tweetsChecked += 1

        # update thoughts and prayers count if it matches criterion
        if self.KEY_WORDS[2] in text and (self.KEY_WORDS[1] in text or self.KEY_WORDS[0] in text):
            self.total += 1
        if self.tweetsChecked % 10 == 0:
            self.c.execute( """UPDATE events SET tps = ? WHERE shooting_name= ? """, (self.total, self.current_shooting))
            self.conn.commit()
