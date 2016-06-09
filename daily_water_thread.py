# Make a thread in the subreddit to get input on water/don't water 

import os
import praw

from datetime import datetime as dt

import config as c
import water_post_template as wpt

# Set-up
r = praw.Reddit(user_agent=c.user_agent)
r.login(c.user_name, c.password)
sr = r.get_subreddit(c.subreddit)

post_body = wpt.body
post_title = wpt.title

s = sr.submit(post_title, text=post_body)

s.sticky()

with open('/home/pi/daily_thread.txt', 'w') as f:
    f.write(s.id)
    

