from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, \
    QRadioButton, QComboBox, QDateEdit, QButtonGroup, QMessageBox
from PyQt5.QtCore import Qt, QDate

from SessionManager import SessionManager
from controllers.Controller import Controller
from datetime import date as dateType

TABLE_NAME = "users"
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
    "status": "varchar(255)"
}


class Login(QDialog):
    def __init__(self, parent):
        super(Login, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(" Connexion - Bernobet")
        self.setFixedSize(500, 500)
        # START TABLE
        self.TABLE_NAME = 'users'
        self.controller = Controller("./db/database.db")
        # END TABLE
        self.mainLayout = QVBoxLayout()
        self.center()
        self.login()

    def login(self):
        self.groupBox = QGroupBox()
        self.groupBox.setFixedSize(350, 250)
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()

        self.usernameLbl = QLabel("Nom d'utilisateur :")
        self.usernameField = QLineEdit()
        self.usernameField.setPlaceholderText("Saisir votre nom d'utilisateur")
        self.passwordLbl = QLabel("Mot de passe: ")
        self.passwordField = QLineEdit()
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.passwordField.setPlaceholderText("Saisir votre mot de passe")

        self.errorMsgLbl = QLabel("")
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red; margin: 5px 0px")

        self.loginButton = QPushButton('Se connecter', self)
        self.account_exist = QLabel("Vous n'avez pas encore de compte ?")
        self.registerButton = QPushButton("S'inscrire", self)

        self.verticalLayout.addWidget(self.usernameLbl)
        self.verticalLayout.addWidget(self.usernameField)
        self.verticalLayout.addWidget(self.passwordLbl)
        self.verticalLayout.addWidget(self.passwordField)
        self.verticalLayout.addWidget(self.errorMsgLbl)
        self.verticalLayout.addWidget(self.loginButton)

        self.horizontalLayout.addWidget(self.account_exist)
        self.horizontalLayout.addWidget(self.registerButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        # self.loginButton.clicked.connect(self.connectTo)
        self.registerButton.clicked.connect(self.registerTo)

        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.mainLayout.setStretch(500, 500)
        self.setLayout(self.mainLayout)
        self.show()

        # ******************************************************** #
        self.loginButton.clicked.connect(lambda: self.manageUserConnection())

    def registerTo(self):
        # Ferme la fenêtre de login
        self.close()
        # Ouvre la fenêtre de register
        registerDialog = Register(self.parent)
        registerDialog.exec_()

    def loginTo(self):
        # Ferme la fenêtre de register
        self.close()
        # Ouvre la fenêtre de login
        loginDialog = Login(self.parent)
        loginDialog.exec_()

    def connectTo(self):
        self.parent.show()
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

    def manageUserConnection(self):
        username = self.usernameField.text()
        pwd = self.passwordField.text()
        self.errorMsgLbl.setVisible(False)

        if username != '' and pwd != '':

            # Récupération des données de l'utilisateur à partir des widgets
            user_data = f"username= '{username}' AND password= '{pwd}' "

            # Envoi des données de l'utilisateur au contrôleur pour enregistrement
            result = self.controller.select(self.TABLE_NAME, user_data)

            if result:
                # nettoyage
                self.vider()
                self.errorMsgLbl.setText("")
                self.errorMsgLbl.setVisible(False)
                # redirection
                SessionManager.setItem('userStorage',result)
                self.connectTo()
            else:
                self.errorMsgLbl.setText(
                    "Vos informations ne sont pas correctes!")
                self.errorMsgLbl.setVisible(True)

        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def vider(self):
        self.usernameField.text()
        self.passwordField.text()


class Register(QDialog):
    def __init__(self, parent):
        super(Register, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle(" Inscription")
        self.center()
        # START TABLE
        self.controller = Controller("./db/database.db")
        # self.dropTable() # uncomment only to drop table
        self.createTable()
        # END TABLE
        self.mainLayout = QVBoxLayout()
        self.register()

    def register(self):
        self.groupBox = QGroupBox()
        self.groupBox.setFixedSize(750, 550)
        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()

        self.title = QLabel("Inscription")

        # last Name
        self.lastNameLabel = QLabel('Nom')
        self.lastNameField = QLineEdit()
        self.lastNameField.setPlaceholderText("Saisir votre nom")
        self.lastNameField.setTextMargins(3, 0, 3, 0)
        self.lastNameField.setMinimumWidth(200)
        self.lastNameField.setMaximumWidth(300)

        # first Name
        self.firstNameLabel = QLabel('Prenom')
        self.firstNameField = QLineEdit()
        self.firstNameField.setPlaceholderText("Saisir votre prenom")
        self.firstNameField.setTextMargins(3, 0, 3, 0)
        self.firstNameField.setMinimumWidth(200)
        self.firstNameField.setMaximumWidth(300)

        # user Name
        self.userNameLabel = QLabel("Nom d'utilisateur")
        self.userNameField = QLineEdit()
        self.userNameField.setPlaceholderText("")
        self.userNameField.setTextMargins(3, 0, 3, 0)
        self.userNameField.setMinimumWidth(200)
        self.userNameField.setMaximumWidth(300)

        # sexe
        self.genderLabel = QLabel('Sexe')
        self.radioButton1 = QRadioButton("Masculin")
        self.radioButton1.setChecked(True)
        self.radioButton2 = QRadioButton("Feminin")
        self.horizontalLayout = QHBoxLayout()

        self.horizontalLayoutRadioButton = QHBoxLayout()
        self.genderGroup = QButtonGroup()

        self.horizontalLayoutRadioButton.addWidget(self.radioButton1)
        self.horizontalLayoutRadioButton.addWidget(self.radioButton2)
        self.genderGroup.addButton(self.radioButton1)
        self.genderGroup.addButton(self.radioButton2)

        # bithday
        self.dateOfBirthLabel = QLabel('Date de naissance')
        # Créez un objet QDateEdit
        self.dateOfBirthField = QDateEdit()

        # Récupérez la date courante
        current_date = QDate.currentDate()

        # Affichez la date courante dans le champ de date
        self.dateOfBirthField.setDate(current_date)
        self.dateOfBirthField.setDisplayFormat("dd/MM/yyyy")
        self.dateOfBirthField.setCalendarPopup(True)
        self.dateOfBirthField.setContentsMargins(3, 0, 3, 0)
        self.dateOfBirthField.setMinimumWidth(200)
        self.dateOfBirthField.setMaximumWidth(300)

        # Téléphone
        self.phoneLabel = QLabel('Telephone')
        self.phoneField = QLineEdit()
        self.phoneField.setPlaceholderText("Saisir votre numero de telephone")
        self.phoneField.setTextMargins(3, 0, 3, 0)
        self.phoneField.setMinimumWidth(200)
        self.phoneField.setMaximumWidth(300)

        # NIF/CIN
        self.nif_cinLabel = QLabel('Nif/Cin')
        self.nif_cinField = QLineEdit()
        self.nif_cinField.setPlaceholderText("Saisir votre nif ou votre cin")
        self.nif_cinField.setTextMargins(3, 0, 3, 0)
        self.nif_cinField.setMinimumWidth(200)
        self.nif_cinField.setMaximumWidth(300)

        # Password
        self.passwordLabel = QLabel('Mot de passe')
        self.passwordField = QLineEdit()
        self.passwordField.setPlaceholderText("Saisir un mot de passe")
        self.passwordField.setTextMargins(3, 0, 3, 0)
        self.passwordField.setMinimumWidth(200)
        self.passwordField.setMaximumWidth(300)
        self.passwordField.setEchoMode(QLineEdit.Password)

        # Confirm Password
        self.confirmPasswordLabel = QLabel('Confirmation de mot de passe')
        self.confirmPasswordField = QLineEdit()
        self.confirmPasswordField.setPlaceholderText(
            "Confirmer votre mot de passe")
        self.confirmPasswordField.setTextMargins(3, 0, 3, 0)
        self.confirmPasswordField.setMinimumWidth(200)
        self.confirmPasswordField.setMaximumWidth(300)
        self.confirmPasswordField.setEchoMode(QLineEdit.Password)

        # error MSG
        self.errorMsgLbl = QLabel('')
        self.errorMsgLbl.setStyleSheet("color:red; margin:5px 0px")

        # add row in formlayout
        self.Vbox.addWidget(self.lastNameLabel)
        self.Vbox.addWidget(self.lastNameField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.firstNameLabel)
        self.Vbox.addWidget(self.firstNameField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.userNameLabel)
        self.Vbox.addWidget(self.userNameField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.dateOfBirthLabel)
        self.Vbox.addWidget(self.dateOfBirthField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.genderLabel)
        self.Vbox.addLayout(self.horizontalLayoutRadioButton)
        self.verticalLayout.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.nif_cinLabel)
        self.Vbox.addWidget(self.nif_cinField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.phoneLabel)
        self.Vbox.addWidget(self.phoneField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.passwordLabel)
        self.Vbox.addWidget(self.passwordField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.confirmPasswordLabel)
        self.Vbox.addWidget(self.confirmPasswordField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)

        self.loginButton = QPushButton("Se connecter", self)
        self.account_exist = QLabel("Vous avez deja un compte ?")
        self.registerButton = QPushButton("S'inscrire", self)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.registerButton)

        self.horizontalLayout.addWidget(self.errorMsgLbl)
        self.horizontalLayout.addWidget(self.account_exist)
        self.horizontalLayout.addWidget(self.loginButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.registerButton.clicked.connect(
            lambda: self.manageUserRegistration())
        self.loginButton.clicked.connect(self.loginTo)
        self.show()
        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def registerTo(self):
        # Ferme la fenêtre de login
        self.close()
        # Ouvre la fenêtre de register
        registerDialog = Register(self.parent())
        registerDialog.exec_()

    def loginTo(self):
        # Ferme la fenêtre de register
        self.close()
        # Ouvre la fenêtre de login
        loginDialog = Login(self.parent())
        loginDialog.exec_()

    def center(self):
        # Ajout de cette méthode pour centrer la fenêtre
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def manageUserRegistration(self):
        #
        last_name = self.lastNameField.text()
        first_name = self.firstNameField.text()
        username = self.userNameField.text()
        gender = self.get_gender_selected()
        birth_date = self.dateOfBirthField.text()
        phone = self.phoneLabel.text()
        nif = self.nif_cinLabel.text()
        password = self.passwordField.text()
        confirmPassword = self.confirmPasswordField.text()

        balance = 0.0
        status = 'A'

        self.errorMsgLbl.setVisible(False)

        if last_name != '' and first_name != '' and username != '' and gender != '' and birth_date != '' \
                and phone != '' and nif != '' and password != '':

            if password == confirmPassword:

                # Récupération des données de l'utilisateur à partir des widgets
                user_data = {
                    "last_name": last_name,
                    "first_name": first_name,
                    "gender": gender,
                    "birth_date": birth_date,
                    "phone": phone,
                    "nif": nif,
                    "username": username,
                    "password": password,
                    "balance": balance,
                    "status": status
                }

                # Envoi des données de l'utilisateur au contrôleur pour enregistrement
                result = self.controller.insert(TABLE_NAME, user_data.items())

                if result:
                    # nettoyages
                    self.vider()
                    self.errorMsgLbl.setText("")
                    self.errorMsgLbl.setVisible(False)
                    # redirection
                    self.loginTo()
                else:
                    self.errorMsgLbl.setText(
                        "Veuillez verifier vos informations!")
                    self.errorMsgLbl.setVisible(True)
            else:
                self.errorMsgLbl.setText(
                    "Les mots de passe ne correspondent pas!")
                self.errorMsgLbl.setVisible(True)

        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def get_gender_selected(self):
        gnd_selected = self.genderGroup.checkedButton().text()
        if gnd_selected:
            return gnd_selected

        return ''

    def vider(self):

        self.lastNameField.clear()
        self.firstNameField.clear()
        self.userNameField.clear()
        self.dateOfBirthField.clear()
        self.phoneLabel.clear()
        self.nif_cinLabel.clear()
        self.passwordField.clear()
        self.confirmPasswordField.clear()

    # ********************************#

    def createTable(self):
        result = self.controller.create_table(
            table_name=TABLE_NAME, columns=COLUMNS_NAME.items())

        if not result:
            print(f"Table not created:\nResult: {result}")

    def dropTable(self):
        self.controller.drop(TABLE_NAME)
        print(f"Table ```{TABLE_NAME.upper()}``` is dropped")
