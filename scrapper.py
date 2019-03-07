from twython import Twython
import json
import argparse
import time

MAX_REQUEST_SIZE = 200
DELAY = 15


class Scrapper():
    ''' Autentica requests na API do Twitter e faz busca tweets de um usuario especifico '''

    def __init__(self, username, total_tweets, include_retweets):

        self.username = username
        self.total_tweets = total_tweets
        self.include_retweets = include_retweets

        config = self.parse_config()

        twitter = Twython(config['consumer_key'],
        config['consumer_secret'],oauth_version=2)

        ACCESS_TOKEN = twitter.obtain_access_token()

        self.t = Twython(config['consumer_key'], access_token=ACCESS_TOKEN)

        #user_timeline = t.get_user_timeline(screen_name='jairbolsonaro', count=200, include_rts=0, tweet_mode="extended")

    def parse_config(self):
        ''' Pega dos dados de acesso do seu APP no Twitter '''
        f = open('config.json', 'r')
        return json.load(f)

    def get_tweet_batch(self, counts, max_id):
        ''' Pega um batch de tweets '''
        return self.t.get_user_timeline(screen_name=self.username,
        count=counts, include_rts=self.include_retweets, tweet_mode="extended", max_id = max_id)

    def get_total_tweets(self):
        ''' Pega o numero total de tweets atraves de multiplas requisicoes '''
 
        calls, rest = self.total_tweets // MAX_REQUEST_SIZE, self.total_tweets % MAX_REQUEST_SIZE

        if rest >= 0:
            tweets = self.get_tweet_batch(rest, None)
        for i in range(calls):
            time.sleep(DELAY)
            tweets.extend(self.get_tweet_batch(MAX_REQUEST_SIZE, tweets[-1]['id']))

        return tweets

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", '--username', help='Usuario para extracao de tweets', type=str)
    parser.add_argument("-t", '--total', help='Total de tweets para ser extraido', type=int)
    parser.add_argument("-r", '--retweets', help='Se inclui retweets ou nao', type=bool)

    args = parser.parse_args()

    tst = Scrapper(args.username, args.total, args.retweets)

    oi = tst.get_total_tweets()

    return oi

if __name__ == '__main__':
    oi = main()
