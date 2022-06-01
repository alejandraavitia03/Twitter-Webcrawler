from decimal import ConversionSyntax
from multiprocessing.connection import wait
import tweepy
from tweepy import streaming
import json
import pandas as pd
import time

tweet_list = []

def save_tweets(tweet):
    print(json.dumps(tweet, indent=4, sort_keys=True))
    data = tweet['data']
    place = ""
    if 'includes' in tweet:
        if 'places' in tweet['includes']:
            if 'name' in tweet['includes']['places']:
                place = tweet['includes']['places']['name']
    if 'urls' in data['entities']:
        print('URL exists!')
        titles = []
        for u in data['entities']['urls']:
            if 'title' in u:
                titles.append(u['title'])
        tweet_list.append([data['author_id'], data['created_at'],data['text'], titles, place])
    else:
        print('NO URL!')

class Listener(tweepy.StreamingClient):

    tweet_count = 0
    tweet_limit = 15

    def __init__(self, bearer_token, wait_on_rate_limit, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        super(Listener, self).__init__(bearer_token=bearer_token, wait_on_rate_limit=wait_on_rate_limit)

    def on_data(self, data):
        Listener.tweet_count += 1
        if time.time() - self.start_time > self.limit:
            self.disconnect()
        json_response = json.loads(data)
        try:
            save_tweets(json_response)
        except (json.JSONDecodeError, KeyError) as err:
            # In case the JSON fails to decode, we skip this tweet
            print(f"ERROR: encountered a problem with a line of data... \n")

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAnEcAEAAAAAT3JJHlJMeKfQEtTZESDft5mOj2o%3DBs8QkCdtsAvQ9pwEhtGZuNnTPFM0TDtomlhnyOeVAmuYXGPpOE'
rules = []
rules.append(tweepy.StreamRule(value="Riverside", tag="Riverside"))
tweet_fields = ["author_id", "created_at", "entities"]
streaming_client = Listener(bearer_token=bearer_token, wait_on_rate_limit=True, time_limit=60)
streaming_client.add_rules(rules)
streaming_client.filter(tweet_fields=tweet_fields,expansions="geo.place_id")

print("writing...")
df = pd.DataFrame(tweet_list, columns = ['author_id' , 'created_at', 'text', 'titles', 'place'])
df.to_json("tweets.json")
print("finished writing")
