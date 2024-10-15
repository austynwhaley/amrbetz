import tweepy
from utils.keys import *

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

client.create_tweet(text="API TEST MIND YA BIZNESS - AMR")

print("Tweet successful :)")