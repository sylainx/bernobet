from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, \
    QRadioButton, QComboBox, QDateEdit, QButtonGroup, QMessageBox, QDateTimeEdit, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QDoubleValidator
import random
from SessionManager import SessionManager
from controllers.Controller import Controller
from datetime import date

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


class AccountView(QDialog):
    def __init__(self, parent):
        super(AccountView, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(" Compte - JetBrainsBet")
        self.setMinimumSize(1000, 600)
        # START TABLE
        self.user_id = None
        self.controller = Controller(PATH_NAME)
        # END TABLE
        self.mainLayout = QHBoxLayout()
        self.createTable()
        self.center()
        self.ui()

    def ui(self):
        self.groupBox = QGroupBox()
        self.groupBox.setMinimumSize(500, 600)

        scrollVertLayout = QScrollArea()
        scrollVertLayout.setWidgetResizable(True)
        scrollVertLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        scrollVertLayout.setLayout(self.verticalLayout)
        # horizontal views
        self.horizontalLayout = QHBoxLayout()
        self.h1_Lyt = QHBoxLayout()
        self.h2_Lyt = QHBoxLayout()
        self.h3_Lyt = QHBoxLayout()
        self.h4_Lyt = QHBoxLayout()
        self.h5_Lyt = QHBoxLayout()
        doubleValidator = QDoubleValidator()

        # enregistrer match
        self.lbl_title_match = QLabel("Utilisateurs :")
        self.lbl_title_match.setStyleSheet("text-align: center;")
        # ******************** start box
        # title account
        self.title_account_QLB = QLabel("Compte")

        # user id
        self.user_id_lbl = QLabel("Code: ")
        self.user_id_Field = QLineEdit()
        self.user_id_Field.setPlaceholderText("Code")
        self.user_id_Field.setEnabled(False)
        # last name
        self.last_name_lbl = QLabel("Last name: ")
        self.last_name_Field = QLineEdit()
        self.last_name_Field.setPlaceholderText("Last name")
        # first name
        self.first_name_lbl = QLabel("Fist name: ")
        self.first_name_Field = QLineEdit()
        self.first_name_Field.setPlaceholderText("Firstname")
        # gender
        self.gender_lbl = QLabel("Gender: ")
        self.gender_QCB = QComboBox()
        gnd = ["Masculin", "Feminin"]
        self.gender_QCB.addItems(gnd)
        # birth date
        # min date
        self.min_date = QDate.currentDate().addYears(-18)
        self.birth_date_QDTM.setMaximumDate(self.min_date)
        self.birth_date_QDTM.setKeyboardTracking(False)
        self.birth_date_lbl = QLabel("Date de naissance: ")
        self.birth_date_Field = QDateEdit()
        self.birth_date_Field.setDisplayFormat("yyyy/MM/dd")
        self.birth_date_Field.setCalendarPopup(True)
        # phone
        self.phone_Field = QLineEdit()
        self.phone_Field.setPlaceholderText("Tel")
        # username
        self.username_Field = QLineEdit()
        self.username_Field.setPlaceholderText("Username")
        # nif
        self.nif_lbl = QLabel("Nif: ")
        self.nif_Field = QLineEdit()
        self.nif_Field.setPlaceholderText("Nif")
        # password
        self.password_lbl = QLabel("Mot de passe: ")
        self.password_Field = QLineEdit()
        self.password_Field.setEchoMode(QLineEdit.Password)
        self.password_Field.setPlaceholderText("Saisir le mot de passe")
        # confirm_password
        self.confirm_password_lbl = QLabel("Confirmer votre mot de passe: ")
        self.confirm_password_Field = QLineEdit()
        self.confirm_password_Field.setEchoMode(QLineEdit.Password)
        self.confirm_password_Field.setPlaceholderText(
            "Confirmer votre mot de passe")

        self.updateInfoBtn = QPushButton()
        self.updateInfoBtn.setStyleSheet(
            "background:rgb(244,102,47); color: white; padding: 5px;")
        # ******************** end box
        #
        #
        #
        #
        self.errorMsgLbl = QLabel("")
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red;")

        self.updateDataBtn = QPushButton('Modifier', self)

        # add to layout
        # self.verticalLayout.addWidget(
        #     self.lbl_title_match, alignment=Qt.AlignCenter)
        # fields
        self.verticalLayout.addWidget(self.user_id)

        self.h4_Lyt.addWidget(self.user_id_Field)
        self.h4_Lyt.addWidget(self.username_Field)
        self.verticalLayout.addLayout(self.h4_Lyt)

        self.h1_Lyt.addWidget(self.last_name_Field)
        self.h1_Lyt.addWidget(self.first_name_Field)
        self.verticalLayout.addLayout(self.h1_Lyt)

        self.h2_Lyt.addWidget(self.gender_QCB)
        self.h2_Lyt.addWidget(self.birth_date_Field)
        self.verticalLayout.addLayout(self.h2_Lyt)

        self.h5_Lyt.addWidget(self.phone_Field)
        self.h5_Lyt.addWidget(self.nif_Field)
        self.verticalLayout.addLayout(self.h5_Lyt)

        self.h3_Lyt.addWidget(self.password_Field)
        self.h3_Lyt.addWidget(self.confirm_password_Field)
        self.verticalLayout.addLayout(self.h3_Lyt)

        # error
        self.verticalLayout.addWidget(self.errorMsgLbl)

        self.horizontalLayout.addWidget(self.updateDataBtn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.mainLayout.setStretch(300, 500)
        self.setLayout(self.mainLayout)
        self.show()

        # ******************************************************** #
        self.updateDataBtn.clicked.connect(lambda: self.manageUpdateUser())

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

    def load_datas(self, data_user):
        """
        cette fonction va remplir le champs avec les donnees de 
        l'utilisateurs connecté
        """
        if data_user:
            print(f"LOad: {data_user}")
            self.user_id_Field.setText(str(data_user['id']))
            self.last_name_Field.setText(str(data_user['last_name']))
            self.first_name_Field.setText(str(data_user['first_name']))
            self.gender_QCB.setCurrentText(str(data_user['gender']))
            # self.birth_date_Field.setDate(
            #     date.fromisoformat(data_user['birth_date]']))
            self.phone_Field.setText(str(data_user['phone']))
            self.username_Field.setText(str(data_user['username']))
            self.nif_Field.setText(str(data_user['nif']))
            self.password_Field.setText(str(data_user['password']))
            self.confirm_password_Field.setText(str(data_user['password']))

        # end list
    def refresh_datas(self):
        """
        Cette fonction permet de mettre a jour les donnees des utilisateurs apres certaines operations
        """
        get_users = self.get_user_datas()
        print(f"REFRESH: {get_users}")
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

    def _isFormFielsValid(self, code_user, last_name, first_name, gender, birth_date, phone, nif, username, pwd, cpwd):

        if code_user != "" and last_name != "" and first_name != "" and gender != "" and \
            birth_date != "" and phone != "" and nif != "" and username != "" \
                and pwd != "" and cpwd != "":

            return True

        return False

    def type_de_match_pressed(self):
        print("type de match")
        return False

    def vider(self):
        # buttons

        self.user_id_Field.clear()
        self.last_name_Field.clear()
        self.first_name_Field.clear()
        self.gender_QCB.clear()
        self.birth_date_lbl.clear()
        self.phone_Field.clear()
        self.nif_Field.clear()
        self.username_Field.clear()
        self.password_Field.clear()
        self.confirm_password_Field.clear()
    # end vider()

    def manageUpdateUser(self):
        """
            Logiques de traitment pour modifier un utilisateur
        """
        print("click update")
        self.errorMsgLbl.setVisible(False)

        code_user = self.user_id_Field.text()
        last_name = self.last_name_Field.text()
        first_name = self.first_name_Field.text()
        gender = self.gender_QCB.currentText()
        birth_date = self.birth_date_Field.date().toPyDate()
        phone = self.phone_Field.text()
        username = self.username_Field.text()
        nif = self.nif_Field.text()
        pwd = self.password_Field.text()
        cpwd = self.confirm_password_Field.text()


        if self._isFormFielsValid(
                code_user, last_name, first_name, gender, birth_date, phone, nif, username, pwd, cpwd):
            if QDate.fromString(birth_date, "dd/MM/yyyy") > self.min_date:
                if pwd == cpwd:
                    # Récupération des données de l'utilisateur à partir des widgets

                    user_data = [
                        ("last_name", last_name),
                        ("first_name", first_name),
                        ("gender", gender),
                        ("birth_date", birth_date),
                        ("phone", phone),
                        ("nif", nif),
                        ("username", username),
                        ("password", pwd),
                    ]

                    where_data = f"id = {code_user}"

                    print(f"user data: {user_data}")

                    # Envoi des données de l'utilisateur au contrôleur pour enregistrement
                    result = self.controller.update(
                        TABLE_NAME, user_data, where_data)

                    # nettoyages
                    # self.vider()
                    QMessageBox.information(self, 'Modification', "Modification effectuée")
                    self.refresh_datas()
                    self.errorMsgLbl.setText("")
                    self.errorMsgLbl.setVisible(False)
                    # redirection
                    # self.call_back()
            
                # *****
                else:
                    self.errorMsgLbl.setText("Les mots de passe ne correspondent pas")
                    self.errorMsgLbl.setVisible(True)
                # *****
            else:
                self.errorMsgLbl.setText("Date incorrecte")
                self.errorMsgLbl.setVisible(True)
            # *****

        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def get_user_datas(self):
        user_table="users"
        user_id = SessionManager.getItem('userStorage')
        if user_id and int(user_id) > 0:
            where_data = f"id = {user_id}"
            result = self.controller.select(user_table, where_data)   
            if result :         
                data = {
                    'id': result[0][0],
                    'last_name': result[0][1],
                    'first_name': result[0][2],
                    'gender': result[0][3],
                    'birth_date': result[0][4],
                    'phone': result[0][5],
                    'nif': result[0][6],
                    'username': result[0][7],
                    'balance': result[0][9],
                    'status': result[0][10],
                    'password': result[0][8],
                    'is_admin': result[0][11],
                }

                print(f" accountView RESULR:  {result}")
                self.user_infos = data
                return self.user_infos

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
