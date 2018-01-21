import os

from bs4 import BeautifulSoup
from flask import Flask, request, Response
import requests
import feedgenerator
from dateutil import parser

feed_lookup = {
    'data-is-plural': {
        'url': 'https://tinyletter.com/data-is-plural/archive',
        'feed_name': 'Data Is Plural',
        'author': 'Jeremy Singer Vine'
    }
}

app = Flask(__name__)

def build_feed(feed_record, full=False, count=None):
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

    count = count if count else 10
    base_feed_url = feed_record.get('url')
    response = requests.get(base_feed_url, params={'recs': count, 'sort': 'desc', 'page': 1, 'q': None})
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

@app.route('/feeds/summary/<str:feed_name>/<int:count>/')
@app.route('/feeds/summary/<str:feed_name>/')
def summary_feed(feed_name, count=None):
    """Short form of feed. Does not follow link to extract full content"""
    feed_record = feed_lookup.get(feed_name)
    feed_result = build_feed(feed_record, count=count)
    return Response(feed_result.writeString(encoding='utf-8'), mimetype='text/xml')

@app.route('/feeds/summary/<str:feed_name>/<int:count>/')
@app.route('/feeds/full/<str:feed_name>/')
def full_feed(feed_name, count=None):
    """Long feed format. Loops over each record and fetches the full letter"""
    feed_record = feed_lookup.get(feed_name)
    feed_result = build_feed(feed_record, full=True, count=count)
    return Response(feed_result.writeString(encoding='utf-8'), mimetype='text/xml')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)