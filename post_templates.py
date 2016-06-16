### This is to generate the text of daily water-decision post
import requests
import datetime
import pytz

from datetime import datetime as dt
from pytz import timezone

import config as c
import secret
import history_format as hf

# Date time set up
date_format = '%H:%M:%S PST'
title_format = '%Y-%m-%d'
PST = timezone('US/Pacific')

utc_now = dt.now(tz=pytz.utc)
now_pst = utc_now.astimezone(PST)

def ord(n):
    if 4<=n%100<=20:
        return str(n)+"th"
    else:
        return str(n)+{1:"st",2:"nd",3:"rd"}.get(n%10,"th")

ord_date = ord(int(now_pst.strftime('%-d')))

now_formatted = now_pst.strftime(date_format)
end_time = now_pst + datetime.timedelta(0, 20*3600)
end_time_formatted = end_time.strftime(date_format)

# Weather update
url = 'http://api.openweathermap.org/data/2.5/weather?zip={ZIP},us&APPID={APIKEY}'
url = url.format(ZIP=secret.zipcode, APIKEY=secret.weather_api)
r = requests.get(url)
description = r.json()['weather'][0]['main']

# Daily Water Thread
title = """
Today is {0}, {1} {2}. Do you want to water the plant today? 
"""

title = title.format(now_pst.strftime('%A'),
                     now_pst.strftime('%B'), 
                     ord_date) 
                    
history = hf.history_table

body = """
Hello, and thanks for taking care of my plant! 

It is **{0}** in California and the weather report today calls for: *{1}*.


If you think that the plant should be watered today, please comment `yes` on
this post. If you think that plant should not be watered today, please comment
`no` below. 


When this post is 20 hours old, at **{2}**, this post will be locked.
u/takecareofmyplant will tally all the `yes` or `no` votes in top level comments
on this thread. 

If `yes` is the majority, u/takecareofmyplant will turn on the
pump and water the plant. If not, we will check in again tomorrow!


**To help take care of my plant, please vote below!**

****

>>Watering Decisions Past 7 Days

{3}
"""

body = body.format(now_formatted, description, end_time_formatted, history)

# Wrapup
body_edit = """
Hello again, it is **{0}** and I've just finished counting your votes.


Here are the results:


Yes | No
---|--
{1} | {2}


If `Yes` votes are in the majority, the following will take place:


* The pump will be switched on in 10 minutes for 15 seconds, dispensing ~150ml of water
* In 14 hours, the pump will be switched on again for another 10  seconds, dispensing ~100ml of water


Try to catch it on the [PLANT CAM](http://www.pleasetakecareofmyplant.com)! 


Thanks for taking care of my plant!
"""

continuous_vote_display = """

%s

%s

""".format(now_formatted)

