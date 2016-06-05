

import os
import re
import praw
import datetime as dt

from config import user_agent, user_name, password

# App Constants
WATER_SUBMISSION_TIME_LIMIT = 3600
WATER_ME_SUBREDDIT = 'tylerjaywood_test'
TITLE_TRIGGER = '^water the plant\w*'
WATER_ME_USERNAME = 'takecareofmyplant'
WATER_ME_PASSWORD = 'hunter2'

# App setup
r = praw.Reddit(user_agent=user_agent)
r.login(user_name, password)
SUBREDDIT = r.get_subreddit(WATER_ME_SUBREDDIT)

if not os.path.isfile("recorded_submissions.txt"):
    recorded_submissions = []
else:
    with open("recorded_submissions.txt", 'r') as f:
        recorded_submissions = f.read()
        recorded_submissions = recorded_submissions.split("\n")
        recorded_submissions = filter(None, recorded_submissions)

# Useful functions
def is_trigger(submission):
    """takes a submission object, returns true if it's a watering proposal"""
    t = submission.title
    return True if re.match(TITLE_TRIGGER, t, re.IGNORECASE) else False

def get_trigger_submissions(subreddit_root, id_list):
    """move through new submissions
    return list of watering proposals"""
    gen_obj = subreddit_root.get_new()
    for submission in gen_obj:
        sub_obj = gen_obj.next()
        if sub_obj.id in id_list:
            break
        else:
            if is_trigger(sub_obj):
                id_list += [submission.id]
            else:
                continue


# STEP ONE
# Collect full list of water_submission ids
water_submissions = get_trigger_submissions(SUBREDDIT, recorded_submissions)
print water_submissions
# STEP TWO
# Load submissions as WaterProposal objects.
# If the expiration has passed, and is not closed, then resolve issue
# If expiration has passed, and is closed, ignore
# If expiration has not passed, ignore

# Class for water proposal submissions to track shit
class WaterProposal(object):
    def __init__(self, REDDIT, submission_id):
        self.r = REDDIT
        self.sub_id = submission_id
        self.sub_obj = self.r.get_submission(submission_id = self.sub_id)
        self.sub_time = None
        self.expiration = None
        self.is_expired = False
        self.creator = None
        self.comments = []
        self.score = None
        self.results = {}
        self.replied = False
    
    PROPOSAL_DURATION = 9993600
    YES = ['.*\w{,1}yes.*']
    NO = ['.*\w{,1}no.*']

    def prep_submission(self):
        self.sub_time = dt.datetime.fromtimestamp(self.sub_obj.created_utc)
        self.expiration = self.sub_time + dt.timedelta(0, self.PROPOSAL_DURATION)

        self.creator = self.sub_obj.author.name

    # Dealing with comments: 
    # Need to load them as part of the submission,
    # Script will run intermittently and assign a score to a top level comment
    # It will reply to that top-level comment with the score
    # Edits to the top-level comment should not change the decision
    
    def load_comments(self):
        """process comments eligible for decision"""
        comments_raw = self.sub_obj.comments
        for comment in comments_raw:
            if dt.datetime.fromtimestamp(comment.created_utc) <= self.expiration:
                self.comments.append(comment)
            else:
                None

    def get_comment_score(self, com_obj):
        """iterate through yes/no regex lists to score
        Returns a SCORE: 1, 0 , -1"""
        yes = [re.match(x, com_obj.body, re.IGNORECASE) for x in self.YES]
        no = [re.match(x, com_obj.body, re.IGNORECASE) for x in self.NO]
        
        if (len(yes) - yes.count(None)) > (len(no) - no.count(None)):
            score = 1
        elif (len(yes) - yes.count(None)) < (len(no) - no.count(None)):
            score = -1
        else:
            score = 0
        return score

    def already_counted(self, com_obj):
        """If bot has already replied to comment, it's been counted
        returns false"""
        repliers = [x.author.name for x in com_obj.replies]
        return self.r.user.name in repliers

    def reply_to_comment(self, comment, score):
        decision = 'water' if score > 0 else "don't water"
        body = """
        Thanks for your comment, this has been counted as a vote for:
        {0} the plant
        """.format(decision)
        comment.reply(body)

    def score_comments(self):
        for comment in self.comments:
            score = self.get_comment_score(comment)
            self.score += score
            if self.already_counted(comment):
                continue
            else:
                self.reply_to_comment(comment, score)

    def resolve_submission(self):
        if self.score > 0:
            decision = 'water the plant'
        else:
            decision = "don't water the plant"
        
        time = self.sub_time.strftime('%Y-%m-%d %H:%M:%S')+' UTC'
        exp_time = self.expiration.strftime('%Y-%m-%d %H:%M:%S')+' UTC'

        body = """
        This proposal to water the plant is closed. 
        Submission time: {0}
        Submitter: {1}
        Expiration time: {2}

        Decision: {3}

        Sending message "{3}" to the pump right now!"
        """.format(time, self.author, exp_time, decision) 

        self.sub_obj.add_comment(body)
        self.sub_obj.lock()


for submission in water_submissions:
    wp = WaterProposal(r, submission)
    wp.prep_submission
    if wp.sub_obj.locked:
        continue
    else:
        wp.score_comments()











