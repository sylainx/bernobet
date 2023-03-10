
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

from controllers.Controller import Controller


TABLE_NAME = "matchs"
PATH_NAME = "./db/database.db"
COLUMNS_NAME = {
    "id": "VARCHAR(255) PRIMARY KEY",
    "match_type": "varchar(255)",
    "pays": "varchar(255)",
    "date": "datetime",
    "eq_rec": "VARCHAR(255)",
    "eq_vis": "varchar(255)",
    "cote": "DOUBLE NOT NULL",
    "score_final": "varchar(255)",
    "etat": "varchar(255)",
}


class MatchsController ():

    def __init__(self) -> None:
        self.TABLE_NAME=TABLE_NAME
        self.controller = Controller(PATH_NAME)


    
    def get_available_matchs(self):
        """
        Lister tous matchs les disponibles
        """

        whre_values = f" etat == 'N' OR etat='E' "
        matchs_datas = self.controller.select(self.TABLE_NAME, whre_values)
        if matchs_datas:
            list_of_matchs = list()
            for m in matchs_datas:
                dict_match = {
                    'match_id': m[0],
                    'match_type': m[1],
                    'pays': m[2],
                    'date': m[3],
                    'eq_rec': m[4],
                    'eq_vis': m[5],
                    'cote': m[6],
                    'scr_1': (m[7]).split(":")[0], # extrait separé par :
                    'scr_2': (m[7]).split(":")[1], # extrait separé par :
                    'etat': m[8],
                }
                list_of_matchs.append(dict_match)

            return list_of_matchs
            
        return None
    

    
    def get_all_matchs(self):
        """
            Pour afficher toutes les matchs indistinctements
        """
        matchs_datas = self.controller.select(self.TABLE_NAME)
        if matchs_datas:
            list_of_matchs = list()
            for m in matchs_datas:
                dict_match = {
                    'match_id': m[0],
                    'match_type': m[1],
                    'pays': m[2],
                    'date': m[3],
                    'eq_rec': m[4],
                    'eq_vis': m[5],
                    'cote': m[6],
                    'scr_1': (m[7]).split(":")[0], # extrait separé par :
                    'scr_2': (m[7]).split(":")[1], # extrait separé par :
                    'etat': m[8],
                }
                list_of_matchs.append(dict_match)

            return list_of_matchs

        return None
    

    def get_match_by_id(self, match_id):
        """
            Pour afficher un matchs par son id
        """

        if not match_id :
            return None

        whre_id = f"id ='{match_id}'"
        
        matchs_datas = self.controller.select(self.TABLE_NAME,whre_id)
        if matchs_datas:
            dict_match = {
                'match_id': matchs_datas[0][0],
                'match_type': matchs_datas[0][1],
                'pays': matchs_datas[0][2],
                'date': matchs_datas[0][3],
                'eq_rec': matchs_datas[0][4],
                'eq_vis': matchs_datas[0][5],
                'cote': matchs_datas[0][6],
                'scr_1': (matchs_datas[0][7]).split(":")[0], # extrait separé par :
                'scr_2': (matchs_datas[0][7]).split(":")[1], # extrait separé par :
                'etat': matchs_datas[0][8],
            }
            
            return dict_match

        return None
