import Doggo
import redis
import os
from urllib.parse import urlparse

meta = redis.from_url(os.environ.get('REDISTOGO_URL'))
# url = urlparse(os.environ.get())
# meta = redis.Redis(host=url.hostname, port=url.port, password=url.password)

store = redis.from_url(os.environ.get('REDISGREEN_URL'))
# url = urlparse(os.environ.get())
# store = redis.Redis(host=url.hostname, port=url.port, password=url.password)

doggo = Doggo.Retriever()

for gvkey in meta.scan_iter():
    try:
        handles = eval(meta.get(gvkey))
    except:
        continue

    tweets = {}

    for user, latest in handles.items():
        new_id = None
        try:
            for tweet in doggo.get_tweets(user, latest):
                if new_id == None:
                    new_id = tweet[0]
                tweets[tweet[0]] = tweet[1:]
                store.set((gvkey, user), tweets)
            if new_id != None:
                old_info = eval(meta.get(gvkey))
                print(old_info)
                old_info[user] = new_id
                meta.set(gvkey, old_info)
                if new_id < latest:
                    print('Houston we have a problem')
        except Exception as e:
            print('Out loop exception: {}'.format(e))
            continue        
