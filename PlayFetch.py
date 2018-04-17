import Doggo
import redis

url = urlparse(os.environ.get('REDISTOGO_URL'))
meta = redis.Redis(host=url.hostname, port=url.port, password=url.password)

url = urlparse(os.environ.get('REDISGREEN_URL'))
store = redis.Redis(host=url.hostname, port=url.port, password=url.password)

def parse_username(url):
    if '"' == url[0]:
        url =  url[1:]
    if '"' == url[-1]:
        url = url[:-1]
    if 'twitter.com' not in url:
        raise Exception('wtf')
    beg = url.find('https://twitter.com/')
    end = url.find('?')
    if end == -1:
        result = url[beg+20:]
    else:
        result = url[beg+20:end]
    if '/' in result:
        if result[-1] == '/':
            result = result[:-1]
        else:
            raise Exception('wtf')
    return result

doggo = Doggo.Retriever()

for gvkey in meta.scan_iter("user:*"):
    handles = eval(meta.get(gvkey))
    tweets = {}
    try:
        test = handles.keys()
    except:
        continue
    for handle, l_id in handles.items():
        if len(handle.split('/')) == 2:
            print('n/a found')
            continue

        try:
            handle = parse_username(handle.strip())
        except:
            print('bad url: {}'.format(handle), end='')
            continue

        try:
            for tweet in doggo.get_tweets(handle):
                tweets[tweet[0]] = tweet[1:]
        except Exception as e:
            print(e)
            continue        
            
    store.set(gvkey, tweets)
