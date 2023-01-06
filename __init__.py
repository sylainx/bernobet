
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QScrollArea, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import threading, time
from SessionManager import SessionManager
from Views.matchs.MatchsView import MatchView
from authentification import Login
import functools

from controllers.Controller import Controller
from authentification import Login, Register
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
