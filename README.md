## Welcome

This is a simple, Flask-based API that proxies TinyLetter archives into a Atom
feed, suitable for use with feed readers. The inspiration from this came from a
tweet from [Lou Huang](https://github.com/louh).

### Configuration

None required. The proxy API will scrape author, title and TinyLetter descriptions and populate accordingly.


### Use

The API exposes endpoints for summaries feeds and full record feeds. Both endpoints take a "slugged" feed name.

For example, if you want to generate a feed for `https://tinyletter.com/data-is-plural/archive`, you would use
`data-is-plural` as the `feed_name` parameter. 

 You can also pass an optional count of results to fetch. TinyLetter returns a minimum of 10 results when displaying 
 the archive, so any count less than 10 will have no effect.

**Summary Feed**

The summary endpoint will return a feed with a short description of each letter's content.

* **URL**

  `/feeds/summary/:feed_name/:count/`
  `/feeds/summary/:feed_name/`

* **Method:**

  `GET`
  
* **URL Params**

  **Required**
  
  `feed_name=[string]`
  
  **Optional**
  
  `count=[int]`
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** ATOM XML Document
 

**Full Feed**

The full end point will return the full content of the letter itself.

* **URL**

  `/feeds/full/:feed_name/:count/`
  `/feeds/full/:feed_name/`

* **Method:**

  `GET`
  
* **URL Params**

  **Required**
  
  `feed_name=[string]`
  
  **Optional**
  
  `count=[int]`
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** ATOM XML Document
    
    
### Deployment

As this is a standard, WSGI-based Flask app, it can be packaged and deployed anywhere that can
host and serve Python web applications. That said, this is an ideal application for deploying to AWS Lambda using
[zappa](https://github.com/Miserlou/Zappa)

Zappa configuration and deployment is fairly straightforward.

Configuring a IAM role for the application can be a bit tricky. The Zappa documentation is slightly vague on how to best
grant permissions, partially due to the security implications. That said, [this](https://github.com/Bartvds/Zappa/blob/6f6f52eb01976c2390c24ef2b40c5c43c35ad8e5/example/policy/deploy.json)
is an example policy that will allow you to deploy this application with Zappa.

The steps required before running Zappa, include setting up an IAM Role, downloading and installing the AWS credentials
in a local credentials file (likely located at `~/.aws/credentials`), and then attaching a policy to that role.

The policy linked to above requires a few edits. You'll need to fill in the name of the s3 bucket that you intend to use. 
This bucket should also be specified in the `zappa_settings.json` file that will be generated after running `zappa init`. 
You'll also need to fill in your AWS account id. 

 