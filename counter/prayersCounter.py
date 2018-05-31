import datetime
import sqlalchemy

# Class to count the number of shootings
class prayers_counter():
    def __init__(self, db):
        # Database connection
        self.db = db

        # setup classic keywords that make a difference
        self.tweetsChecked = 0
        self.KEY_WORDS = ['thoughts', 'prayers', 'shooting']
        self.words = ' AND '.join(self.KEY_WORDS)

        # obtain current values database if it exists
        all_shootings = (self.db.execute("SELECT * FROM events")).fetchall()
        if len(all_shootings) == 0:
            self.db.execute("INSERT INTO events VALUES(%s, %s, %s, %s)", (0, "Noblesville", 0, datetime.datetime(2018, 5, 25)))
            all_shootings = self.db.execute("SELECT * FROM events")
        
        latest = all_shootings[len(all_shootings)-1]
        self.current_shooting = latest[1]
        self.total = 0
        self.shooting_date = latest[3]

    # process the tweet text if to see if its a real thought and/or prayer
    def process_tweet(self, text):
        text = text.lower()
        self.tweetsChecked += 1

        # update thoughts and prayers count if it matches criterion
        if self.KEY_WORDS[2] in text and (self.KEY_WORDS[1] in text or self.KEY_WORDS[0] in text):
            self.total += 1
        if self.tweetsChecked % 10 == 0:
            self.db.execute( """UPDATE events SET count = %s WHERE place = %s """, (self.total, self.current_shooting))
