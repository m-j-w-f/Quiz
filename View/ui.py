from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from Model.player import Game, Player

Gme = Game(0)


class WelcomeWindow(Screen):
    numberP = ObjectProperty(None)
    numberR = ObjectProperty(None)

    def startGame(self):
        Gme.setMaxRounds(int(self.numberR.text))
        # Next Window
        sm.current = "playerW"


class PlayerWindow(Screen):
    inpP = ObjectProperty(None)

    def createPlayer(self):
        if len(self.inpP.text) > 0:
            p = Player(name=self.inpP.text, gme=Gme)
            print("Player:", p, "created")
            self.inpP.text = ""
        else:
            print("Name must have length > 0!")

    def startGame(self):
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
        Gme.setCategory(self.category.text)
        self.setDifficulty()
        # Create Window for new Question and activate it
        sm.add_widget(QuestionWindow())
        sm.current = "questionW"

    def setDifficulty(self):
        Gme.difficulty = self.difficulty.text


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
        :return:
        """
        sm.remove_widget(self)
        # TODO change Current Player Here
        # TODO check if new round starts
        sm.add_widget(QuestionWindow())
        sm.current = "questionW"


    def answeredA(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="A"):
            # TODO Add effect for correct/wrong Answer
            self.getNewQuestionWindow()
        else:
            # TODO add handling for wrong answers
            pass

    def answeredB(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="B"):
            self.getNewQuestionWindow()

    def answeredC(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="C"):
            self.getNewQuestionWindow()

    def answeredD(self):
        p = Gme.getCurrentPlayer()
        if p.answerQ(q=Gme.getCurrentQuestion(), a="D"):
            self.getNewQuestionWindow()

    pass


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


if __name__ == "__main__":
    MainApp().run()
