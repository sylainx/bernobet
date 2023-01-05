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
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "compte_id": "varchar(255)",
    "match_id": "INTEGER(255)",
    "date_pari": "varchar(255)",
    "montant": "DOUBLE",
    "score_prevu": "VARCHAR(255)",    
}


class PariView(QDialog):
    def __init__(self, parent):
        super(PariView, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Pari - JetBrainsBet")
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
        self.lbl_title_box = QLabel("Parier sur un match :")
        self.lbl_title_box.setStyleSheet("text-align: center;")
        # montant pari
        self.montant_lbl = QLabel("Pays: ")
        self.montant_Field = QLineEdit()
        self.montant_Field.setPlaceholderText("Saisir le pays")
        # date match
        self.score_prevu_lbl = QLabel("Date match: ")
        self.score_prevu_Field = QDateTimeEdit()
        self.score_prevu_Field.setDisplayFormat("dd/MM/yyyy")
        self.score_prevu_Field.setCalendarPopup(True)
        
        #
        #
        #
        #
        self.errorMsgLbl = QLabel("")
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red; margin: 5px 0px")

        self.saveParisBtn = QPushButton('Enregistrer', self)

        # add to layout
        self.verticalLayout.addWidget(
            self.lbl_title_box, alignment=Qt.AlignCenter)
        self.verticalLayout.addWidget(self.montant_lbl)
        self.verticalLayout.addWidget(self.montant_Field)
        self.verticalLayout.addWidget(self.saveParisBtn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.mainLayout.setStretch(500, 500)
        self.setLayout(self.mainLayout)
        self.show()

        # ******************************************************** #
        self.saveParisBtn.clicked.connect(lambda: self.manageCreationParis())

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

    def manageCreationParis(self):
        """
        toute la logique de traitment pour enregistrer un match
        """
        montant = self.montant_Field.text()
        
        score = "0:0"
        self.errorMsgLbl.setVisible(False)

        isValid = self._isMatchFielsValid(montant)

        if isValid:
            match_id = self.generate_id()
            # Récupération des données de l'utilisateur à partir des widgets
            user_data = {
                "id": match_id,
                "compte_id": '',
                "match_id": '',
                "date_pari": '',
                "montant": '',
                "score_prevu": '',
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



    def _isMatchFielsValid(self, montant):

        if montant != "":
            return True

        return False

    def vider(self):
        self.montant_Field.text()
        

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
