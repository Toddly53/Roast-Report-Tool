# Import packages.
import requests
from lxml import html


# A function log into Roastlog.com and return the session.
def login(url, username, password):

    # Initialize session.
    session = requests.session()
    
    # Get login csrf token.
    result = session.get(url)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    
    # Create payload with token.
    payload = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': authenticity_token
            }
    
    # Perform login.
    session.post(url, data = payload, headers = dict(referer = url))
    
    # Return the session.
    return session