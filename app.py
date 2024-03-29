#!/usr/bin/env python


import requests
from flask import Flask, Response,json,request
from flask import jsonify
from BeautifulSoup import *
from models.link import Link
from flask.ext.jsonpify import jsonify

from werkzeug.contrib.fixers import ProxyFix

import json
import re




app = Flask(__name__)
SECRET_KEY = "0219"
app.config.from_object(__name__)
body = None
link = Link()


def jsonp(data,callback = "function"):
    return Response(
            "%s(%s);" %(callback,json.dumps(data)),
            mimetype="text/javascript"
            )


def is_valid_link(link):
    match = re.match(r'.*\.html',str(link))
    if match:
        return True
    return False


def fetch_news():
    r = requests.get("http://javascriptweekly.com/archive/")
    body = r.content
    soup = BeautifulSoup(body)
    links = soup.findAll("a")
    res = []
    for link in links:
        if is_valid_link(link):
            res.append(link)
    return sorted_links(links)

## append links to link.objects
def inject_links(links):
    for l in links:
        tmp  =  re.split(r'<a\shref=',str(l))
        number =  re.sub(r'\.*html','',tmp[1]).split(">")[0]
        if not re.match(r'"\/"',str(number)):
            link.objects.append(
                    {"number": int(number.strip('"')),
                        "body": l}
                    )

## set link.objects order by newest.
def sorted_links(links):
    inject_links(links)
    link.objects = sorted(link.objects,key = lambda link_obj:link_obj["number"])
    return link.objects

def latest_link():
    latest = link.objects.pop()
    return latest




@app.route("/")
def hello():
    return "hellooo"

# return fetch latest_number take argument as <int:news_id>.html
@app.route("/latest_number")
def latest_number():
    fetch_news()
    last = link.objects.pop()
    return jsonify(data = str(last["number"]))


@app.route("/api/latest")
def l():
    fetch_news()
    last = link.objects.pop()
    callback = request.args.get("callback")
    data = {"content": last["number"]}
    if callback:
        return jsonp(data,callback)
    return jsonp(data)

@app.route("/api/latest/<int:article_id>")
def latest(article_id):
    callback = request.args.get("callback")

    if not link.objects:
        fetch_news()
    link.current_news = link.objects.pop()
    link.format(link.current_news,article_id)

    data = {"content": link.weekly_news}
    return jsonify(user="haha")

@app.route("/latest/<int:article_id>")
def latest(article_id):
    if not link.objects:
        fetch_news()
    link.current_news = link.objects.pop()
    link.format(link.current_news,article_id)
    return jsonify(data=link.weekly_news)




app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=3000)
