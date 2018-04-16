import os
from urllib.parse import urlparse
import redis

url = urlparse(os.environ.get('REDISTOGO_URL'))

r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

r.flushall()

r.set('Shijia', 'Lorolana')

print('done')
