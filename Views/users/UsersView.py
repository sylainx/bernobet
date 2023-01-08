from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, \
    QRadioButton, QComboBox, QDateEdit, QButtonGroup, QMessageBox, QDateTimeEdit, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QDoubleValidator
import random
from SessionManager import SessionManager
from controllers.Controller import Controller
from datetime import datetime

TABLE_NAME = "users"
PATH_NAME = "./db/database.db"
COLUMNS_NAME = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "last_name": "varchar(255)",
    "first_name": "varchar(255)",
    "gender": "varchar(255)",
    "birth_date": "DATE",
    "phone": "varchar(255)",
    "nif": "varchar(255)",
    "username": "varchar(255)",
    "password": "varchar(255)",
    "balance": "DOUBLE",
    "status": "varchar(255)",
    "is_admin": "integer(5)"
}


class UserView(QDialog):
    def __init__(self, parent):
        super(UserView, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(" User - JetBrainsBet")
        self.setMinimumSize(1000, 600)
        # START TABLE
        self.user_id = None
        self.controller = Controller(PATH_NAME)
        # END TABLE
        self.mainLayout = QHBoxLayout()
        self.createTable()
        self.center()
        self.ui()
        self.listTableWidget()

    def ui(self):
        self.groupBox = QGroupBox()
        self.groupBox.setMinimumSize(350, 600)

        scrollVertLayout = QScrollArea()
        scrollVertLayout.setWidgetResizable(True)
        scrollVertLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        scrollVertLayout.setLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        doubleValidator = QDoubleValidator()

        # enregistrer match
        self.lbl_title_match = QLabel("Utilisateurs :")
        self.lbl_title_match.setStyleSheet("text-align: center;")
        # code
        self.code_user_lbl = QLabel("Code utilisateur: ")
        self.code_user_QLE = QLineEdit()
        self.code_user_QLE.setEnabled(False)
        # last name
        self.last_name_lbl = QLabel("nom: ")
        self.last_name_Field = QLineEdit()
        self.last_name_Field.setPlaceholderText("Lastname")
        # first name
        self.first_name_lbl = QLabel("Prenom: ")
        self.first_name_Field = QLineEdit()
        self.last_name_Field.setPlaceholderText("first name")
        # gender
        self.gender_lbl = QLabel("Sexe: ")
        genders = ["Masculin", "Feminin"]
        self.gender_QCB = QComboBox()
        self.gender_QCB.addItems(genders)
        # birth date
        self.birth_date_lbl = QLabel("Equipe receveuse: ")
        self.birth_date_QDTM = QDateEdit()
        self.birth_date_QDTM.setDisplayFormat("dd/MM/yyyy")
        self.birth_date_QDTM.setCalendarPopup(True)
        # phone
        self.phone_lbl = QLabel("Tel: ")
        self.phone_Field = QLineEdit()
        # nif/cin
        self.nif_lbl = QLabel("NIF/CIN: ")
        self.nif_Field = QLineEdit()
        # Username
        self.username_lbl = QLabel("Username: ")
        self.username_Field = QLineEdit()
        # Password
        self.pwd_lbl = QLabel("Password: ")
        self.pwd_Field = QLineEdit()
        self.pwd_Field.setEchoMode(QLineEdit.Password)
        # confirm Password
        self.confirm_pwd_lbl = QLabel("Confirmer Password: ")
        self.confirm_pwd_Field = QLineEdit()
        self.confirm_pwd_Field.setEchoMode(QLineEdit.Password)
        # Balance
        self.balance_lbl = QLabel("Balance: ")
        self.balance_Field = QLineEdit()
        self.balance_Field.setValidator(doubleValidator)
        # etat
        self.status_lbl = QLabel("Etat: ")
        etats = ["A", "S", "F"]
        self.status_QCB = QComboBox()
        self.status_QCB.addItems(etats)
        # is admin
        self.isAdmin_lbl = QLabel("Admin: ")
        self.groupe_admin_RDB = QButtonGroup()
        self.yesAdmin_QPB = QRadioButton("Oui")
        self.noAdmin_QPB = QRadioButton("Non")
        self.noAdmin_QPB.setChecked(True)
        self.groupe_admin_RDB.addButton(self.yesAdmin_QPB)
        self.groupe_admin_RDB.addButton(self.noAdmin_QPB)
        #
        #
        #
        #
        self.errorMsgLbl = QLabel("")
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red; margin: 5px 0px")

        self.saveDataBtn = QPushButton('Enregistrer', self)
        self.updateDataBtn = QPushButton('Modifier', self)
        self.deleteDataBtn = QPushButton('Supprimer', self)
        # disable
        self.updateDataBtn.setEnabled(False)
        self.deleteDataBtn.setEnabled(False)

        # add to layout
        # self.verticalLayout.addWidget(
        #     self.lbl_title_match, alignment=Qt.AlignCenter)
        # fields
        self.verticalLayout.addWidget(self.code_user_lbl)
        self.verticalLayout.addWidget(self.code_user_QLE)
        self.verticalLayout.addWidget(self.last_name_lbl)
        self.verticalLayout.addWidget(self.last_name_Field)
        self.verticalLayout.addWidget(self.first_name_lbl)
        self.verticalLayout.addWidget(self.first_name_Field)
        self.verticalLayout.addWidget(self.username_lbl)
        self.verticalLayout.addWidget(self.username_Field)
        self.verticalLayout.addWidget(self.gender_lbl)
        self.verticalLayout.addWidget(self.gender_QCB)
        self.verticalLayout.addWidget(self.birth_date_lbl)
        self.verticalLayout.addWidget(self.birth_date_QDTM)
        self.verticalLayout.addWidget(self.phone_lbl)
        self.verticalLayout.addWidget(self.phone_Field)
        self.verticalLayout.addWidget(self.nif_lbl)
        self.verticalLayout.addWidget(self.nif_Field)
        # self.verticalLayout.addWidget(self.pwd_lbl)
        # self.verticalLayout.addWidget(self.pwd_Field)
        # self.verticalLayout.addWidget(self.confirm_pwd_lbl)
        # self.verticalLayout.addWidget(self.confirm_pwd_Field)
        self.verticalLayout.addWidget(self.balance_lbl)
        self.verticalLayout.addWidget(self.balance_Field)
        self.verticalLayout.addWidget(self.status_lbl)
        self.verticalLayout.addWidget(self.status_QCB)
        self.verticalLayout.addWidget(self.isAdmin_lbl)
        self.verticalLayout.addWidget(self.yesAdmin_QPB)
        self.verticalLayout.addWidget(self.noAdmin_QPB)
        # error
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
        self.saveDataBtn.clicked.connect(lambda: self.manageCreationUser())
        self.updateDataBtn.clicked.connect(lambda: self.manageUpdateUser())
        self.deleteDataBtn.clicked.connect(lambda: self.manageDeleteUser())

    def connectTo(self,):
        self.parent.show()
        # passer details utilisateur qui est connecté
        self.close()
    # end connectTo

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

    def listTableWidget(self):

        self.table_WDG = QTableWidget()
        self.table_WDG.setStyleSheet("background-color: #667373;color: white")
        self.table_WDG.cellClicked.connect(lambda: self.eventOnTable())
        header = ("Code", "Nom", "Username", "Tel",
                  "Balance", "Sexe", "Date Naissance")

        self.table_WDG.setColumnCount(len(header))
        self.table_WDG.setHorizontalHeaderLabels(header)
        # add layout
        self.mainLayout.addWidget(self.table_WDG)

    def load_datas(self, list_users):
        """
        cette fonction va remplir le tableau avec des elements
        """
        self.table_WDG.setRowCount(len(list_users))
        # self.table_WDG.setStyleSheet(
        #   "background-color: #2C2C2C;\n"
        # )

        row = 0

        for i in list_users:
            self.table_WDG.setItem(row, 0, QTableWidgetItem(str(i[0])))
            self.table_WDG.setItem(
                row, 1, QTableWidgetItem(str(f"{i[1]} {i[2]}")))
            self.table_WDG.setItem(row, 2, QTableWidgetItem(str(i[7])))
            self.table_WDG.setItem(row, 3, QTableWidgetItem(str(i[5])))
            self.table_WDG.setItem(row, 4, QTableWidgetItem(str(i[9])))
            self.table_WDG.setItem(row, 5, QTableWidgetItem(str(i[3])))
            self.table_WDG.setItem(row, 6, QTableWidgetItem(str(i[4])))
            row += 1

    def refresh_datas(self):
        """
        Cette fonction permet de mettre a jour les donnees des utilisateurs apres certaines operations
        """
        get_users = self.controller.select(TABLE_NAME)
        if get_users:
            self.load_datas(get_users)
        else:
            self.empty_data()
    # end refresh_datas

    def empty_data(self,):
        """
        Est appellee lorsqu'il n'y a pas de donnees a afficher dans le tableau
        """
        print("empty datas")
    # end empty_data

    # **************************************************************

    def get_isAdminChoice(self):
        """
            Determiner quel RadioButton est selectionnee
            `isAdmin`
        """
        selected_btn = self.groupe_admin_RDB.checkedButton()
        if selected_btn and selected_btn.lower() == 'yes'.lower():
            return True
        return False

    def manageCreationUser(self):
        """
            Logique de traitment pour enregistrer un user
        """
        code_user = self.code_user_QLE.text()
        last_name = self.last_name_Field.text()
        first_name = self.first_name_Field.text()
        gender = self.gender_QCB.currentText()
        birth_date = self.birth_date_QDTM.dateTime().toPyDateTime()
        phone = self.phone_Field.text()
        nif = self.nif_Field.text()
        username = self.username_Field.text()
        pwd = 1234
        # pwd = self.pwd_Field.text()
        # cpwd = self.confirm_pwd_Field.text()
        etat = self.status_QCB.currentText()
        balance = self.gender_QCB.currentText()
        # ternary : TrueValue if cond else FalseValue
        admin = 1 if self.get_isAdminChoice() else 0

        self.errorMsgLbl.setVisible(False)

        if self._isFormFielsValid(
                code_user, last_name, first_name, gender, birth_date, phone, nif, username, etat, balance):

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

                print(f"user data: {user_data}")
                # Envoi des données de l'utilisateur au contrôleur pour enregistrement
                result = self.controller.insert(
                    TABLE_NAME, user_data.items())

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
           
        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def _isFormFielsValid(self, code_user, last_name, first_name, gender, birth_date, phone, nif, username, etat, balance):

        if code_user != "" and last_name != "" and first_name != "" and gender != "" and \
            birth_date != "" and phone != "" and nif != "" and username != "" \
                and etat != "" and balance != "":
            
            return True

        return False

    def type_de_match_pressed(self):
        print("type de match")
        return False

    def vider(self):
        # buttons
        self.saveDataBtn.setEnabled(True)
        self.updateDataBtn.setEnabled(False)
        self.deleteDataBtn.setEnabled(False)

        self.code_user_QLE.clear()
        self.last_name_Field.clear()
        self.first_name_Field.clear()
        self.gender_QCB.setCurrentIndex(0)
        self.birth_date_lbl.clear()
        self.phone_Field.clear()
        self.nif_Field.clear()
        self.username_Field.clear()
        self.pwd_Field.clear()
        self.confirm_pwd_Field.clear()
        self.balance_Field.clear()
        self.noAdmin_QPB.setChecked(True)
        self.status_QCB.setCurrentIndex(0)
    # end vider()

    def eventOnTable(self):

        self.saveDataBtn.setEnabled(False)
        self.updateDataBtn.setEnabled(True)
        self.deleteDataBtn.setEnabled(True)

        index = self.table_WDG.currentRow()
        id = self.table_WDG.item(index, 0).text()
        if id:
            where_clause = f" id= {id}"
            row = self.controller.select(TABLE_NAME, where_clause)
            if row:
                # fill form
                # self.table_WDG.item(index, 0).text()
                self.code_user_QLE.setText(str(row[0][0]))
                self.last_name_Field.setText(str(row[0][1]))
                self.first_name_Field.setText(str(row[0][2]))
                self.gender_QCB.setCurrentText(row[0][3])
                # self.birth_date_QDTM.setDateTime(datetime.fromisoformat(str(row[4])))
                self.phone_Field.setText(str(row[0][5]))
                self.nif_Field.setText(str(row[0][6]))
                self.username_Field.setText(str(row[0][7]))
                self.pwd_Field.setText(str(row[0][8]))
                self.confirm_pwd_Field.setText(str(""))
                self.balance_Field.setText(str(row[0][9]))
                self.gender_QCB.setCurrentText(row[0][10])

            else:
                print("No data found")
        else:
            print("No id selected")

    def manageUpdateUser(self):
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
        # pwd = self.pwd_Field.text()
        # cpwd = self.confirm_pwd_Field.text()
        etat = self.status_QCB.currentText()
        balance = self.balance_Field.text()
        self.errorMsgLbl.setVisible(False)

        if self._isFormFielsValid(
                code_user,last_name, first_name, gender, birth_date, phone, nif, username, etat, balance):

            if float(balance):
                balance = float(balance)
                # Récupération des données de l'utilisateur à partir des widgets

                user_data = [
                    ("last_name", last_name),
                    ("first_name", first_name),
                    ("gender", gender),
                    ("birth_date", birth_date),
                    ("phone", phone),
                    ("nif", nif),
                    ("username", username),
                    ("balance", balance),
                    ("status", etat),
                ]
                
                where_data = f"id = {code_user}"

                print(f"user data: {user_data}")

                # Envoi des données de l'utilisateur au contrôleur pour enregistrement
                result = self.controller.update(
                    TABLE_NAME, user_data, where_data)
                
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
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def manageDeleteUser(self):
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
