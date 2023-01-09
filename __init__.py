
from PyQt5.QtWidgets import QApplication, QMainWindow
from authentification import Login
from main import mainView


class MainStart(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.authentification =  Login(self)
        self.main = mainView(self)
        self.user_id = 0
        
    def startProject(self):
        self.authentification.show()

    def startMainView(self):
        self.main.show()
        self.main.initialise()


if __name__ == '__main__':
    app = QApplication([])
    ms = MainStart()
    ms.startProject()
    app.exec_()
