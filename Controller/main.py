from Model.player import Player
from Model.questions import Question
from random import shuffle


def main():
    # create Game
    n = None
    rounds = None

    passed = False
    while not passed:
        try:
            n = int(input("Enter Number of Players:"))
            rounds = int(input("Enter Number of Rounds:"))
            passed = True
        except ValueError:
            print("Make sure to enter numbers only")

    # Create Players
    players = list()
    for _ in range(n):
        pl = Player(input("Enter Name of player:"))
        players.append(pl)

    tok = Question.getSessionToken()

    for _ in range(rounds):
        # TODO Select Category for Round
        for i, p in enumerate(players):
            # TODO sometimes Bug here
            q = Question("easy", 9, tok)
            q.translateQ()
            temp = i
            # If player does not answer correctly, next player has to answer the question
            while not players[temp].answerQ(q):
                temp += 1
                if temp >= n:
                    temp = 0
        shuffle(players)

    # Print Results
    players.sort(key=lambda p: p.score, reverse=True)
    print("Scoreboard:")
    for x in players:
        print(x)


if __name__ == "__main__":
    main()
