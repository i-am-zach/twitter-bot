import os
import time

import tweepy

access_token, access_token_secret, consumer_key, consumer_secret = [os.environ[key] for key in ['TWI_ACCESS_TOKEN', 'TWI_ACCESS_TOKEN_SECRET', 'TWI_API_KEY', 'TWI_API_SECRET_KEY']]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


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

def timed_method(func, duration=30, loops=1, params=[]):
    """
    Method that will call a function a certain amount of (loops) given a time period of (duration)

    Params:
        func (function) => The function/method that will be called on the loop
        duration (int) => How long it will take for the code to execute
        loops (int) => How many times the function will be called
        params (list) => An list of lists. Each in the list will be unpacked as the parameters of the function
    """
    for i in range(loops):
        if params:
            func(*params[i])
        else:
            func()
        time.sleep(duration/loops)

