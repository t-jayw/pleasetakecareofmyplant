# Make a thread in the subreddit to get input on water/don't water 

import os
import praw

from datetime import datetime as dt

import config as c
import post_templates as posts
import gpio_out as g


REDDIT_USERNAME = 'takecareofmyplant'
REDDIT_PASSWORD = 'hunter2'

# Set-up
r = praw.Reddit(user_agent=c.user_agent)
r.login(c.user_name, c.password)
sr = r.get_subreddit(c.subreddit)

post_body = posts.body
post_title = posts.title

s = sr.submit(post_title, text=post_body)

s.sticky()

with open('/home/pi/pleasetakecareofmyplant/daily_thread.txt', 'w') as f:
    f.write(s.id)
    f.close()

with open('/home/pi/pleasetakecareofmyplant/topup.txt', 'r+') as f:
    x = f.read()
    if x == '1':
      g.on_off(10)    

