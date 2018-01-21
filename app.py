import os

from bs4 import BeautifulSoup
from flask import Flask, request, Response
import requests
import feedgenerator
from dateutil import parser

from .letters_to_proxy import feed_lookup

app = Flask(__name__)

def build_feed(feed_record, full=False):
    """Takes a feed_record extracted from feed_lookup and generates an RSS feed

    :param feed_record: dict
    :param full: boolean
    :return:
    """
    feed = feedgenerator.Atom1Feed(
        title=feed_record.get('feed_name'),
        description='',
        author_name=feed_record.get('author'),
        link=request.url)

    response = requests.get(feed_record.get('url'))
    archive_content = response.content

    soup = BeautifulSoup(archive_content, 'html.parser')
    raw_feed_items = soup.find_all('li', class_='message-item')

    for fi in raw_feed_items:
        date_item = parser.parse(fi.find(class_='message-date').text)
        link = fi.find(class_='message-link').attrs['href']
        title = fi.find(class_='message-link').find('span').text
        snippet = fi.find(class_='message-snippet').text
        if full:
            # SLOW. Will want to implement some sort of dumping / caching via tinydb or the like
            # Will also want to implement some sort of thread pool or maybe an async co-routine to
            # speed up the fetching of pages
            content = requests.get(link)
            full_content_soup = BeautifulSoup(content.content, 'html.parser')
            feed.add_item(title, link, snippet, content=full_content_soup.__repr__(), pubdate=date_item)
        else:
            # feed.add(title, snippet, content_type='text', url=link, updated=date_item)
            feed.add_item(title, link, snippet, content=snippet, pubdate=date_item)
    return feed

@app.route('/feeds/summary/<feed_name>')
def summary_feed(feed_name):
    """Short form of feed. Does not follow link to extract full content"""
    feed_record = feed_lookup.get(feed_name)
    feed_result = build_feed(feed_record)
    return Response(feed_result.writeString(encoding='utf-8'), mimetype='text/xml')

@app.route('/feeds/full/<feed_name>')
def full_feed(feed_name):
    """Long feed format. Loops over each record and fetches the full letter"""
    feed_record = feed_lookup.get(feed_name)
    feed_result = build_feed(feed_record, full=True)
    return Response(feed_result.writeString(encoding='utf-8'), mimetype='text/xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)