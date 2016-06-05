### This is to generate the text of daily water-decision post

import config 
import requests
import datetime

from datetime import datetime as dt

# Date time set up
date_format = '%H:%M:%S PST'
title_format = '%Y-%m-%d'
now = dt.now()
now_formatted = now.strftime(date_format)
end_time = now + datetime.timedelta(0, 12*3600)
end_time_formatted = end_time.strftime(date_format)

# Weather update
api = config.weather_api
url = 'http://api.openweathermap.org/data/2.5/weather?zip={ZIP},us&APPID={APIKEY}'
url = url.format(ZIP=config.zipcode, APIKEY=api)
r = requests.get(url)
description = r.json()['weather'][0]['description']

title = """
Do you want to water the plant today? {0}
"""
title = title.format(now.strftime(title_format))
body = """
Hello! 

It is **{0}** in California.
The weather report today calls for: *{1}*.

This thread will close in **12** hours, at which time all top-level comments
will be assessed as votes in favor of watering the plant, or not. 

**VOTING**
Comment 'Yes' or 'No'

The decision will be made at {2}, and this thread will be updated, and locked
at that time.
"""

body = body.format(now_formatted, description, end_time_formatted)

