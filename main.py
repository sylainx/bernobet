
from datetime import date
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QLineEdit,\
    QScrollArea, QButtonGroup, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from Helpers import Helpers
from Views.BetsView import BetsView
from Views.PaymentsView import PaymentsView
from Views.matchs.MatchsView import MatchView
from Views.users.AccountView import AccountView
from Views.users.UsersView import UserView
from controllers.BetsController import BetsController

from controllers.MatchsController import MatchsController
from controllers.UsersController import UsersController


class mainView(QMainWindow):

    def __init__(self, parent) -> None:
        super().__init__()
        self.initialise_constants()
        self.match_controller = MatchsController()
        self.user_controller = UsersController()
        self.bet_controller = BetsController()
        self.func_helpers = Helpers()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(1000, 600)
        self.setWindowIcon(QIcon(self.WINDOW_ICON))
        self.content = QWidget()
        # self.content.setStyleSheet(
        #     "background-color: #FAFAFA;"
        # )

        self.setCentralWidget(self.content)

    def initialise(self):
        self.user_infos = self.user_controller.get_user_datas()
        self.display()
        self.header_content()
        self.sidebar_content()
        self.bet_info_content()
        self.content.setLayout(self.container)
        self.available_match_content()

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
        # add

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
        # Menu de l'entete
        self.main_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()

        self.menu = QGroupBox()
        self.menu.setFixedWidth(450)

        # Logo de l'application
        self.logo = QLabel("JetBrainsBet")
        self.logo.setStyleSheet(
            "color: rgb(244,102,27);"
            "font-weight: bold;"
        )

        # Bouton pour les matchs
        self.match_btn = QPushButton("Matchs")
        self.match_btn.clicked.connect(lambda: self.available_match_content())

        # Bouton pour les paris
        self.bet_btn = QPushButton("Paris")
        self.bet_btn.clicked.connect(lambda:self.displayParisCallback())

        # Bouton pour les paiements
        self.payment_btn = QPushButton("Paiements")
        self.payment_btn.clicked.connect(
            lambda: self.displayAdminPaymentsCallback())

        # Bouton pour les comptes
        self.account_btn = QPushButton("Comptes")
        self.account_btn.clicked.connect(
            lambda: self.displayUserAccountCallback())

        # Ajout des widgets
        self.content_layout.addWidget(self.logo)
        self.content_layout.addWidget(self.match_btn)
        self.content_layout.addWidget(self.bet_btn)
        self.content_layout.addWidget(self.payment_btn)
        self.content_layout.addWidget(self.account_btn)

        # Ajout des widgets du content_layout dans le menu
        self.menu.setLayout(self.content_layout)

        # Ajout du menu dans le main_layout
        self.main_layout.addWidget(self.menu, alignment=Qt.AlignLeft)

        # Authentification
        self.auth = QGroupBox()
        self.content_layout = QVBoxLayout()

        self.user = QLabel(f"{self.user_infos['username']} ")
        self.sold = QLabel(f" Solde : {self.user_infos['balance']} Gdes")
        self.logout_btn = QPushButton("Logout", self)
        self.logout_btn.setStyleSheet(
            "background: rgb(244,102,27); border-radius:5px; padding:5px")
        self.logout_btn.clicked.connect(lambda: self.logoutCallback())
        # Ajout des widgets
        self.content_layout.addWidget(self.user)
        self.content_layout.addWidget(self.sold)
        self.content_layout.addWidget(self.logout_btn)

        # Ajout des widgets du content_layout dans le menu
        self.auth.setLayout(self.content_layout)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.auth, alignment=Qt.AlignRight)

        # Ajout du main_layout dans le header
        self.header.setLayout(self.main_layout)

    def sidebar_content(self):

        # Espace administration
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Espace administration")

        self.dashboard_btn = QPushButton("Dashboard")
        self.match_btn = QPushButton("Matchs")
        self.account_btn = QPushButton("Compte")
        self.adm_payments_btn = QPushButton("Paiements")

        # Ajout des Widgets
        if self.user_infos['is_admin']:
            self.content_layout.addWidget(self.subtitle_lbl)
            self.content_layout.addWidget(self.dashboard_btn)
            self.content_layout.addWidget(self.match_btn)
            self.content_layout.addWidget(self.account_btn)
            self.content_layout.addWidget(self.adm_payments_btn)

        self.grp.setLayout(self.content_layout)
        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop)

        # Informations
        self.content_btm_layout = QVBoxLayout()
        self.grp = QGroupBox()


        # Ajout des composants dans le main_layout
        self.grp.setLayout(self.content_btm_layout)

        self.main_layout.addWidget(self.grp, alignment=Qt.AlignBottom)
        self.main_layout.setAlignment(Qt.AlignJustify)

        # Ajout du main_layout dans le sidebar
        self.sidebar.setLayout(self.main_layout)

        # Evenements sur les boutons
        self.account_btn.clicked.connect(
            lambda: self.displayAdminListUsersCallback())
        self.adm_payments_btn.clicked.connect(
            lambda: self.displayAdminPaymentsCallback())
        self.dashboard_btn.clicked.connect(lambda: self.dashboard_content())
        self.match_btn.clicked.connect(lambda: self.admin_match_content())
        

    def bet_info_content(self):
        # pariages
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        grid_Lyt = QGridLayout()

        self.grp = QGroupBox()

        # teams
        self.subtitle_lbl = QLabel("Informations du pariage")
        self.subtitle_lbl.setStyleSheet("font:16px;  color: white")
        self.bet_amount_lbl = QLabel("Montant du pariage : ")
        # match_id
        self.BET_match_id = QLabel()
        self.BET_match_id.setVisible(False)
        # home team
        self.eq_1 = QLabel()
        self.eq_1.setVisible(False)
        # move team
        self.eq_2 = QLabel()
        self.eq_2.setVisible(False)
        # cote
        self.match_cote = QLabel()
        self.match_cote.setVisible(False)
        # score 1
        self.usr_scr1 = QLineEdit()
        self.usr_scr1.setValidator(QIntValidator(0, 10, self))
        self.usr_scr1.setPlaceholderText(
            "Score 1")
        self.usr_scr1.setVisible(False)
        # score 2
        self.usr_scr2 = QLineEdit()
        self.usr_scr2.setVisible(False)
        self.usr_scr2.setValidator(QIntValidator(0, 10, self))
        self.usr_scr2.setPlaceholderText(
            "Score 1")
        self.bet_amount_field = QLineEdit()
        self.bet_amount_field.setText(str(25))
        self.bet_amount_field.setStyleSheet(
            "border-radius: 5px; height:20px; border: 1px solid #FBFBFB")
        self.bet_amount_field.setValidator(
            QDoubleValidator(0.0, 75000.0, 2, self))
        self.bet_amount_field.setPlaceholderText(
            "Saisir le montant du pariage")

        self.bet_errorMsg= QLabel()
        self.bet_errorMsg.setVisible(False)
        self.bet_errorMsg.setStyleSheet("color: white; background: rgb(244,102,27);")
        
        self.place_bet_btn = QPushButton("Parier")
        self.place_bet_btn.setStyleSheet(
            "background-color: #f4661b;"
            "border-radius: 5px;"
            "padding: 5px 2px;"
        )

        self.bet_h_layout = QHBoxLayout()
        self.bet_win_h_layout = QHBoxLayout()

        self.total_lbl = QLabel("Total : ")
        self.total_value_lbl = QLabel(f"{20.00} Gdes")

        self.bet_win_lbl = QLabel("Possibilite de gain de : ")        
        self.bet_win_value_lbl = QLabel(f"{300.00} Gdes")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl, Qt.AlignCenter)
        # grid layout
        grid_Lyt.addWidget(self.eq_1, 0, 0)
        grid_Lyt.addWidget(self.eq_2, 0, 1)
        grid_Lyt.addWidget(self.usr_scr1, 1, 0)
        grid_Lyt.addWidget(self.usr_scr2, 1, 1)
        self.content_layout.addLayout(grid_Lyt)
        # grid layout
        self.content_layout.addWidget(self.match_cote)
        self.content_layout.addWidget(self.bet_amount_lbl)
        self.content_layout.addWidget(self.bet_amount_field)
        self.content_layout.addWidget(self.bet_errorMsg)
        self.content_layout.addWidget(self.place_bet_btn)

        self.bet_h_layout.addWidget(self.total_lbl)
        self.bet_h_layout.addWidget(self.total_value_lbl)

        self.bet_win_h_layout.addWidget(self.bet_win_lbl)
        self.bet_win_h_layout.addWidget(self.bet_win_value_lbl)

        self.content_layout.addLayout(self.bet_h_layout)
        self.content_layout.addLayout(self.bet_win_h_layout)

        self.grp.setLayout(self.content_layout)
        self.grp.setContentsMargins(5, 5, 5, 5)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop)

        self.main_layout.setAlignment(Qt.AlignJustify)

        # Ajout du main_layout dans le sidebar
        self.bet_info.setLayout(self.main_layout)

        # =========== A C T I O N ===============
        self.place_bet_btn.clicked.connect(
            lambda x: self.displayUserPlaceBetCallback(x))
        # self.bet_amount_field.textChanged.connect(lambda:self.validaAmountCallback())

    # def validaAmountCallback(self):
    #     if self.func_helpers.is_float_in_range(self.bet_amount_field.text(),0):
    #         print("Valid amount")
    #         mt = float(self.bet_amount_field.text())
    #         ct_mtch = float(self.BET_match_id.text())
    #         amount = mt * ct_mtch
    #         self.bet_win_value_lbl.setText(f"{amount} Gdes")
    #         return True

    #     return False

    def dashboard_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Dashboard")

        # widget()
        self.box_dashboards = QWidget()
        scrollLaout_DashboardMatch = QScrollArea()
        scrollLaout_DashboardMatch.setWidgetResizable(True)
        vLyt_list_Dashboard = QVBoxLayout()
        scrollLaout_DashboardMatch.setWidget(self.box_dashboards)

        # ******************** start box
        box_dashboard = QWidget(self.box_dashboards)
        # ******************** end box

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)

        return self.main_layout

    def change_body_content(self, new_layout):
        # Récupération du layout actuel du QWidget "body"
        old_layout = self.body.layout()

        # Suppression de tous les widgets du layout actuel du QWidget "body"
        for i in reversed(range(old_layout.count())):
            widget = old_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Mise à jour du layout du QWidget "body"
        self.body.setLayout(new_layout)

    def account_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.account_content_layout = QVBoxLayout()
        # self.hLyt_account = QHBoxLayout()
        # self.account_content_layout.alignment(Qt.AlignTop)
        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your account")

        # widget()
        scrollLaout_Account = QScrollArea()
        scrollLaout_Account.setWidgetResizable(True)
        # self.box_accounts = QWidget()
        # vLyt_list_Dashboard = QVBoxLayout()
        scrollLaout_Account.setLayout(self.account_content_layout)

        # ******************** start box
        # title account
        self.title_account_QLB = QLabel("Compte")
        self.title_account_QLB.setStyleSheet("color: white;")
        # match_id
        self.user_id_lbl = QLabel("Code: ")
        self.user_id_Field = QLineEdit()
        self.user_id_Field.setEnabled(False)
        self.user_id_Field.setStyleSheet("color: white;")
        # last name
        self.last_name_lbl = QLabel("Last name: ")
        self.last_name_Field = QLineEdit()
        self.last_name_Field.setStyleSheet("color: white;")
        self.last_name_Field.setPlaceholderText("Saisir le pays")
        # first name
        self.first_name_lbl = QLabel("Fist name: ")
        self.first_name_Field = QLineEdit()
        self.first_name_Field.setStyleSheet("color: white;")
        self.first_name_Field.setPlaceholderText("Saisir le pays")
        # gender
        self.gender_lbl = QLabel("Gender: ")
        self.gender_Field = QLineEdit()
        self.gender_Field.setStyleSheet("color: white;")
        self.gender_Field.setPlaceholderText("Saisir le pays")
        # birth date
        self.birth_date_lbl = QLabel("Date de naissance: ")
        self.birth_date_Field = QLineEdit()
        self.birth_date_Field.setStyleSheet("color: white;")
        self.birth_date_Field.setPlaceholderText("Saisir le pays")
        # phone
        self.phone_lbl = QLabel("Tel: ")
        self.phone_Field = QLineEdit()
        self.phone_Field.setStyleSheet("color: white;")
        self.phone_Field.setPlaceholderText("Saisir tel")
        # username
        self.username_lbl = QLabel("Id: ")
        self.username_Field = QLineEdit()
        self.username_Field.setStyleSheet("color: white;")
        self.username_Field.setPlaceholderText("Saisir le pays")
        # nif
        self.nif_lbl = QLabel("Id: ")
        self.nif_Field = QLineEdit()
        self.nif_Field.setStyleSheet("color: white;")
        self.nif_Field.setPlaceholderText("Saisir le pays")
        # password
        self.password_lbl = QLabel("Mot de passe: ")
        self.password_Field = QLineEdit()
        self.password_Field.setStyleSheet("color: white;")
        self.password_Field.setPlaceholderText("Saisir le mot de passe")
        # confirm_password
        self.confirm_password_lbl = QLabel("Confirmer votre mot de passe: ")
        self.confirm_password_Field = QLineEdit()
        self.confirm_password_Field.setStyleSheet("color: white;")
        self.confirm_password_Field.setPlaceholderText(
            "Confirmer votre mot de passe")

        self.updateInfoBtn = QPushButton()
        self.updateInfoBtn.setStyleSheet(
            "background:rgb(244,102,47); color: white; padding: 5px;")
        # ******************** end box

        # Ajout des Widgets
        self.account_content_layout.addWidget(self.subtitle_lbl, Qt.AlignTop)
        self.account_content_layout.addWidget(self.user_id_lbl)
        self.account_content_layout.addWidget(self.user_id_Field)
        self.account_content_layout.addWidget(self.username_lbl)
        self.account_content_layout.addWidget(self.username_Field)
        self.account_content_layout.addWidget(self.first_name_lbl)
        self.account_content_layout.addWidget(self.first_name_Field)
        self.account_content_layout.addWidget(self.last_name_lbl)
        self.account_content_layout.addWidget(self.last_name_Field)
        self.account_content_layout.addWidget(self.gender_lbl)
        self.account_content_layout.addWidget(self.gender_Field)
        self.account_content_layout.addWidget(self.birth_date_lbl)
        self.account_content_layout.addWidget(self.birth_date_Field)
        self.account_content_layout.addWidget(self.phone_lbl)
        self.account_content_layout.addWidget(self.phone_Field)
        self.account_content_layout.addWidget(self.nif_lbl)
        self.account_content_layout.addWidget(self.nif_Field)
        self.account_content_layout.addWidget(self.password_lbl)
        self.account_content_layout.addWidget(self.password_Field)
        self.account_content_layout.addWidget(self.confirm_password_lbl)
        self.account_content_layout.addWidget(self.confirm_password_Field)
        self.account_content_layout.addWidget(self.updateInfoBtn)
        self.account_content_layout.setAlignment(Qt.AlignCenter)
        # Ajout des composants dans le main_layout
        self.body.setLayout(self.account_content_layout)
        return self.account_content_layout

    def vertica_scroll_layout(self, parent: QWidget = None):
        """
            - Dynamic vertical scroll the parent widget
            - Argument:
                - `parent`: `QWidget`
            - Return `QVBoxLayout`
        """
        # scrollable
        scroll_vLyt = QScrollArea(verticalScrollBarPolicy=Qt.ScrollBarAlwaysOn)
        scroll_vLyt.setWidgetResizable(True)
        # widget container in ScrollArea
        container_widget = QWidget(parent)
        vLyt_container = QVBoxLayout()
        scroll_vLyt.setWidget(container_widget)
        return vLyt_container

    def admin_match_content(self):

        matchView = MatchView(self)
        matchView.refresh_datas()
        self.refresh_dashboard()
        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)
        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Liste des matchs")
        # add to layout

        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignTop)

        # Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)
    # end match_contents

    def available_match_content(self):
        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)
        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Liste des matchs")
        #
        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)

        # Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)

        # =================== LIST MATCHS ===================

        list_datas = self.match_controller.get_available_matchs()
        if list_datas:
            self.loadListMatchs(list_datas)
        else:
            print(f"No matchs found")
    # end match_contents

    def loadListMatchs(self, list_matchs):

        # self.list_of_box_matchs = QWidget()
        # self.list_of_box_matchs.setContentsMargins(5, 5, 5, 5)
        # self.vLyt_listBoxMatchs = QVBoxLayout()

        self.group_lineMatch_QGB = QButtonGroup()

        scrl_Lyt = self.vertica_scroll_layout()

        if list_matchs:
            for match in list_matchs:
                # *********** start Boite mise en Page pour un match

                boxMatch_WDG = QWidget()
                boxMatch_WDG.setObjectName(f"{match['match_id']}")
                self.send2Bet_Btn = QPushButton("Parier")
                self.send2Bet_Btn.setStyleSheet(
                    "background-color: #f4661b;"
                    "border-radius: 2px;"
                    "padding: 2px 5px;"
                )
                self.send2Bet_Btn.setContentsMargins(0, 0, 0, 0)
                self.send2Bet_Btn.setObjectName(f"{match['match_id']}")
                self.group_lineMatch_QGB.addButton(self.send2Bet_Btn)

                #
                boxMatch_WDG.setStyleSheet(
                    "background-color: rgb(94,101,102); border-radius: 5px;"
                )
                hLyt_Boxmatch = QHBoxLayout(boxMatch_WDG)
                # left box
                self.eqDom_Lbl = QLabel(f"{match['eq_rec']}")
                self.eqDom_Lbl.setStyleSheet(
                    "color: rgb(255,255,255);"
                    "font: 16px bold;"
                )

                hLyt_Boxmatch.addWidget(self.eqDom_Lbl, alignment=Qt.AlignLeft)

                # center box
                self.eqScore_Lbl = QLabel(
                    f"[ {match['scr_1']} - {match['scr_2']} ]")
                self.eqScore_Lbl.setStyleSheet(
                    "color: rgb(255,255,255); padding: 2px; font: 16px bold;")
                hLyt_Boxmatch.addWidget(self.eqScore_Lbl)
                # right box
                self.eqDep_Lbl = QLabel(f"{match['eq_vis']}")
                self.eqDep_Lbl.setStyleSheet(
                    "color: rgb(255,255,255);"
                    "font: 16px bold;"
                )

                hLyt_Boxmatch.addWidget(
                    self.eqDep_Lbl, alignment=Qt.AlignRight)
                hLyt_Boxmatch.addWidget(
                    self.send2Bet_Btn, alignment=Qt.AlignRight)

                # *********** end Boite mise en Page pour un match
                scrl_Lyt.addWidget(boxMatch_WDG)
                # self.group_lineMatch_QGB.setLayout(boxMatch_WDG)

            self.content_layout.addLayout(scrl_Lyt)

            # ======== A C T I O N S  ========
            self.group_lineMatch_QGB.buttonClicked.connect(
                lambda x: self.goToBetBoxCallback(x))

    def setting_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your setting info")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)

    def help_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("How can we help you ?")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)

    def about_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("We are devs !")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.body.setLayout(self.content_layout)

    def initialise_constants(self):
        self.TABLE_NAME = "users"
        self.PATH_NAME = "./db/database.db"
        self.WINDOW_TITLE = "JetbrainsBet"
        self.WINDOW_ICON = "assets/logo.pnp"

    # ====================  U S E R S   =========================

    def displayUserAccountCallback(self):
        print("User account is clicked")
        self.ui_account_user = AccountView(self)
        self.ui_account_user.refresh_datas()

    def displayParisCallback(self):
        print("Liste pari is clicked")
        self.ui_user_bets = BetsView(self)
        self.ui_user_bets.refresh_datas()

    def displayUserPlaceBetCallback(self, btn: QPushButton):

        # button = btn.objectName()
        self.bet_errorMsg.setVisible(False)
        id_match_selectionne = self.BET_match_id.text()
        match = self.match_controller.get_match_by_id(id_match_selectionne)
        
        if match:
            scr1_enter_by_user = self.usr_scr1.text()
            scr2_enter_by_user = self.usr_scr2.text()
            mt_place = self.bet_amount_field.text()  # montant entré par l'utilisateur
            MIN_VALUE = 0
            MIN_BET=25
            MAX_BET=75000

            if scr1_enter_by_user != "" and scr2_enter_by_user != "" and mt_place != "" \
                and self.func_helpers.is_int_in_range(scr1_enter_by_user, MIN_VALUE) \
                and self.func_helpers.is_int_in_range(scr2_enter_by_user, MIN_VALUE)\
                and self.func_helpers.is_float_in_range(mt_place, MIN_BET, MAX_BET):
                mt_place = float(mt_place)
                
                if mt_place <= float(self.user_infos['balance']):
                    INITIAL_state = "SAVE"
                    bet_datas = {
                        "user_id": self.user_infos['id'],
                        "match_id": match['match_id'],
                        "date": self.func_helpers.get_datetime(),
                        "montant_depense": mt_place,
                        "cote": match['cote'],
                        "score_prevu": f"{scr1_enter_by_user}:{scr2_enter_by_user}",
                        "etat" : INITIAL_state
                    }
                    
                    # Enregistrer le pari
                    bet = self.bet_controller.create_bet(bet_datas)
                    # Enlever le montant sur le compte de l'utilisateur
                    remove_balance= self.user_controller.pay_with_balance(self.user_infos['id'], mt_place)
                    # update info de l'utilsateur
                    self.user_infos = self.user_controller.get_user_datas()
                    print(f"New Balance: {remove_balance}")
                    QMessageBox.information(
                    None, "Confirmation", "Enregistrement pari reussi", QMessageBox.Ok)
                    self.emptyField()
                    self.initialise()
                else:
                    self.bet_errorMsg.setText("Balance insuffisante")
                    self.bet_errorMsg.setVisible(True)
            else:
                self.bet_errorMsg.setText(f"Entrer score du match et/ou montant pari({MIN_BET}-{MAX_BET})!")
                self.bet_errorMsg.setVisible(True)
        else:
            self.bet_errorMsg.setText(f"Veuillez choisir un match SVP!")
            self.bet_errorMsg.setVisible(True)

    # end displayUserPlaceBetCallback()

    # ====================  A D M I N   =========================

    def displayAdminListUsersCallback(self):
        self.ui_admin_user_view = UserView(self)
        self.ui_admin_user_view.refresh_datas()

    def displayAdminPaymentsCallback(self):
        self.ui_adm_payments = PaymentsView(self)
        self.ui_adm_payments.refresh_datas()

    def goToBetBoxCallback(self, btn: QPushButton):
        """
            Mettre a jour certaines donnees placer un pari. 
            Réf. fonction `bet_info_content` 
            Arguments:
                - `btn: QPushButton` -> le bouton cliqué

        """
        obj_name = btn.objectName()
        print(f"Match id : {obj_name}")
        #
        if not obj_name:
            None

        match_info = self.match_controller.get_match_by_id(obj_name)
        if match_info:

            self.eq_1.setVisible(True)
            self.eq_2.setVisible(True)
            self.usr_scr1.setVisible(True)
            self.usr_scr2.setVisible(True)
            self.match_cote.setVisible(True)
            # fill inputs
            self.eq_1.setText(match_info['eq_rec'])
            self.eq_2.setText(match_info['eq_vis'])
            self.match_cote.setText(f"Cote: {match_info['cote']} ")
            # ajouter objectName pour connaitre l'ID match
            self.BET_match_id.setText(match_info['match_id'])

    def refresh_dashboard(self):
        """
            - Mettre a jour les données du Dashboard :
                - Username
                - balance
        """
        print("To refresh dashboard")

    def logoutCallback(self):
        self.parent.startMainView()
        self.close()

    def emptyField(self):
        self.eq_1.setVisible(False)
        self.eq_2.setVisible(False)
        self.usr_scr1.setVisible(False)
        self.usr_scr2.setVisible(False)
        self.match_cote.setVisible(False)
        # fill inputs
        self.eq_1.clear()
        self.eq_2.clear()
        self.usr_scr1.clear()
        self.usr_scr2.clear()
        self.match_cote.clear()
        # ajouter objectName pour connaitre l'ID match
        self.BET_match_id.clear()
        # 
        self.bet_amount_field.setText(str(25))