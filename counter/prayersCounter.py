import datetime

class prayersCounter():
    def __init__(self, api):
        self.total = 0
        self.tweetsChecked = 0
        self.KEY_WORDS = ['thoughts', 'prayers', 'shooting']
        self.words = ' AND '.join(self.KEY_WORDS)
        self.counts = dict((word,0) for word in self.KEY_WORDS)
        self.shootings = {"Noblesville": 0}
        self.currentShooting = "Noblesville"
        self.shooting_date = datetime.datetime(2018,5,25)
    def process_tweet(self, text):
        text = text.lower()
        self.tweetsChecked += 1
        if self.KEY_WORDS[2] in text and (self.KEY_WORDS[1] in text or self.KEY_WORDS[0] in text):
            self.total += 1

