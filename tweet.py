import os
import time

import tweepy
import asyncio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pprint import pprint
from dotenv import load_dotenv

load_dotenv(verbose=True)

# Access Secret Keys for Authenticating Twitter Api Object
access_token, access_token_secret, consumer_key, consumer_secret = [os.environ[key] for key in ['TWI_ACCESS_TOKEN', 'TWI_ACCESS_TOKEN_SECRET', 'TWI_API_KEY', 'TWI_API_SECRET_KEY']]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

epoch = datetime(year=2020, month=3, day=26, hour=2, minute=17)

def fake_tweet(status):
    print(status)

def send_tweet(status, options={"supress_message": True}):
    """
    Method that will send a tweet with a message

    Params:
        status *required (str) => The message that will be tweeted
        options:
            - supress_message (t/f):
                when false, prints a message indicating the tweet was sent
    """
    if not options['supress_message']:
        print("Sending Tweet with Message")

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
        
def gen_msg(schedule_time):
    delta = relativedelta(schedule_time, epoch)
    return f"Telling @JeffProbst and @survivorcbs to put @DerrickTiveron on Survivor every day until he's on Survivor. Day {delta.days}" 

def log_scheduled_tweet(schedule_time, msg, repeat):
    print(f"""
Scheduled Tweet for {schedule_time}
Message: {msg}
Repeat: {repeat}""")

async def schedule_tweet(hour, minute, second, msg="--reminder", repeat=False):
    if hour != 0:
        assert hour, "Hour argument is required"
    if minute != 0:
        assert minute, "Minute argument is required"

    start = datetime.now()
    schedule_time = datetime(year=start.year, month=start.month, day=start.day, hour=hour, minute=minute, second=second)
    
    if schedule_time < start:
        schedule_time += timedelta(days=1)


    if msg == "--reminder":
        msg = gen_msg(schedule_time)
        
    log_scheduled_tweet(schedule_time, msg, repeat)
    while True:
        diff = datetime.now() - schedule_time
        if diff.seconds < 1:
            send_tweet(msg, {'supress_message':False})

            # Tweet has been sent, program either terminates or increments the time for the next day
            if repeat:
                schedule_time = schedule_time + timedelta(days=1)
                msg = gen_msg(schedule_time)
                log_scheduled_tweet(schedule_time, msg, repeat)
            else:
                return
        await asyncio.sleep(1)
    
async def get_tweets_from_user(userId=36155411, screen_name="JeffProbst"):
    while True:
        tl = api.user_timeline(screen_name=screen_name)
        for tweet in tl:
            if tweet.created_at > epoch:
                delta = relativedelta(tweet.created_at, epoch)
                days = delta.days
                msg = f"Hey @JeffProbst , I've been tweeting for {days} days to remind you to put Mr. Tiveron on survivor. You should definitely consider him."
                tweet_id = tweet.id_str
                api.update_status(msg, tweet_id)
            await asyncio.sleep(0.1)
    await asyncio.sleep(30)
    



async def main(reminder="daily"):
    print(f"started at {time.strftime('/%X')}")

    if reminder == "daily":
        task1 = asyncio.create_task(
            schedule_tweet(hour=2+12, minute=17, second=0, msg="--reminder", repeat=True)
        )
        task2 = asyncio.create_task(
            get_tweets_from_user("JeffProbst")
        )

        await task1
        await task2
        

    print(f"finished at {time.strftime('/%X')}")

if __name__ == "__main__":
    asyncio.run(main())