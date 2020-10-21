import praw
import re
import base64
import threading
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

reddit = praw.Reddit(client_id=config.get("ACCOUNT", "CLIENT_ID"),
                     client_secret=config.get("ACCOUNT", "CLIENT_SECRET"),
                     username=config.get("ACCOUNT", "USERNAME"),
                     password=config.get("ACCOUNT", "PASSWORD"),
                     user_agent="Created by u/ItsTheRedditPolice")

subreddit = config.get("SUBREDDIT", "NAME")

user = reddit.user.me()

def find_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>" \
            r"]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    return [x[0] for x in url]

def encode_link(body, type):
    link = find_url(body)
    if len(link) <= 0:
        pass
    else:
        encoded_link = (base64.b64encode(bytes(link[0], "utf-8")))
        clean_encoded_link = str(encoded_link)[2:-1]
        type.reply(f"Here is the link encoded in base64: {clean_encoded_link}")
        print(f"[ALERT] Found a raw link and encoded it!")
        #print(f"Here is the link encoded in base64: {clean_encoded_link}")

def scan_comments():
    for comment in reddit.subreddit(subreddit).stream.comments(skip_existing=True):
        body = comment.body
        encode_link(body, comment)

def scan_submissions():
    for submission in reddit.subreddit(subreddit).stream.submissions(skip_existing=True):
        if submission.is_self:
            body = submission.selftext
            encode_link(body, submission)

def initialise():
    try:
        print(f"[STARTING] Initialising bot...")
        time.sleep(0.5)
        print(f"[ALERT] Logged in as {user}.")
        thread1 = threading.Thread(target=scan_submissions)
        thread2 = threading.Thread(target=scan_comments)
        thread1.start()
        thread2.start()
        time.sleep(1)
        print(f"[ALERT] Chosen Subreddit is r/{subreddit}")
        time.sleep(1)
        print("[ALERT] Bot has started!")
        print("---------------------------------------------\n")
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(f"[ERROR] The bot encountered an error!\n {e}\n\n")

initialise()