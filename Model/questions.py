import urllib.parse, urllib.request, urllib.error
import json
import translate


def openURL(url: str) -> dict:
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    response = json.loads(data)
    if response["response_code"] == 0:
        return response
    # TODO add other response codes
    raise Exception("Something went Wrong")


def getSessionToken() -> str:
    """
    Returns a session Token which is valid for 6h
    :return: Token
    """
    url = "https://opentdb.com/api_token.php?command=request"
    response = openURL(url)
    return response["token"]


def getQ(diff: str, cat: int, token: str) -> dict:
    """
    Function to get Questions from the db
    :param diff: difficulty can be "easy", "medium", "hard"
    :param cat: category, all categories can be found here: https://opentdb.com/api_category.php
    :param token: session Token from getSessionToken
    :return: Dict with category, type, difficulty, question, correct_answer and incorrect_answers
    """
    url = "https://opentdb.com/api.php?"
    url = url + urllib.parse.urlencode({"amount": 1, "difficulty": diff, "category": cat, "type": "multiple",
                                        "token": token})
    response = openURL(url)
    return response["results"][0]

# Test
getQ("hard", 9, "fd9d2541116a22530350997198b2a964be6ed944a0ca31b0c71bf7516dd95bfa")
