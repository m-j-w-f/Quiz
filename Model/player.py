from Model.questions import Question
import re


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def answerQ(self, q: Question) -> bool:
        """

        :param q:
        :return:
        """
        print(self.name, "to answer")
        print(q)

        while True:
            ans = input("Your Answer (A/B/C/D):")
            if re.search("[A-D]", ans) and len(ans) == 1:
                break

        idx_ans = ord(ans) - 65

        if idx_ans == q.correct_index:
            print("Correct!")
            self.score += 1
            return True
        print("Incorrect!")
        return False

    def __str__(self):
        return self.name + ":" + str(self.score)
