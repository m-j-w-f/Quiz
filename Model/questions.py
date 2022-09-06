from Model.helpers import openURL
from random import randint
import urllib.parse
from Model.translate import translateT


class Question:

    @staticmethod
    def getSessionToken() -> str:
        """
        Returns a session Token which is valid for 6h
        :return: Token
        """
        url = "https://opentdb.com/api_token.php?command=request"
        response = openURL(url)
        return response["token"]

    @staticmethod
    def getCategories():
        url = "https://opentdb.com/api_category.php"
        response = openURL(url)
        return {x["name"]: x["id"] for x in response["trivia_categories"]}

    def __init__(self, diff: str, cat: int, token: str):
        """
        Function to get Questions from the db and initialize Question
        :param diff: difficulty can be "easy", "medium", "hard"
        :param cat: category, all categories can be found here: https://opentdb.com/api_category.php
        :param token: session Token from getSessionToken
        """

        url = "https://opentdb.com/api.php?"
        url = url + urllib.parse.urlencode({"amount": 1, "difficulty": diff, "category": cat, "type": "multiple",
                                           "encoding": "base64", "token": token})
        response = None
        while response is None:
            try:
                response = openURL(url)
            except Exception:
                pass
        self.full = response["results"][0]
        self.question = self.full["question"]
        self.correct_answer = self.full["correct_answer"]
        self.answers = self.full["incorrect_answers"]
        # Create shuffled answers
        idx = randint(0, len(self.answers))
        self.answers.insert(idx, self.correct_answer)
        self.correct_index = idx
        self.translated = False

    def __str__(self):
        s = self.question + "\n"
        c = ord("A")
        for a in self.answers:
            s += "(" + chr(c) + ") " + a + "   "
            c += 1
        return s

    def translateQ(self):
        if not self.translated:
            temp = [self.question] + self.answers
            temp = translateT(temp)
            self.question = temp[0]["text"]
            temp = temp[1:]
            self.answers = [x["text"] for x in temp]
            self.translated = True
