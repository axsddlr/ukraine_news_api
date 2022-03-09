import sys
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

"""
Twitter Authentification Credentials
Please update with your own credentials
"""
cons_key = os.getenv("cons_key")
cons_secret = os.getenv("cons_secret")
acc_token = os.getenv("acc_token")
acc_secret = os.getenv("acc_secret")


def get_twitter_auth():
    """
    @return:
        - the authentification to Twitter
    """
    try:
        consumer_key = cons_key
        consumer_secret = cons_secret
        access_token = acc_token
        access_secret = acc_secret

    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return auth


def get_twitter_client():
    """
    @return:
        - the client to access the authentification API
    """
    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client


def get_all_tweets(screen_name):
    all_tweets = []
    new_tweets = []
    client = get_twitter_client()
    new_tweets = client.user_timeline(screen_name=screen_name, count=10)
    while len(new_tweets) > 0:
        for tweet in new_tweets:
            parsed_tweet = {'date': tweet.created_at, 'author': tweet.user.name, 'twitter_name': tweet.user.screen_name,
                            'text': tweet.text, 'number_of_likes': tweet.favorite_count,
                            'number_of_retweets': tweet.retweet_count}
            all_tweets.append(parsed_tweet)
        # print("We've got %s tweets so far" % (len(all_tweets)))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(screen_name=screen_name,
                                          count=10, max_id=max_id)
    return all_tweets


def get_kyiv():
    all_tweets = []
    new_tweets = []
    client = get_twitter_client()
    new_tweets = client.user_timeline(screen_name="KyivIndependent", count=10)
    while len(new_tweets) > 0:
        for tweet in new_tweets:
            parsed_tweet = {'date': tweet.created_at, 'author': tweet.user.name, 'twitter_name': tweet.user.screen_name,
                            'text': tweet.text, 'number_of_likes': tweet.favorite_count,
                            'number_of_retweets': tweet.retweet_count}
            all_tweets.append(parsed_tweet)
        # print("We've got %s tweets so far" % (len(all_tweets)))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(screen_name="KyivIndependent",
                                          count=10, max_id=max_id)
    return all_tweets


if __name__ == '__main__':
    print(get_all_tweets("KyivIndependent"))
