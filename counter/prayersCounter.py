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
            self.db.execute("INSERT INTO events VALUES(%s, %s, %s, %s, %s, %s, %s)", (0, "Noblesville", 0, datetime.datetime(2018, 5, 25), 0, 0, True))
            all_shootings = self.db.execute("SELECT * FROM events").fetchall()
        
        latest = all_shootings[len(all_shootings)-1]
        self.current_shooting = latest[1]
        self.total = latest[2]
        self.shooting_date = latest[3]
        self.last_id = latest[4]
        self.initial_tweet = latest[5]
        self.past = latest[6]

    # process the tweet text if to see if its a real thought and/or prayer
    def process_tweet(self, text):
        text = text.lower()
        self.tweetsChecked += 1
        # update thoughts and prayers count if it matches criterion
        if self.KEY_WORDS[2] in text and (self.KEY_WORDS[1] in text or self.KEY_WORDS[0] in text):
            self.total += 1
        if self.tweetsChecked % 10 == 0:
            self.db.execute( """UPDATE events SET count = %s WHERE place = %s """, (self.total, self.current_shooting))
    def finished_past(self):
        self.past = False
        self.last_id = self.initial_tweet
        self.db.execute( """UPDATE events SET backwards = %s WHERE place = %s """, (self.past, self.current_shooting))
    def update_id(self):
        self.db.execute( """UPDATE events SET lasttweet = %s WHERE place = %s """, (self.last_id, self.current_shooting))
    def update_initial_id(self):
        self.db.execute( """UPDATE events SET initialtweet = %s WHERE place = %s """, (self.initial_tweet, self.current_shooting))

