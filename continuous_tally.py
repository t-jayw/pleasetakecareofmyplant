# Currently, in the workNewComments function, it handles comment loading well
# It will load comments sequentially and breaks when at where it left off
# Does not handle 1/vote per person due to 'voter' list not updating with 
#   each iteration of the loop through s.comments

import pickle
import json
import re

import praw

import config as c

# Setup
r = c.getReddit()
sr = c.getSubReddit(r)

path = c.pathPrefix()

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

with open(path+'cont_comment_log.txt', 'r+') as f:
    try:
        processed = pickle.load(f) 
    except EOFError:
        processed = []

# Get the submission
with open(path+'daily_thread.txt', 'r+') as f:
    thread = f.read()
    f.close()

s = r.get_submission(submission_id = thread)

def workNewComments(submission=s, record=processed):
    done = [x[1] for x in record]
    print(str(done))
    voters = [x[2]+str(x[4]) for x in record]
    for x in s.comments:
        if not type(x) is praw.objects.Comment:
            s.get_more_comments(limit=10)
            workNewComments(s, record)
        if x.name in done:
            print('id')
            break
        if x.author.name in voters:
            print('name')
            continue
        score = get_comment_score(x)
        if score == 0:
            continue
        tuple_log = (s.id, x.name, x.author.name, x.body, score)
        reply_to_vote(x, score)
        record = [tuple_log] + record
    print(record)
    return record

processed = workNewComments()

def getScores(record = processed):
    y = 0
    n = 0
    for x in processed:
        if x[4] == 1:
            y += 1
        elif x[4] == -1:
            n += 1
    return y, n

yes, no = getScores()

print str(yes) + "\n" + str(no)

with open('cont_comment_log.txt', 'w') as f:
    pickle.dump(processed, f)

    


    






