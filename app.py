from flask import Flask, render_template, request
from urllib.parse import urlparse
import os
import redis

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return 'Hi!'

@app.route('/rtg', methods=['GET','POST'])
def rtg():
    val = None
    if request.method == 'POST':
        url = urlparse(os.environ.get('REDISTOGO_URL'))
        val = redis.Redis(host=url.hostname, port=url.port, password=url.password).get(request.form['key'])
    return render_template('rtg_db.html', val=val)

@app.route('/rg', methods=['GET','POST'])
def rg():
    val = None
    if request.method == 'POST':
        old_key = request.form['key']
        url = urlparse(os.environ.get('REDISTOGO_URL'))
        val = eval(redis.Redis(host=url.hostname, port=url.port, password=url.password).get(old_key))
        for thing in val.keys():
            new_key = (eval(old_key), eval(thing))
        url = urlparse(os.environ.get('REDISGREEN_URL'))
        val = str(redis.Redis(host=url.hostname, port=url.port, password=url.password).get(new_key))
    return render_template('rg_db.html', val=val)
