from Model.questions import Question
from random import shuffle


class Game:
    players = list()
    currentRound = 0
    i = 0
    savedI = 0
    flag = True
    j = 0

    def __init__(self, nRnds: int):
        self.numberOfRounds = nRnds
        self.token = Question.getSessionToken()
        self.categories = Question.getCategories()
        self.category = None
        self.difficulty = None
        self.question = None

    def setMaxRounds(self, nRnds: int):
        self.numberOfRounds = nRnds

    def nextRound(self):
        print("Players Shuffled")
        self.currentRound += 1
        self.i = 0
        shuffle(self.players)

    def storeI(self):
        if self.flag:
            # nothing is yet stored
            self.flag = False
            self.savedI = self.i
            print(f"stored {self.savedI}")

    def restoreI(self):
        if not self.flag:
            # something was stored
            self.flag = True
            self.i = self.savedI
            print(f"restored {self.i}")

    def nextQinRoundCounter(self):
        self.j += 1
        print(self.j)

    def checkNextRound(self):
        if self.j >= len(self.players):
            self.j = 0
            print("New Round Started!")
            return True
        return False

    def getCurrentPlayer(self):
        """
        :return: returns current Player (normal Game loop: Everybody answers correctly)
        """
        return self.players[self.i]

    def nextPlayer(self):
        """
        called by Player if Question is answered correctly
        """
        self.i += 1
        if self.i >= len(self.players):
            self.i = 0

    def getScoreboard(self) -> list:
        """
        :return: Sorted list of Players
        """
        return sorted(self.players, key=lambda p: p.score, reverse=True)

    def setCategory(self, cat: str):
        self.category = self.categories.get(cat)
        print(self.category)

    def setDifficulty(self, diff: str):
        self.difficulty = diff
        print(self.difficulty)

    def getNewQuestion(self, cat: int, diff: str):
        self.question = Question(diff=diff, cat=cat, token=self.token)
        # self.question.translateQ()
        return self.question

    def getCurrentQuestion(self):
        return self.question


class Player:
    def __init__(self, name: str, gme: Game):
        self.name = name
        self.score = 0
        self.game = gme
        gme.players.append(self)

    def answerQ(self, q: Question, a: str) -> bool:
        """
        Player answers Question, adds Points if correct
        :param q: Question to be answered
        :param a: Answer provided by Player
        :return: Boolean if correct
        """
        print(self.name, "to answer")
        print(q)

        answer_to_idx = {"A": 0, "B": 1, "C": 2, "D": 3}
        a = answer_to_idx.get(a)
        #print(a)
        #print(q.correct_index)
        if a == q.correct_index:
            print("Correct!")
            self.score += 1
            # restores the correct order of players
            self.game.restoreI()
            self.game.nextPlayer()
            return True
        print("Incorrect!")
        return False

    def __str__(self):
        return self.name + " : " + str(self.score)
