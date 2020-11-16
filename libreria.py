import urllib
import oauth2
import requests

CONSUMER_KEY = '' # chiedere
CONSUMER_SECRET = '' # chiedere


def oauth_req(url, key, secret, http_method="GET", post_body=b"", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url,
                                   method=http_method,
                                   body=post_body,
                                   headers=http_headers )
    return content


def request_oauth_token():
    # Create your consumer with the proper key/secret.
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)

    # Request token URL for Twitter.
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob"

    # Create our client.
    client = oauth2.Client(consumer)

    params = {
        'oauth_callback': 'oob'
    }
    encoded_query = urllib.parse.urlencode(params)

    headers = {'Authorization': 'oauth_callback="oob"'}

    # The OAuth Client request works just like httplib2 for the most part.
    resp, content = client.request(request_token_url, "GET", headers=headers)
    content = (content.decode("utf-8")).split('&')
    content = list(map(lambda x: x.split('='), content))
    return content


def access_token(oauth_token, oauth_verifier_pin):
    access_token_url = "https://api.twitter.com/oauth/access_token?oauth_token="+oauth_token+\
                       "&oauth_verifier="+oauth_verifier_pin

    content = requests.post(access_token_url).text
    content = list(map(lambda x: x.split('='), content.split('&')))
    return content


request_tokens = request_oauth_token()
#print (request_tokens)
url_for_pin = "https://api.twitter.com/oauth/authorize?oauth_consumer_key="+CONSUMER_KEY+\
              "&oauth_nonce="+oauth2.generate_nonce(13)+"&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&" \
                "oauth_token="+request_tokens[0][1]
print(url_for_pin)

oauth_pin = input('Inserisci pin: ')
access_tokens = access_token(request_tokens[0][1], oauth_pin)
print(access_tokens)

home_timeline = oauth_req( 'https://api.twitter.com/1.1/direct_messages/events/list.json',
                           '31078625-6MkpqGhgQGvgGsDjUMzzA6SJvYr8IBkX8O3AMzjsB',
                           '' ) # chiedere

print(home_timeline)