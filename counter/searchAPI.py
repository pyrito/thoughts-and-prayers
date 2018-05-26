from TwitterAPI import TwitterPager
import datetime
import prayersCounter

class searchAPI():
    def __init__(self, api, prayers):
        self.api = api
        self.counter = prayers
        self.last_id  = 0

    def countPrayers(self, new=False):
        if not new:
            r = TwitterPager(self.api, 'search/tweets', {'q': self.counter.words, 'count': 100})
            for item in r.get_iterator(wait=6):
                if 'id_str' in item:
                    tweet_id = int(item['id_str'])
                    if tweet_id > self.last_id:
                        self.last_id = tweet_id

                if 'created_at' in item:
                    tweet_date = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    if tweet_date < self.counter.shooting_date:
                        break

                if 'text' in item:
                    self.counter.process_tweet(item['text'])
                elif 'message' in item and item['code'] == 88:
                    print('\n*** SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
                    break
                print("Tweets Checked " + str(self.counter.tweetsChecked))
                print(self.counter.total)
        else:
            limit = 0
            r = TwitterPager(self.api, 'search/tweets', {'q': self.counter.words, 'count': 100, 'since_id': self.last_id})
            for item in r.get_iterator(wait=6):
                if limit < 100:
                    limit += 1
                    if 'id_str' in item:
                        tweet_id = int(item['id_str'])
                        if tweet_id > self.last_id:
                            self.last_id = tweet_id
                    if 'text' in item:
                        self.counter.process_tweet(item['text'])
                    elif 'message' in item and item['code'] == 88:
                        print('\n*** SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
                        break
                else:
                    break
        print("Tweets Checked " + str(self.counter.tweetsChecked))
        print(self.counter.total)