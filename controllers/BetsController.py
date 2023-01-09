
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import threading
import time
from SessionManager import SessionManager
from Views.matchs.MatchsView import MatchView
from Views.users.AccountView import AccountView
from Views.users.UsersView import UserView
from authentification import Login
import functools

from controllers.Controller import Controller
from controllers.MatchsController import MatchsController
from controllers.UsersController import UsersController


TABLE_NAME = "bets"
PATH_NAME = "./db/database.db"
COLUMNS_NAME = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "user_id": "varchar(255) NOT NULL",
    "match_id": "varchar(255) NOT NULL",
    "date": "DATETIME NOT NULL",
    "montant_depense": "DOUBLE NOT NULL",
    "cote": "DOUBLE NOT NULL",
    "score_prevu": "varchar(255) NOT NULL",
    "etat" : "VARCHAR(25)"
}


class BetsController ():

    def __init__(self) -> None:
        self.TABLE_NAME=TABLE_NAME
        self.controller = Controller(PATH_NAME)
        self.COLUMNS_NAME=COLUMNS_NAME
        self.user_controller = UsersController()
        self.match_controller = MatchsController()
        self.createTable()
    

    def create_bet(self,columns:dict):
        """
            - Enregistrer un pari
        """
        if columns:
            print(f"BEts colums: {columns}")
            bets_datas = self.controller.insert(self.TABLE_NAME, columns.items())
        else:
            print(f"BEts controller- no data to insert: {columns}")
        return columns
            
    
    def get_bets(self, FOR_USER_ID=None):
        """
        Lister tous les paris disponibles
        """
        if FOR_USER_ID:
            user_id = SessionManager.getItem('userStorage')
            where_data = f" user_id = {user_id}"
        else:
            where_data= None

        bets_datas = self.controller.select(self.TABLE_NAME, where_data)
        if bets_datas:
            list_of_bets = list()
            for bet in bets_datas:
                # get user data
                user = self.user_controller.get_user_datas()
                match = self.match_controller.get_match_by_id(bet[2])
                if user and match:
                    
                    dict_match = {                    
                        "id": bet[0],
                        "user": f"{user['first_name']} {user['last_name']}",
                        "match": f"{match['eq_rec']} - {match['eq_vis']}",
                        "date": bet[3],
                        "montant_depense": bet[4],
                        "cote": bet[5],
                        "score_prevu": bet[6],
                    }
                    list_of_bets.append(dict_match)

                return list_of_bets
            
        return None
    
    def get_bet_by_id(self, id=None):
        print("Click on bet")


    def createTable(self):
        """
        pour creer la table en question
        si elle est deja presente, elle ne fait rien
        """
        result = self.controller.create_table(
            table_name=self.TABLE_NAME, columns=self.COLUMNS_NAME.items())

        if not result:
            print(f"Table : ```{self.TABLE_NAME}``` already exist")
        else:
            print(f"Table : ```{self.TABLE_NAME}``` vient d'etre créée")

    def dropTable(self):
        """
        use it only for drop table and delete all fields
        """
        self.controller.drop(self.TABLE_NAME)
        print(f"Table ```{self.TABLE_NAME.upper()}``` is dropped")
