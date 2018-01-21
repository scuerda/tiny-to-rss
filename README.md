## Welcome

This is a simple, Flask-based API that proxies TinyLetter archives into a Atom
feed, suitable for use with feed readers. The inspiration from this came from a
tweet from [Lou Huang](https://github.com/louh).

### Configuration

Links to TinyLetter archives can be added as entries in the `letters_to_proxy.py`
file.

### Use

The API exposes two endpoints: 

Summary Feeds: `/feeds/summary/<feed_name>`

Full Feeds: `'/feeds/full/<feed_name>`

Passing the key for the given feed (as specified in the `letters_to_proxy.py` file) will 
return serialized feed data for the requested TinyLetter. 

This allows configuring separate URLs in a feed reader for each TinyLetter you want to follow.

### Deployment

As this is a standard, WSGI-based Flask app, it can be packaged and deployed anywhere that can
host and serve Python web applications. That said, this is an ideal application for deploying to AWS Lambda using
[zappa](https://github.com/Miserlou/Zappa)

More details on ideal zappa config coming soon...

 