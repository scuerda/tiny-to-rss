from bs4 import BeautifulSoup
from flask import Flask, request, render_template
from werkzeug.contrib.atom import AtomFeed
import requests
from dateutil import parser
import os

app = Flask(__name__)

feed_lookup = {
    'data_is_plural': {
        'url': 'https://tinyletter.com/data-is-plural/archive?recs=5&sort=desc&q=',
        'feed_name': 'Data Is Plural',
        'author': 'Jeremy Singer Vine'
    }
}

def build_feed(feed_record, full=False):
    feed = AtomFeed(title=feed_record.get('feed_name'),
                    title_type='text',
                    author=feed_record.get('author'),
                    feed_url=request.url, url=request.url_root)

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
            content = requests.get(link)
            feed.add(title, content=content.content, content_type='html',
                     summary=snippet, summary_type='text', url=link, updated=date_item)
        else:
            feed.add(title, snippet, content_type='text', url=link, updated=date_item)
    return feed.get_response()


@app.route('/feeds/summary/<feed_name>')
def summary_feed(feed_name):
    feed_record = feed_lookup.get(feed_name)
    return build_feed(feed_record)

@app.route('/feeds/full/<feed_name>')
def full_feed(feed_name):
    feed_record = feed_lookup.get(feed_name)
    return build_feed(feed_record, full=True)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)