

import pickle
import json
import re
import time

import praw

import post_templates as posts
import config as c

# Setup
r = c.getReddit()
sr = c.getSubReddit(r, False)

path = c.pathPrefix()

## Get necessary files
# Comment log, in case one exists (vestigial file)
try:
    with open(path+'continuous_tally/cont_comment_log.txt', 'r+') as f:
        try:
            processed = pickle.load(f) 
        except EOFError:
            processed = []
        f.close()
except:
    processed = []

# Similar to above, if there is already a comment, it's written here
try:
    with open('cont_comment_id.txt', 'r') as f:
        update_comment = f.read()
        f.close()
except:
    update_comment = False

# Get the submission -- written by Daily Water thread script
with open(path+'daily_thread.txt', 'r+') as f:
    thread = f.read()
    f.close()

## Functions
def get_comment_score(x):
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
        comment.reply("1")
    elif score == -1:
        comment.reply("2")

def workNewComments(submission, record):
    done = [x[1] for x in record]
    voters = [x[2]+str(x[4]) for x in record]
    
    for x in s.comments:
        if not type(x) is praw.objects.Comment:
            s.get_more_comments(limit=10)
            workNewComments(s, record)
        if x.name in done:
            print('id')
            break
        score = get_comment_score(x)
        if x.author.name+str(score) in voters:
            print('name')
            continue
        if score == 0:
            continue
        tuple_log = (s.id, x.name, x.author.name, x.body, score)
        #reply_to_vote(x, score)
        record = [tuple_log] + record
        voters = [x.author.name+str(score)] + voters
    return record

def getScores(record=processed):
    y = 0
    n = 0
    for x in processed:
        if x[4] == 1:
            y += 1
        elif x[4] == -1:
            n += 1
    return y, n

def makeBars(yes, no):
    yes_pct = yes*100/(yes + no)
    no_pct = 100 - yes_pct

    yes_bar = "`Y`: `"+"|"*(yes_pct/2)+"` (%d)"%(yes)
    no_bar = "`N `:     `"+"|"*(no_pct/2)+"` (%d)"%(no)
    return yes_bar, no_bar

# WHO RUN IT
s = r.get_submission(submission_id = thread)

it = 0

while it <= 240:
    processed = workNewComments(submission=s,record=processed)
    yes, no = getScores()
    yes_bar, no_bar = makeBars(yes, no)
    
    continuous_score_body = posts.continuous_vote_display%(yes_bar, no_bar)

    if not update_comment:
        update = s.add_comment(continuous_score_body)
    else:
        update = r.get_info(thing_id = update_comment)
        update.edit(continuous_score_body)
    
    update.distinguish(sticky=True)
    time.sleep(300)
    it += 1

with open('cont_comment_log.txt', 'w') as f:
        pickle.dump(processed, f)

with open('cont_comment_id.txt', 'w') as f:
    f.write(update.name)

