import os
from urllib.parse import urlparse
import redis

url = urlparse(os.environ.get('REDISCLOUD_URL'))

r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

r.set('Shijia', 'Lorolana')

print('done')
