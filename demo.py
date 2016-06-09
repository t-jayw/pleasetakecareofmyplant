import requests

import gpio_out

url = 'http://www.pleasetakecareofmyplant.com/demo.html'

r = requests.get(url)

if r.content == 'yep':
    gpio_out.on_off()
else:
    None
