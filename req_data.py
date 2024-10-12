import tweepy
from utils.keys import *

# Authenticate to the Twitter API
auth = tweepy.OAuth1UserHandler(client_id, client_secret, access_token, access_token_secret)
api = tweepy.API(auth)


try:
    # Get the rate limit status
    rate_limit_status = api.rate_limit_status()

    # Display the rate limit status for specific endpoints
    for resource, limits in rate_limit_status['resources'].items():
        print(f"Resource: {resource}")
        for endpoint, limit_info in limits.items():
            print(f"  Endpoint: {endpoint}")
            print(f"    Limit: {limit_info['limit']}")
            print(f"    Remaining: {limit_info['remaining']}")
            print(f"    Reset: {limit_info['reset']} (Unix timestamp)")
except tweepy.Unauthorized as e:
    print("Error: Authentication failed. Check your API keys and tokens.")
except tweepy.TweepyException as e:
    print(f"Error: {e}")
