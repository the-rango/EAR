from flask import Flask, render_template, request
from urllib.parse import urlparse
import os
import redis

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    val = None
    if request.method == 'POST':
        url = urlparse(os.environ.get('REDISCLOUD_URL'))
        val = redis.Redis(host=url.hostname, port=url.port, password=url.password).get(request.form['key'])
    return render_template('db.html', val=val)
