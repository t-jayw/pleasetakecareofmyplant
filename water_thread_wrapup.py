# Tally the votes in the daily water thread

import os
import praw
import re
import time

from datetime import datetime as dt

import gpio_out as g
import config as c
import post_templates as posts

# Set-up
r = praw.Reddit(user_agent=c.user_agent)
r.login(c.user_name, c.password)
sr = r.get_subreddit(c.subreddit)

with open('/home/pi/pleasetakecareofmyplant/daily_thread.txt', 'r+') as f:
    thread = f.read()
    f.close()


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
recorded_yes = {}
recorded_no ={}

for x in comments:
    score = get_comment_score(x)
    tuple_log = (s.id, x.name, x.author.name, x.body, score)
    if score == 1:
        d = recorded_yes
    elif score == -1:
        d = recorded_no
    else:
        continue
    if not d.has_key(tuple_log[2]):
        d[tuple_log[2]] = tuple_log
        reply_to_vote(x, tuple_log[4])

total = len(recorded_yes) - len(recorded_no)

self_text = s.selftext
wrapup = posts.body_edit.format(posts.now_formatted, len(recorded_yes), len(recorded_no))

wrapup = self_text + "\n **** \n" + wrapup

print total
print wrapup


# Reply to submission
if total > 0:
    s.edit(wrapup)
    time.sleep(600)
    g.on_off(20) 
else:
    s.edit(wrapup)

with open('/home/pi/pleasetakecareofmyplant/yes_votes.txt', 'a+') as f:
    f.write(str(recorded_yes))
    f.close()

with open('/home/pi/pleasetakecareofmyplant/no_votes.txt', 'a+') as f:
    f.write(str(recorded_no))
    f.close


