from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, \
    QRadioButton, QComboBox, QDateEdit, QButtonGroup, QMessageBox, QDateTimeEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QDoubleValidator
import random
from SessionManager import SessionManager
from controllers.Controller import Controller
from datetime import date as dateType

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


class MatchView(QDialog):
    def __init__(self, parent):
        super(MatchView, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(" Matchs - JetBrainsBet")
        self.setMinimumSize(1000, 600)
        self.center()
        # START TABLE
        self.user_id = None
        self.controller = Controller(PATH_NAME)
        self.createTable()
        # END TABLE
        self.mainLayout = QHBoxLayout()
        self.ui()
        self.listTableWidget()
        self.doubleValidator = QDoubleValidator()

    def ui(self):
        self.groupBox = QGroupBox()
        self.groupBox.setMinimumSize(300, 600)
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        
        # enregistrer match
        self.lbl_title_match = QLabel("Enregistrer un match: ")
        self.lbl_title_match.setStyleSheet("text-align: center;")
        # match_id
        self.match_id_lbl = QLabel("Id: ")
        self.match_id_Field = QLineEdit()
        self.match_id_Field.setEnabled(False)
        self.match_id_Field.setPlaceholderText("Cette valeur sera ajoutée automatique")
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
        self.dateTimeMatch_Field.setDisplayFormat("yyyy/MM/dd HH:mm:ss")
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
        # self.cote_Field.setValidator(self.doubleValidator)
        # etat
        self.etat_lbl = QLabel("Etat: ")
        etatMatch = ['N', 'E', 'T', 'A', 'S']
        self.etat_QCB = QComboBox()
        self.etat_QCB.addItems(etatMatch)
        #
        #
        #
        self.errorMsgLbl = QLabel()
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red; margin: 5px 0px")

        self.saveDataBtn = QPushButton('Enregistrer', self)
        self.updateDataBtn = QPushButton('Modifier', self)
        self.deleteDataBtn = QPushButton('Supprimer', self)

        # add to layout
        self.verticalLayout.addWidget(
            self.lbl_title_match, alignment=Qt.AlignCenter)
        self.verticalLayout.addWidget(self.match_id_lbl)
        self.verticalLayout.addWidget(self.match_id_Field)
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

        self.horizontalLayout.addWidget(self.saveDataBtn)
        self.horizontalLayout.addWidget(self.updateDataBtn)
        self.horizontalLayout.addWidget(self.deleteDataBtn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.mainLayout.setStretch(300, 500)
        self.setLayout(self.mainLayout)
        self.show()

        # ******************************************************** #
        self.saveDataBtn.clicked.connect(lambda: self.manageCreationMatch())
        self.updateDataBtn.clicked.connect(lambda: self.manageUpdateMatch())
        self.deleteDataBtn.clicked.connect(lambda: self.manageDeleteMatch())

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

    # **************************************************************

    def listTableWidget(self):

        self.table_WDG = QTableWidget()
        self.table_WDG.setStyleSheet("background-color: #667373;color: white")
        self.table_WDG.cellClicked.connect(lambda: self.eventOnTable())
        header = ("ID", "Type", "Equipes", "Pays", "Date",
                  "Cote", "Score", "Etat")

        self.table_WDG.setColumnCount(len(header))
        self.table_WDG.setHorizontalHeaderLabels(header)
        # add layout
        self.mainLayout.addWidget(self.table_WDG)

    def load_datas(self, list_datas):
        """
        cette fonction va remplir le tableau avec des elements
        - Arguments:
            - list_datas : `list[()]`
        - Return `NoneType`
        """
        self.table_WDG.setRowCount(len(list_datas))
       
        row = 0
        for i in list_datas:
            
            self.table_WDG.setItem(row, 0, QTableWidgetItem(str(i[0])))
            self.table_WDG.setItem(
                row, 1, QTableWidgetItem(str(f"{i[1]}")))
            self.table_WDG.setItem(row, 2, QTableWidgetItem(str(f"{i[4]} - {i[5]}")))
            self.table_WDG.setItem(
                row, 3, QTableWidgetItem(str(f"{i[2]}")))
            self.table_WDG.setItem(row, 4, QTableWidgetItem(str(i[3])))
            self.table_WDG.setItem(row, 5, QTableWidgetItem(str(i[6])))
            self.table_WDG.setItem(row, 6, QTableWidgetItem(str(i[7])))
            self.table_WDG.setItem(row, 7, QTableWidgetItem(str(i[8])))
            row += 1

    def refresh_datas(self):
        """
        Cette fonction permet de mettre a jour les donnees des utilisateurs apres certaines operations
        """
        get_datas = self.controller.select(TABLE_NAME)
        if get_datas:
            self.load_datas(get_datas)
        else:
            self.empty_data()

    def empty_data(self,):
        """
        Est appellee lorsqu'il n'y a pas de donnees a afficher dans le tableau
        """
        print("empty datas")
    # end empty_data

    def manageCreationMatch(self):
        """
            toute la logique de traitment pour enregistrer un match
        """
        type_match = self.type_match_QCB.currentText()
        country_match = self.country_match_Field.text()
        date_match = self.dateTimeMatch_Field.dateTime().toPyDateTime()
        eq_rec = self.equipe_receveuse_Field.text()
        eq_depl = self.equipe_deplacement_Field.text()
        cote = self.cote_Field.text()
        etat = self.etat_QCB.currentText()
        score = "0:0"
        self.errorMsgLbl.setVisible(False)

        isValid = self._isMatchFielsValid(
            type_match, country_match, date_match, eq_rec, eq_depl, cote, etat)

        if isValid:
            if float(cote):
                cote = float(cote)
                match_id = self.generate_id()
                # Récupération des données de l'utilisateur à partir des widgets
                match_data = {
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
                result = self.controller.insert(TABLE_NAME, match_data.items())

                # if result:
                    # nettoyages
                self.vider()
                self.refresh_datas()
                self.errorMsgLbl.setText("")
                self.errorMsgLbl.setVisible(False)
                # redirection
                # self.call_back()
                # else:
                #     self.errorMsgLbl.setText(
                #         "Veuillez verifier vos informations!")
                #     self.errorMsgLbl.setVisible(True)
            # *****
            else:
                print("Error: cote not convert")
                self.errorMsgLbl.setText("Le cote doit etre un nombre decimal!")
                self.errorMsgLbl.setVisible(True)
        else:
            print("Error: not valid")
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def _isMatchFielsValid(self, type_match, country_match, date_match, eq_rec, eq_depl, cote:str, etat):

        if type_match != "" and country_match != "" and date_match != "" and \
                eq_rec != "" and eq_depl != "" and cote != "" and etat != "":
            
            if cote.isnumeric():
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

    def manageUpdateMatch(self):
        print("Update")
        """
            Logiques de traitment pour modifier un utilisateur
        """
        code_user = self.code_user_QLE.text()
        last_name = self.last_name_Field.text()
        first_name = self.first_name_Field.text()
        gender = self.gender_QCB.currentText()
        birth_date = self.birth_date_QDTM.dateTime().toPyDateTime()
        phone = self.phone_Field.text()
        nif = self.nif_Field.text()
        username = self.username_Field.text()
        pwd = self.pwd_Field.text()
        cpwd = self.confirm_pwd_Field.text()
        etat = self.status_QCB.currentText()
        balance = self.balance_Field.text()
        # ternary : a if cond else b
        admin = 1 if self.get_isAdminChoice() else 0
        self.errorMsgLbl.setVisible(False)

        if self._isFormFielsValid(
                code_user, last_name, first_name, gender, birth_date, phone, nif, username, pwd, cpwd, etat, balance):

            if pwd == cpwd:

                if float(balance):
                    balance = float(balance)
                    # Récupération des données de l'utilisateur à partir des widgets

                    user_data = {
                        "last_name": last_name,
                        "first_name": first_name,
                        "gender": gender,
                        "birth_date": birth_date,
                        "phone": phone,
                        "nif": nif,
                        "username": username,
                        "password": pwd,
                        "balance": balance,
                        "status": etat,
                        "is_admin": admin,
                    }

                    where_data = f"id = {code_user}"

                    print(f"user data: {user_data}")
                    # Envoi des données de l'utilisateur au contrôleur pour enregistrement
                    result = self.controller.update(
                        TABLE_NAME, user_data, where_data)
                    result = None
                    if result:
                        # nettoyages
                        self.vider()
                        self.refresh_datas()
                        self.errorMsgLbl.setText("")
                        self.errorMsgLbl.setVisible(False)
                        # redirection
                        # self.call_back()
                    else:
                        self.errorMsgLbl.setText(
                            "Veuillez verifier vos informations!")
                        self.errorMsgLbl.setVisible(True)
                # *****
                else:
                    print("Le montant est inforrect")
            # *****
            else:
                print("Les mots de passe ne correspondent pas")
        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def manageDeleteMatch(self):
        print("Delete")
        """
            Logiques de traitment pour supprimer un utilisateur
        """
        code_user = self.code_user_QLE.text()
        if code_user:
            where_clause = f" id = {code_user} "
            self.controller.delete(TABLE_NAME, where_clause)
            self.vider()
            self.refresh_datas()

    def eventOnTable(self):

        self.saveDataBtn.setEnabled(False)
        self.updateDataBtn.setEnabled(True)
        self.deleteDataBtn.setEnabled(True)

        index = self.table_WDG.currentRow()
        id = self.table_WDG.item(index, 0).text()
        if id:
            where_clause = f" id= '{id}'"
            row = self.controller.select(TABLE_NAME, where_clause)
            if row:
                # fill form
                self.match_id_Field.setText(str(row[0][0]))
                self.type_match_QCB.setCurrentText(str(row[0][1]))
                self.country_match_Field.setText(str(row[0][2]))
                # self.dateTimeMatch_Field.setDateTime(datetime.fromisoformat(str(row[4])))
                self.equipe_receveuse_Field.setText(row[0][4])
                self.equipe_deplacement_Field.setText(str(row[0][5]))
                self.cote_Field.setText(str(row[0][6]))
                self.etat_QCB.setCurrentText(str(row[0][7]))

            else:
                print("No data found")
        else:
            print("No id selected")

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
