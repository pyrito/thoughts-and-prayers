from TwitterAPI import TwitterPager
import datetime

# Class that handles processing the API calls to twitter
class search_API():
    def __init__(self, api, prayers):
        self.api = api
        self.counter = prayers

    # method to access twitterAPI and count prayers in the past or live
    def count_prayers(self, new=False):
        # Count past prayers until the date of the incident
        if not new and self.counter.last_id == 0:
            r = TwitterPager(self.api, 'search/tweets', {'q': self.counter.words, 'count': 100})
            print("first iterator")
            for item in r.get_iterator(wait=6):
                if 'id_str' in item:
                    tweet_id = int(item['id_str'])
                    if tweet_id > self.counter.last_id:
                        self.counter.last_id = tweet_id
                        self.counter.initial_tweet = tweet_id
                        self.counter.update_initial_id()
                    elif tweet_id < self.counter.last_id:
                        self.counter.last_id = tweet_id
                    self.counter.update_id()

                # Make sure we haven't reached a tweet that occured before the incident
                if 'created_at' in item:
                    tweet_date = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    print(tweet_date)
                    if tweet_date < self.counter.shooting_date:
                        break

                # Process tweet unless we reach an API call limit
                if 'text' in item:
                    self.counter.process_tweet(item['text'])
                elif 'message' in item and item['code'] == 88:
                    print('\n*** SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
                    break
                print("Tweets Checked " + str(self.counter.tweetsChecked))
                print(self.counter.total)
        #API has partially been parsed continue searching into the past
        elif not new and self.counter.last_id > 0:
            r = TwitterPager(self.api, 'search/tweets', {'q': self.counter.words, 'count': 100, 'max_id':self.counter.last_id})
            print("pickup iterator")
            for item in r.get_iterator(wait=6):
                if 'id_str' in item:
                    tweet_id = int(item['id_str'])
                    if tweet_id < self.counter.last_id:
                        self.counter.last_id = tweet_id
                        self.counter.update_id()
                # Make sure we haven't reached a tweet that occured before the incident
                if 'created_at' in item:
                    tweet_date = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    print(tweet_date)
                    if tweet_date < self.counter.shooting_date:
                        break

                # Process tweet unless we reach an API call limit
                if 'text' in item:
                    self.counter.process_tweet(item['text'])
                elif 'message' in item and item['code'] == 88:
                    print('\n*** SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
                    break
                print("Tweets Checked " + str(self.counter.tweetsChecked))
                print(self.counter.total)
        # Count prayers from last checked ID and upto live prayers about the incident
        else:
            print("new iterator")
            r = TwitterPager(self.api, 'search/tweets', {'q': self.counter.words, 'count': 100, 'since_id':self.counter.last_id})
            for item in r.get_iterator(wait=6, new_tweets=True):
                if 'id_str' in item:
                    tweet_id = int(item['id_str'])
                    if tweet_id > self.counter.last_id:
                        self.counter.last_id = tweet_id
                        self.counter.update_id()
                if 'text' in item:
                    print(item['created_at'])
                    self.counter.process_tweet(item['text'])
                elif 'message' in item and item['code'] == 88:
                    print('\n*** SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
                    break
                print("Tweets Checked " + str(self.counter.tweetsChecked))
                print(self.counter.total)