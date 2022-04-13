import urllib.parse, urllib.request, urllib.error
import json
import html


def openURL(url: str) -> dict:
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    data = html.unescape(data)
    response = json.loads(data)
    if response["response_code"] == 0:
        return response
    # TODO add other response codes
    raise Exception("Something went Wrong")