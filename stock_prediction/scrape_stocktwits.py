import sys
import requests
import lxml.html
import json
import re
import random
import time
from datetime import datetime

# scrapes n days of Stocktwits feed
def scrape(symbol, n):
    s = requests.Session()
    r = s.get("http://stocktwits.com/symbol/" + symbol)
    e = lxml.html.fromstring(r.text)
    csrf_token = e.xpath('//meta[@name="csrf-token"]/@content')[0]
    scripts = e.xpath("//script")
    for script in scripts:
        if "max_id" in str(script.text):
            max_id  = int(re.findall("max_id: (\d+),", script.text)[0])
            item_id = int(re.findall("poll_id: '(\d+)',", script.text)[0])

    s.headers = {'X-CSRF-Token': csrf_token,
                 'X-Requested-With':'XMLHttpRequest'}

    messages = []
    current_time = datetime.now()
    days_so_far = 0

    while days_so_far < n:
        r = s.get("http://stocktwits.com/streams/poll?stream=symbol&stream_id={}&max={}&substream=top&item_id={}".format(item_id,max_id, item_id))
        j = json.loads(r.text)

        temp = j['messages']
        for t in temp:
            del t["avatar_url"]
            del t["avatar_url_ssl"]
            del t["latest_likes"]
            del t["user_path"]

        messages.extend(temp)
        max_id = j['max']

        time_so_far = datetime.strptime(temp[-1]['created_at'], '%a, %d %b %Y %H:%M:%S -0000')
        days_so_far = (current_time - time_so_far).days

        print "{} total\t{} days\t{}".format(len(messages), days_so_far, temp[-1]['created_at'])
        time.sleep(random.random() * 0.25 + 0.15)

    return messages

if __name__ == "__main__":
#    dow = ["BA","TSLA","CSCO","IBM","INTC","JNJ","MRK","MSFT","PFE","UNH","UTX","VZ","GOOG"]
    dow = ["GOOG"]
    for symbol in dow:
        messages = scrape(symbol, 730)

        with open('data/twits730/'+symbol+'.txt', 'w') as outfile:
            json.dump(messages, outfile)
