import os
from urllib.parse import urlparse
import redis

url = urlparse(os.environ.get('REDISTOGO_URL'))

r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

for gvkey in r.scan_iter():
    handles, l_id = r.get(gvkey)
    if len(handles) == 1:
        r.set(gvkey, {handles[0]:l_id})

print('done')
