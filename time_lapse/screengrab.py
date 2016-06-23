import requests
import os
import sys
sys.path.append("/home/pi/pleasetakecareofmyplant/")
import config as c

from secret import plant_cam_device_id, nest_api_auth
from post_templates import now_pst

path = c.pathPrefix()
url = "https://www.dropcam.com/api/wwn.get_snapshot/%s?auth=%s"%(plant_cam_device_id,
								 nest_api_auth)

r = requests.get(url)

img = r.content

print now_pst

file_name = str(now_pst) +"_screengrab.jpg"

with open(path+"time_lapse/captures/"+file_name, 'w') as f:
    f.write(img)
    f.close()


