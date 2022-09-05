from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from Model.player import Game, Player

# Initialize Game
Gme = Game(0)


class WelcomeWindow(Screen):
    numberP = ObjectProperty(None)
    numberR = ObjectProperty(None)

    def startGame(self):
        """
        Start Game one Button press
        """
        Gme.setMaxRounds(int(self.numberR.text))
        # Next Window: Player Creation Window
        sm.current = "playerW"


class PlayerWindow(Screen):
    inpP = ObjectProperty(None)

    def createPlayer(self):
        """
        Function that creates a Player on Buttonpress
        """
        if len(self.inpP.text) > 0:
            p = Player(name=self.inpP.text, gme=Gme)
            print("Player:", p, "created")
            self.inpP.text = ""
        else:
            print("Name must have length > 0!")

    def startGame(self):
        """
        Starts Game
        """
        if len(self.inpP.text) > 0:
            p = Player(name=self.inpP.text, gme=Gme)
            print("Player:", p, "created")
            self.inpP.text = ""
        sm.add_widget(CategoryWindow())


class CategoryWindow(Screen):
    currentPlayer = StringProperty()
    categories = ObjectProperty(Gme.categories.keys())
    category = ObjectProperty(None)
    difficulty = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CategoryWindow, self).__init__(**kwargs)
        self.currentPlayer = Gme.getCurrentPlayer().name + " to select category"

    def setCategory(self):
        """
        Set Category and Difficulty
        """
        Gme.setCategory(self.category.text)
        Gme.setDifficulty(self.difficulty.text)
        # Create Window for new Question and activate it
        sm.add_widget(QuestionWindow())
        sm.current = "questionW"


class QuestionWindow(Screen):
    # TODO add round based answering
    questionText = StringProperty()
    answerA = StringProperty()
    answerB = StringProperty()
    answerC = StringProperty()
    answerD = StringProperty()

    def __init__(self, **kwargs):
        super(QuestionWindow, self).__init__(**kwargs)
        # Set Text for Question
        self.questionText = Gme.getCurrentPlayer().name + " to answer:\n" + \
                            Gme.getNewQuestion(cat=Gme.category, diff=Gme.difficulty).question
        # Set answers
        self.answerA = Gme.question.answers[0]
        self.answerB = Gme.question.answers[1]
        self.answerC = Gme.question.answers[2]
        self.answerD = Gme.question.answers[3]

    def getNewQuestionWindow(self):
        """
        Crates new Question Window with a new Question
        """
        # Remove old Question
        sm.remove_widget(self)
        # Add one to in-Round Counter
        Gme.nextQinRoundCounter()
        # check if new round starts
        if Gme.checkNextRound:
            Gme.nextRound()
            sm.current = "categoryW"
        else:
            sm.add_widget(QuestionWindow())
            sm.current = "questionW"

    def answeredA(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="A"):
            # TODO Add effect for correct/wrong Answer
            # this adds a new Question Window with a new Question
            self.getNewQuestionWindow()
        else:
            # Next Player to answer and Update Text in Question Window
            Gme.nextPlayer()
            self.questionText = Gme.getCurrentPlayer().name + " to answer:\n" + Gme.getCurrentQuestion().question

    def answeredB(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="B"):
            self.getNewQuestionWindow()
        else:
            # Next Player to answer and Update Text in Question Window
            Gme.nextPlayer()
            self.questionText = Gme.getCurrentPlayer().name + " to answer:\n" + Gme.getCurrentQuestion().question

    def answeredC(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="C"):
            self.getNewQuestionWindow()
        else:
            # Next Player to answer and Update Text in Question Window
            Gme.nextPlayer()
            self.questionText = Gme.getCurrentPlayer().name + " to answer:\n" + Gme.getCurrentQuestion().question

    def answeredD(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="D"):
            self.getNewQuestionWindow()
        else:
            # Next Player to answer and Update Text in Question Window
            Gme.nextPlayer()
            self.questionText = Gme.getCurrentPlayer().name + " to answer:\n" + Gme.getCurrentQuestion().question


class GameOverWindow(Screen):
    # TODO add scoreboard
    pass


# Read .kv file
kv = Builder.load_file("welcome.kv")
# Create Screen Manager to change Screen in .py file
sm = ScreenManager()
screens = [WelcomeWindow(), PlayerWindow()]
for screen in screens:
    sm.add_widget(screen)
# Set Starting Screen
sm.current = "welcomeW"


class MainApp(App):
    def build(self):
        return sm
