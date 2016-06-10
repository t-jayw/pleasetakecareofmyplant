# Tally the votes in the daily water thread

import os
import praw
import re

from datetime import datetime as dt

import gpio_out as g
import config as c
import water_post_template as wpt

# Set-up
r = praw.Reddit(user_agent=c.user_agent)
r.login(c.user_name, c.password)
sr = r.get_subreddit(c.subreddit)

with open('/home/pi/daily_thread.txt', 'r+') as f:
    thread = f.read()

s = r.get_submission(submission_id = thread)
s.lock()
s.unsticky()

# pull top-level comments and calculate score
comments = s.comments

def get_comment_score(comment):
    yes = re.search(r'\byes\b', x.body, re.IGNORECASE)
    no = re.search(r'\bno\b', x.body, re.IGNORECASE)
    if yes and no:
        return 0
    elif yes: 
        return 1
    elif no:
        return -1
    else:
        return 0

def reply_to_vote(comment, score=None):
    score = get_comment_score(comment) if (not score) else score
    if score == 0:
        return None
    elif score == 1:
        comment.reply("thanks, I've recorded your vote to water!")
    elif score == -1:
        comment.reply("thanks, I've recorded your vote to not water!")

# Record comments
tuple_log = []
for x in comments:
    score = get_comment_score(x) 
    tuple_log += [(s.id, x.name, x.author.name, x.body, score)]
    reply_to_vote(x, score)

print tuple_log

# Tally votes
total = 0
for t in tuple_log:
    total += t[4]

# Reply to submission
if total > 0:
    s.edit('water!')
    g.on_off()
else:
    s.edit('no water')

with open('/home/pi/comment_vote_log.txt', 'a+') as f:
    f.write(str(tuple_log))


