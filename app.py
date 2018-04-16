from flask import Flask, render_template, request
from urllib.parse import urlparse
import os
import redis

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return 'Hi!'

@app.route('/rc', methods=['GET','POST'])
def rc():
    val = None
    if request.method == 'POST':
        url = urlparse(os.environ.get('REDISCLOUD_URL'))
        val = redis.Redis(host=url.hostname, port=url.port, password=url.password).get(request.form['key'])
    return render_template('rc_db.html', val=val)

@app.route('/rg', methods=['GET','POST'])
def rg():
    val = None
    if request.method == 'POST':
        url = urlparse(os.environ.get('REDISGREEN_URL'))
        val = redis.Redis(host=url.hostname, port=url.port, password=url.password).get(request.form['key'])
    return render_template('rg_db.html', val=val)
