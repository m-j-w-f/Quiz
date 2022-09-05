import html
import json
import urllib.error
import urllib.parse
import urllib.request


def openURL(url: str) -> dict:
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    data = html.unescape(data)
    response = json.loads(data)
    return response
