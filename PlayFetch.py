import Doggo
import redis
import os
import datetime

meta = redis.from_url(os.environ.get('REDISTOGO_URL'))
store = redis.from_url(os.environ.get('REDISGREEN_URL'))

doggo = Doggo.Retriever()

for gvkey in meta.scan_iter():
    handles = eval(meta.get(gvkey))    

    for user, latest in handles.items():
        try:
            tweets = eval(store.get(user))
            if tweets == None:
                tweets = {}
                print('tis none')
        except:
            tweets = {}
        new_id = None
        try:
            for tweet in doggo.get_tweets(user, latest):
                if new_id == None:
                    new_id = tweet[0]
                tweets[tweet[0]] = tweet[1:]
                store.set(user, tweets)
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
            
log = redis.from_url(os.environ.get('REDIS_URL'))
try:
    history = log.get('log')
    if history == None:
        history = ''
except:
    history = ''
    
history += bytes(str(datetime.date.today()), 'utf-8')
history += bytes(': Done', 'utf-8')
log.set('log', history)
print('Done')
