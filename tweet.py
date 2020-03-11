import os
import time

import tweepy
import asyncio

# Access Secret Keys for Authenticating Twitter Api Object
access_token, access_token_secret, consumer_key, consumer_secret = [os.environ[key] for key in ['TWI_ACCESS_TOKEN', 'TWI_ACCESS_TOKEN_SECRET', 'TWI_API_KEY', 'TWI_API_SECRET_KEY']]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def fake_tweet(status):
    print(status)

def send_tweet(status):
    """
    Method that will send a tweet with a message

    Params:
        status *required (str) => The message that will be tweeted
    """
    api.update_status(status)

def send_media_tweet(filename, status=""):
    """
    Method that will tweet a picture/video/gif

    Params:
        filename *required (str) => The relative filepath of the media to tweet
        status => The text/message to go only with the tweet
    """
    if status:
        api.update_with_media(filename, status=status)
    else:
        api.update_with_media(filename)

async def tweet_many(status_list=[], duration=0):
    assert(duration > 0)

    delay = duration / len(status_list)
    for status in status_list:
        send_tweet(status)
        print(f"Sent tweet with status: {status}")
        await asyncio.sleep(delay)

async def main():
    print(f"started at {time.strftime('/%X')}")

    tasks = []
    tasks.append(tweet_many(['Tweet 1', 'Tweet 2'], 2))
    tasks.append(tweet_many(['Tweet 3', 'Tweet 4'], 2))
    await asyncio.wait(tasks)

    print(f"finished at {time.strftime('/%X')}")

if __name__ == "__main__":
    asyncio.run(main())