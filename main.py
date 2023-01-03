
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from authentification import Login
import functools

from controllers.Controller import Controller


class mainView(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.initialise_constants()
        self.login = Login(self)
        
        self.user_id= None
        self.controller =  Controller(self.PATH_NAME)

    def initialisation(self):
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(1000, 600)
        self.setWindowIcon(QIcon(self.WINDOW_ICON))
        # self.show()
        self.user_infos= dict()
        self.display()
        self.header_content()
        self.sidebar_content()
        self.bet_info_content()

        self.content = QWidget()
        # self.content.setStyleSheet(
        #     "background-color: #FAFAFA;"
        # )

        self.content.setLayout(self.container)
        self.setCentralWidget(self.content)

    def display(self) -> None:

        self.header = QWidget(self)
        self.header.setStyleSheet(
            "background-color: #424949"
        )

        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet(
            "background-color: #616A6B"
        )

        self.body = QWidget(self)
        self.body.setStyleSheet(
            "background-color: #6e7575"
        )

        self.bet_info = QWidget(self)

        self.bet_info.setStyleSheet(
            "background-color: #616A6B"
        )

        self.container = QGridLayout(self)

        self.container.addWidget(self.header, 0, 0, 1, 3)
        self.container.addWidget(self.sidebar, 1, 0)
        self.container.addWidget(self.body, 1, 1)
        self.container.addWidget(self.bet_info, 1, 2)

        self.setContentsMargins(0, 0, 0, 0)
        self.container.setRowStretch(0, 1)
        self.container.setRowStretch(1, 8)

        self.container.setColumnStretch(0, 2)
        self.container.setColumnStretch(1, 5)
        self.container.setColumnStretch(2, 2)

        self.container.setSpacing(0)


    def header_content(self):

        #Menu de l'entete
        self.main_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()

        self.menu = QGroupBox()
        self.menu.setFixedWidth(450)

        #Logo de l'application
        self.logo = QLabel("Bernobet")
        self.logo.setStyleSheet(
            "color: #f4661b;"
        )

        #Bouton pour les matchs
        self.match_btn = QPushButton("Matchs")

        #Bouton pour les paris
        self.bet_btn = QPushButton("Paris")

        #Bouton pour les paiements
        self.payment_btn = QPushButton("Paiements")

        #Bouton pour les comptes
        self.account_btn = QPushButton("Comptes")

        #Ajout des widgets
        self.content_layout.addWidget(self.logo)
        self.content_layout.addWidget(self.match_btn)
        self.content_layout.addWidget(self.bet_btn)
        self.content_layout.addWidget(self.payment_btn)
        self.content_layout.addWidget(self.account_btn)


        #Ajout des widgets du content_layout dans le menu
        self.menu.setLayout(self.content_layout)

        #Ajout du menu dans le main_layout
        self.main_layout.addWidget(self.menu, alignment=Qt.AlignLeft)

        #Authentification
        self.auth = QGroupBox()
        self.content_layout = QVBoxLayout()

        self.user = QLabel(f"Joberno ")
        print(f"USer: {self.user_infos['username']}")
        self.sold = QLabel(f" Solde : {0.0} Gourdes")

        #Ajout des widgets
        self.content_layout.addWidget(self.user)
        self.content_layout.addWidget(self.sold)


        #Ajout des widgets du content_layout dans le menu
        self.auth.setLayout(self.content_layout)

        #Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.auth, alignment=Qt.AlignRight)

        #Ajout du main_layout dans le header
        self.header.setLayout(self.main_layout)


    def sidebar_content(self):

        #Menu principal
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Menu principal")
        self.dashboard_btn = QPushButton("Dashboard")
        self.account_btn = QPushButton("Compte")
        self.match_btn = QPushButton("Matchs")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.addWidget(self.dashboard_btn)
        self.content_layout.addWidget(self.account_btn)
        self.content_layout.addWidget(self.match_btn)

        self.grp.setLayout(self.content_layout)
        #Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop)



        #Informations
        self.content_btm_layout = QVBoxLayout()
        self.grp = QGroupBox()


        self.info_lbl = QLabel("Informations")
        self.setting_btn = QPushButton("Parametres")
        self.help_btn = QPushButton("Aide")
        self.about_btn = QPushButton("A propos")

        # Ajout des Widgets
        self.content_btm_layout.addWidget(self.info_lbl)
        self.content_btm_layout.addWidget(self.setting_btn)
        self.content_btm_layout.addWidget(self.help_btn)
        self.content_btm_layout.addWidget(self.about_btn)

        #Ajout des composants dans le main_layout
        self.grp.setLayout(self.content_btm_layout)

        self.main_layout.addWidget(self.grp, alignment=Qt.AlignBottom)
        self.main_layout.setAlignment(Qt.AlignJustify)

        #Ajout du main_layout dans le sidebar
        self.sidebar.setLayout(self.main_layout)

        #Evenements sur les boutons
        self.dashboard_btn.clicked.connect(self.dashboard_content)
        self.account_btn.clicked.connect(functools.partial(self.change_body_content, self.account_content()))
        self.match_btn.clicked.connect(self.match_content)
        self.setting_btn.clicked.connect(self.setting_content)
        self.help_btn.clicked.connect(self.help_content)
        self.about_btn.clicked.connect(self.about_content)


    def bet_info_content(self):

        # Menu principal
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Informations du pariage")
        self.bet_amount_lbl = QLabel("Montant du pariage : ")
        self.bet_amount_field = QLineEdit()
        self.bet_amount_field.setPlaceholderText("Saisir le montant du pariage")
        self.account_btn = QPushButton("Parier")
        self.account_btn.setStyleSheet(
            "background-color: #f4661b;"
        )

        self.bet_h_layout = QHBoxLayout()
        self.bet_win_h_layout = QHBoxLayout()

        self.total_lbl = QLabel("Total : ")
        self.total_value_lbl = QLabel(f"{20.00} Gourdes")


        self.bet_win_lbl = QLabel("Possibilite de gain de : ")
        self.bet_win_value_lbl = QLabel(f"{300.00} Gourdes")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.addWidget(self.bet_amount_lbl)
        self.content_layout.addWidget(self.bet_amount_field)
        self.content_layout.addWidget(self.account_btn)

        self.bet_h_layout.addWidget(self.total_lbl)
        self.bet_h_layout.addWidget(self.total_value_lbl)

        self.bet_win_h_layout.addWidget(self.bet_win_lbl)
        self.bet_win_h_layout.addWidget(self.bet_win_value_lbl)

        self.content_layout.addLayout(self.bet_h_layout)
        self.content_layout.addLayout(self.bet_win_h_layout)


        self.grp.setLayout(self.content_layout)
        self.grp.setContentsMargins(5,5,5,5)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop)

        self.main_layout.setAlignment(Qt.AlignJustify)

        # Ajout du main_layout dans le sidebar
        self.bet_info.setLayout(self.main_layout)

        # Evenements sur les boutons
        self.dashboard_btn.clicked.connect(self.dashboard_content)


    def dashboard_content(self):

        #Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your dashboard")


        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        #Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)

    def change_body_content(self, new_layout):
        # Récupération du layout actuel du QWidget "body"
        old_layout = self.body.layout()

        # Suppression de tous les widgets du layout actuel du QWidget "body"
        for i in reversed(range(old_layout.count())):
            widget = old_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        print(self.account_content())
        # Mise à jour du layout du QWidget "body"
        self.body.setLayout(new_layout)

    def account_content(self):

        #Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.account_content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your account")


        # Ajout des Widgets
        self.account_content_layout.addWidget(self.subtitle_lbl)
        self.account_content_layout.setAlignment(Qt.AlignCenter)

        #Ajout des composants dans le main_layout
        # self.body.setLayout(self.account_content_layout)

        return self.account_content_layout




    def match_content(self):

        #Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your matchs")


        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        #Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)



    def setting_content(self):

        #Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your setting info")


        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        #Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)


    def help_content(self):

        #Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("How can we help you ?")


        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        #Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)


    def about_content(self):

        #Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("We are devs !")


        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        #Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)


    def initialise_constants(self):
        self.TABLE_NAME = "users"
        self.PATH_NAME="./db/database.db"
        self.WINDOW_TITLE="bernobet"
        self.WINDOW_ICON="assets/logo.pnp"

    def get_user_datas(self):
        if self.login.user_id > 0:
            where_data= f"id = {self.login.user_id}"
            result = self.controller.select(self.TABLE_NAME,where_data)
            
            data = {
                'last_name': result[0][1],
                'first_name': result[0][2],
                'gender': result[0][3],
                'birth_date': result[0][4],
                'gender': result[0][5],
                'phone': result[0][6],
                'nif': result[0][7],
                'username': result[0][8],
                'balance': result[0][9],
                'status': result[0][10],
            }
            
            self.user_infos= data
            self.initialisation()
            



if __name__ == '__main__':
    app = QApplication([])
    main = mainView()
    app.exec_()


