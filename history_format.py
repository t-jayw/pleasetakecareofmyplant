import config as c

with open("/home/pi/pleasetakecareofmyplant/history.txt") as f:
  h = f.readlines()

h = [x.strip().split(',') for x in h]
h = h[-7:]

# today = [['today', '', '']]


header = '|'.join(x[0] for x in h)

cells = '-'+'--,'*len(h)
cells = cells.split(',')
cells = cells[0:-1]
cells = '|'.join(cells)

decisions = '|'.join(x[1] for x in h)
threads = '|'.join(x[2] for x in h)

def format_threads(x):
    url = 'https://www.reddit.com/r/%s/comments/%s/'%(c.subreddit, x)
    return "[thread](%s)"%(url)

threads = '|'.join(format_threads(x[2]) for x in h)


history_table = '\n'.join([header,cells,decisions,threads])


