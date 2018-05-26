import datetime
import sqlite3


class prayersCounter():
    def __init__(self):
        self.conn = sqlite3.connect('shootings.db')
        self.c = self.conn.cursor()
        self.tweetsChecked = 0
        self.KEY_WORDS = ['thoughts', 'prayers', 'shooting']
        self.words = ' AND '.join(self.KEY_WORDS)
        self.counts = dict((word,0) for word in self.KEY_WORDS)

        self.c.execute("SELECT * FROM events")
        all_shootings = self.c.fetchall()
        self.shootings = dict()
        for details in all_shootings:
            self.shootings[details[0]] = details[1]

        latest = all_shootings[len(all_shootings)-1]
        self.currentShooting = latest[0]
        self.total = latest[1]
        self.shooting_date = datetime.datetime.strptime(latest[2],"%Y-%m-%d %H:%M:%S")

    def process_tweet(self, text):
        text = text.lower()
        self.tweetsChecked += 1

        if self.KEY_WORDS[2] in text and (self.KEY_WORDS[1] in text or self.KEY_WORDS[0] in text):
            self.total += 1
        if self.tweetsChecked % 10 == 0:
            self.c.execute( """UPDATE events SET tps = ? WHERE shooting_name= ? """, (self.total, self.currentShooting))
            self.conn.commit()

    def update_table(self):
        pass
