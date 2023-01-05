from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, \
    QRadioButton, QComboBox, QDateEdit, QButtonGroup, QMessageBox, QDateTimeEdit
from PyQt5.QtCore import Qt, QDate
import random
from SessionManager import SessionManager
from controllers.Controller import Controller
from datetime import date as dateType

TABLE_NAME = "matchs"
PATH_NAME = "./db/database.db"
COLUMNS_NAME = {
    "id": "VARCHAR(25) PRIMARY KEY",
    "match_type": "varchar(255)",
    "pays": "varchar(255)",
    "date": "DATETIME",
    "eq_rec": "VARCHAR(255)",
    "eq_vis": "varchar(255)",
    "cote": "DOUBLE",
    "score_final": "varchar(255)",
    "etat": "varchar(255)",
}


class MatchView(QDialog):
    def __init__(self, parent):
        super(MatchView, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(" Matchs - JetBrainsBet")
        self.setMinimumSize(1000, 600)
        # START TABLE
        self.user_id = None
        self.controller = Controller(PATH_NAME)
        # END TABLE
        self.mainLayout = QVBoxLayout()        
        self.createTable()
        self.center()
        self.ui()


    def ui(self):
        self.groupBox = QGroupBox()
        self.groupBox.setMinimumSize(700, 600)
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()

        # enregistrer match
        self.lbl_title_match = QLabel("Enregistrer un match :")
        self.lbl_title_match.setStyleSheet("text-align: center;")
        # type de match
        typeMatch = ['Championnat', 'Coupe du monde', 'Eliminatoire', 'Amical']
        self.type_match_lbl = QLabel("Type de match: ")
        self.type_match_QCB = QComboBox()
        self.type_match_QCB.addItems(typeMatch)
        self.type_match_QCB.setPlaceholderText("Saisir le type de match")
        # country_match
        self.country_match_lbl = QLabel("Pays: ")
        self.country_match_Field = QLineEdit()
        self.country_match_Field.setPlaceholderText("Saisir le pays")
        # date match
        self.dateTimeMatch_lbl = QLabel("Date match: ")
        self.dateTimeMatch_Field = QDateTimeEdit()
        self.dateTimeMatch_Field.setDisplayFormat("dd/MM/yyyy")
        self.dateTimeMatch_Field.setCalendarPopup(True)
        # equipe receveuse
        self.equipe_receveuse_lbl = QLabel("Equipe receveuse: ")
        self.equipe_receveuse_Field = QLineEdit()
        # equipe deplacement
        self.equipe_deplacement_lbl = QLabel("Equipe en deplacement: ")
        self.equipe_deplacement_Field = QLineEdit()
        # cote
        self.cote_lbl = QLabel("Cote: ")
        self.cote_Field = QLineEdit()
        # etat
        self.etat_lbl = QLabel("Etat: ")
        etatMatch = ['N', 'E', 'T', 'A', 'S']
        self.etat_QCB = QComboBox()
        self.etat_QCB.addItems(etatMatch)
        #
        #
        #
        #
        self.errorMsgLbl = QLabel("")
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red; margin: 5px 0px")

        self.saveMatchBtn = QPushButton('Enregistrer', self)

        # add to layout
        self.verticalLayout.addWidget(
            self.lbl_title_match, alignment=Qt.AlignCenter)
        self.verticalLayout.addWidget(self.type_match_lbl)
        self.verticalLayout.addWidget(self.type_match_QCB)
        self.verticalLayout.addWidget(self.country_match_lbl)
        self.verticalLayout.addWidget(self.country_match_Field)
        self.verticalLayout.addWidget(self.dateTimeMatch_lbl)
        self.verticalLayout.addWidget(self.dateTimeMatch_Field)
        self.verticalLayout.addWidget(self.equipe_receveuse_lbl)
        self.verticalLayout.addWidget(self.equipe_receveuse_Field)
        self.verticalLayout.addWidget(self.equipe_deplacement_lbl)
        self.verticalLayout.addWidget(self.equipe_deplacement_Field)
        self.verticalLayout.addWidget(self.cote_lbl)
        self.verticalLayout.addWidget(self.cote_Field)
        self.verticalLayout.addWidget(self.etat_lbl)
        self.verticalLayout.addWidget(self.etat_QCB)
        self.verticalLayout.addWidget(self.errorMsgLbl)
        self.verticalLayout.addWidget(self.saveMatchBtn)

        # self.horizontalLayout.addWidget(self.account_exist)
        # self.horizontalLayout.addWidget(self.registerButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.mainLayout.setStretch(500, 500)
        self.setLayout(self.mainLayout)
        self.show()

        # ******************************************************** #
        self.saveMatchBtn.clicked.connect(lambda: self.manageCreationMatch())

    def connectTo(self,):
        self.parent.show()
        # passer details utilisateur qui est connecté
        self.close()

    def center(self):
        # Ajout de cette méthode pour centrer la fenêtre
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def connect(self):
        self.call_back()

    def call_back(self):
        self.parent.show()
        self.close()

    def manageCreationMatch(self):
        """
        toute la logique de traitment pour enregistrer un match
        """
        type_match = self.type_match_QCB.currentText()
        country_match = self.country_match_Field.text()
        date_match = self.dateTimeMatch_Field.date().toPyDate()
        eq_rec = self.equipe_receveuse_Field.text()
        eq_depl = self.equipe_deplacement_Field.text()
        cote = self.cote_Field.text()
        etat = self.etat_QCB.currentText()
        score = "0:0"
        self.errorMsgLbl.setVisible(False)

        isValid = self._isMatchFielsValid(
            type_match, country_match, date_match, eq_rec, eq_depl, cote, etat)

        if isValid:
            match_id = self.generate_id()
            # Récupération des données de l'utilisateur à partir des widgets
            user_data = {
                "id": match_id,
                "match_type": type_match,
                "pays": country_match,
                "date": date_match,
                "eq_rec": eq_rec,
                "eq_vis": eq_rec,
                "cote": cote,
                "score_final": score,
                "etat": etat,
            }

            # Envoi des données de l'utilisateur au contrôleur pour enregistrement
            result = self.controller.insert(TABLE_NAME, user_data.items())

            if result:
                # nettoyages
                self.vider()
                self.errorMsgLbl.setText("")
                self.errorMsgLbl.setVisible(False)
                # redirection
                self.call_back()
            else:
                self.errorMsgLbl.setText(
                    "Veuillez verifier vos informations!")
                self.errorMsgLbl.setVisible(True)

        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)



    def _isMatchFielsValid(self, type_match, country_match, date_match, eq_rec, eq_depl, cote, etat):

        if type_match != "" and country_match != "" and date_match != "" and \
                eq_rec != "" and eq_depl != "" and cote != "" and etat != "":
            return True

        return False

    def type_de_match_pressed(self):
        print("type de match")
        return False

    def vider(self):
        self.country_match_Field.text()
        self.dateTimeMatch_Field.text()

    def generate_id(self,):
        # Génère un nombre entier aléatoire compris entre 1 et 1000000
        suffix = str(random.randint(1000, 1000000))
        return "JB" + suffix



    # **************************************************************
    
    def createTable(self):
        """
        pour creer la table en question
        si elle est deja presente, elle ne fait rien
        """
        result = self.controller.create_table(
            table_name=TABLE_NAME, columns=COLUMNS_NAME.items())
        if not result:
            print(f"Table not created:\nResult: {result}")
        else:
            print(f"Table : ```{result}``` vient d'etre créée")

    def dropTable(self):
        """
        use it only for delete table
        """
        self.controller.drop(TABLE_NAME)
        print(f"Table ```{TABLE_NAME.upper()}``` is dropped")
