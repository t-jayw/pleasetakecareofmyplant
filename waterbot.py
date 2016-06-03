

import os
import re
import praw

from config import user_agent, user_name, password

# App Constants
WATER_SUBMISSION_TIME_LIMIT = 3600
WATER_ME_SUBREDDIT = 'tylerjaywood_test'
TITLE_TRIGGER = 'Water the plant'

# App setup
r = praw.Reddit(user_agent=user_agent)
r.login(user_name, password)
subreddit_root = r.get_subreddit(WATER_ME_SUBREDDIT)

if not os.path.isfile("water_submissions.txt"):
    water_submissions = []
else:
    with open("water_submissions.txt", 'r') as f:
        water_submissions = f.read()
        water_submissions = water_submissions.split("\n")
        water_submissions = filter(None, water_submissions)

# Useful functions
def is_trigger(submission):
    """takes a submission object, returns true if it's a watering proposal"""
    t = submission.title
    return True if re.match(TITLE_TRIGGER, t, re.IGNORECASE) else False

def water_submission_closed(submission):
    """Checks if submission is created w/in time limit"""
    None

# Pull new watering submissions and record them
for submission in subreddit_root.get_new():
    if is_trigger(submission):
        if submission.id not in water_submissions:
            water_submissions += [submission.id]
        elif submission.id in water_submissions:
            break
        else:
            continue

with open("water_submissions.txt", 'w') as f:
    for id in water_submissions:
        f.write(id + "\n")

# Iterate through, check if submission thread is still active
#for submission in water_submissions:
#    if !water_submission_closed...







