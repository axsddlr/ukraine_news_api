import os
import re
import sys

import httpx
import tweepy
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils.utils import headers

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


# def get_all_tweets(screen_name):
#     all_tweets = []
#     new_tweets = []
#     client = get_twitter_client()
#     new_tweets = client.user_timeline(screen_name=screen_name, count=10)
#     while len(new_tweets) > 0:
#         for tweet in new_tweets:
#             parsed_tweet = {'date': tweet.created_at, 'author': tweet.user.name, 'twitter_name': tweet.user.screen_name,
#                             'text': tweet.text, 'number_of_likes': tweet.favorite_count,
#                             'number_of_retweets': tweet.retweet_count}
#             all_tweets.append(parsed_tweet)
#         # print("We've got %s tweets so far" % (len(all_tweets)))
#         max_id = new_tweets[-1].id - 1
#         new_tweets = client.user_timeline(screen_name=screen_name,
#                                           count=10, max_id=max_id)
#     return all_tweets

class Kyiv:
    @staticmethod
    def kyiv_news():
        URL = "https://kyivindependent.com/news-archive/"
        html = httpx.get(URL, headers=headers)
        soup = BeautifulSoup(html.content, "lxml")
        status = html.status_code

        base = soup.find(id="main")
        # print(base)

        kyiv_module = base.find_all(
            class_=re.compile("type-post")
        )

        result = []
        for module in kyiv_module:
            # Titles of articles
            title = module.find(class_=re.compile("entry-title")).text.strip()
            # # Thumbnails of each article
            excerpt = module.find(class_=re.compile("entry-content")).find(
                class_=re.compile("post-excerpt")).text.strip()

            post_time = module.find(class_=re.compile("recent-date")).text.strip()

            url = module.find(class_=re.compile("entry-title")).find("a")['href']

            # scrape each page from url variable then get the mp4 file per page
            if url.split("//")[-1].split(".")[0] == re.compile("kyivindependent"):
                r = httpx.get(url, headers=headers)
                soup = BeautifulSoup(r.content, 'lxml')

                vids = []
                for mp4 in soup.find_all(class_=re.compile("post-digest__link")):
                    vids.append({mp4["href"]
                                 })
            else:
                vids = url
            # if video is not private, then add to dict
            result.append(
                {
                    "title": title,
                    "post_body": excerpt,
                    "time": post_time,
                    "url": vids,
                }
            )

        if status != 200:
            raise Exception("API response: {}".format(status))
        return result

    @staticmethod
    def get_kyiv():
        all_tweets = []
        new_tweets = []
        client = get_twitter_client()
        new_tweets = client.user_timeline(screen_name="KyivIndependent", count=10)
        while len(new_tweets) > 0:
            for tweet in new_tweets:
                if "⚡" in tweet.text:
                    parsed_tweet = {'date': tweet.created_at, 'author': tweet.user.name,
                                    'twitter_name': tweet.user.screen_name,
                                    'text': tweet.text, 'number_of_likes': tweet.favorite_count,
                                    'number_of_retweets': tweet.retweet_count}
                all_tweets.append(parsed_tweet)
            # print("We've got %s tweets so far" % (len(all_tweets)))
            max_id = new_tweets[-1].id - 1
            new_tweets = client.user_timeline(screen_name="KyivIndependent",
                                              count=10, max_id=max_id)
        return all_tweets


if __name__ == '__main__':
    print(Kyiv().get_kyiv())
