import time
from datetime import date
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, \
    QLineEdit, QComboBox, QDateEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTimeEdit
from PyQt5.QtCore import Qt, QDate
from app.controllers.MatchController import MatchController
from app.models.Match import Match


class MatchDialog(QDialog):
    def __init__(self, parent):
        super(MatchDialog, self).__init__(parent)
        self.setFixedSize(800, 700)
        self.setStyleSheet(open("../../assets/css/style.css", "r").read())
        self.setWindowTitle(" Gestion matchs | GeeBet")
        self.center()
        self.match = Match()
        self.mainLayout = QHBoxLayout()
        self.initUI()
        self.loadDatas()

    def initUI(self):

        self.groupBox = QGroupBox()
        self.groupBox.setObjectName("grpbx")
        self.groupBox.setFixedSize(670, 670)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()

        header = (
            "Id", "Type Match", "Pays", "Date Match", "Heure Match", "Equipe Receveuse", "Equipe Visiteuse", "Cote",
            "Score", "Etat")

        # Titre de la fenetre
        self.title = QLabel("Gestion de matchs")

        # Code du match
        self.code = QLineEdit()
        self.code.setEnabled(False)

        # id de la table match
        self.table_id = QLineEdit()
        self.table_id.setEnabled(False)

        # Champ type match
        self.typeMatchLabel = QLabel('Type Match')
        type = ["Championnat", "Coupe du monde", "Eliminatoire", "Amical"]
        self.typeMatch = QComboBox()
        self.typeMatch.addItems(type)
        self.typeMatch.setContentsMargins(3, 0, 3, 0)
        self.typeMatch.setMinimumWidth(200)
        self.typeMatch.setMaximumWidth(300)

        # Champ pays
        self.countryLabel = QLabel('Pays')
        country = ["Espagne", "Allemagne", "Angleterre",
                   "Italie", "Brezil", "Argentine"]
        self.countryField = QComboBox()
        self.countryField.addItems(country)
        self.countryField.setContentsMargins(3, 0, 3, 0)
        self.countryField.setMinimumWidth(200)
        self.countryField.setMaximumWidth(300)

        # Champ heure match
        self.matchTimeLabel = QLabel("Heure match")
        self.matchTimeField = QTimeEdit()
        self.matchTimeField.setContentsMargins(3, 0, 3, 0)
        self.matchTimeField.setMinimumWidth(200)
        self.matchTimeField.setMaximumWidth(300)

        # Champ equipe receveuse
        self.matchTeam1Label = QLabel("Equipe receveuse")
        self.matchTeam1Field = QLineEdit()
        self.matchTeam1Field.setPlaceholderText(
            "Saisir le nom de l'equipe receveuse")
        self.matchTeam1Field.setTextMargins(3, 0, 3, 0)
        self.matchTeam1Field.setMinimumWidth(200)
        self.matchTeam1Field.setMaximumWidth(300)

        self.horizontalLayout = QHBoxLayout()

        # Champ date match
        self.matchDateLabel = QLabel('Date match')
        self.matchDateField = QDateEdit()
        current_date = QDate.currentDate()

        # Affichez la date courante dans le champ de date
        self.matchDateField.setDate(current_date)
        self.matchDateField.setDisplayFormat("dd/MM/yyyy")
        self.matchDateField.setCalendarPopup(True)
        self.matchDateField.setContentsMargins(3, 0, 3, 0)
        self.matchDateField.setMinimumWidth(200)
        self.matchDateField.setMaximumWidth(300)

        # Champ equipe visiteuse
        self.matchTeam2Label = QLabel('Equipe receveuse')
        self.matchTeam2Field = QLineEdit()
        self.matchTeam2Field.setPlaceholderText(
            "Saisir le nom de l'equipe visiteuse")
        self.matchTeam2Field.setTextMargins(3, 0, 3, 0)
        self.matchTeam2Field.setMinimumWidth(200)
        self.matchTeam2Field.setMaximumWidth(300)

        # Champ Cote
        self.matchCoteLabel = QLabel('Cote')
        self.matchCoteField = QLineEdit()
        self.matchCoteField.setPlaceholderText("Saisir le cote du match")
        self.matchCoteField.setTextMargins(3, 0, 3, 0)
        self.matchCoteField.setMinimumWidth(200)
        self.matchCoteField.setMaximumWidth(300)

        # Champ score match
        self.matchScoreLabel = QLabel('Score du match')
        self.matchScoreField = QLineEdit()
        self.matchScoreField.setPlaceholderText("Saisir le score du match")
        self.matchScoreField.setContentsMargins(3, 0, 3, 0)
        self.matchScoreField.setMinimumWidth(200)
        self.matchScoreField.setMaximumWidth(300)

        # Champ etat match
        self.matchStateLabel = QLabel('Etat du match')
        self.matchStateTab = ["N", "E", "T", "A", "S"]
        self.matchStateField = QComboBox()
        self.matchStateField.addItems(self.matchStateTab)
        self.matchStateField.setContentsMargins(3, 0, 3, 0)
        self.matchStateField.setMinimumWidth(200)
        self.matchStateField.setMaximumWidth(300)

        # Ajout des colonnes dans le add formlayout
        self.Vbox.addWidget(self.typeMatchLabel)
        self.Vbox.addWidget(self.typeMatch)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.countryLabel)
        self.Vbox.addWidget(self.countryField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchDateLabel)
        self.Vbox.addWidget(self.matchDateField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchTimeLabel)
        self.Vbox.addWidget(self.matchTimeField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchTeam1Label)
        self.Vbox.addWidget(self.matchTeam1Field)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchTeam2Label)
        self.Vbox.addWidget(self.matchTeam2Field)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchCoteLabel)
        self.Vbox.addWidget(self.matchCoteField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchStateLabel)
        self.Vbox.addWidget(self.matchStateField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchScoreLabel)
        self.Vbox.addWidget(self.matchScoreField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)

        self.new_match_info_button = QPushButton("Nouveau", self)
        self.new_match_info_button.setObjectName("btn")
        self.save_match_info_button = QPushButton("Enregistrer", self)
        self.save_match_info_button.setObjectName("btn")
        self.update_match_info_button = QPushButton("Modifier", self)
        self.update_match_info_button.setObjectName("btn")
        self.delete_match_info_button = QPushButton("Supprimer", self)
        self.delete_match_info_button.setObjectName("btn")

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.new_match_info_button)
        self.horizontalLayout.addWidget(self.save_match_info_button)
        self.horizontalLayout.addWidget(self.update_match_info_button)
        self.horizontalLayout.addWidget(self.delete_match_info_button)

        self.groupBox.setLayout(self.verticalLayout)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.show()
        self.mainLayout.addWidget(self.groupBox)

        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.mainLayout)

        self.create_match_table(self.verticalLayout, header)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Les evenements
        self.new_match_info_button.clicked.connect(self.new_match)
        self.update_match_info_button.clicked.connect(self.update)
        self.save_match_info_button.clicked.connect(self.registration)
        self.delete_match_info_button.clicked.connect(self.delete_match)

    # Ajout de cette méthode pour centrer la fenêtre

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def registration(self):
        response = MatchController().add_account_info(
            self.typeMatch.currentText(),
            self.countryField.currentText(),
            self.matchDateField.date().toPyDate(),
            self.matchTimeField.text(),
            self.matchTeam1Field.text(),
            self.matchTeam2Field.text(),
            self.matchCoteField.text(),
            self.matchScoreField.text(),
            self.matchStateField.currentText()
        )
        if response == 'update_success':
            QMessageBox.about(self, 'Informations', "OK")
            self.new_match()
            self.loadDatas()
        else:
            QMessageBox.about(self, 'Erreur', response)

    def update(self):
        self.save_match_info_button.setEnabled(False)
        code = self.code.text()
        response = MatchController().update_account_info(
            self.typeMatch.currentText(),
            self.countryField.currentText(),
            self.matchDateField.date().toPyDate(),
            self.matchTimeField.text(),
            self.matchTeam1Field.text(),
            self.matchTeam2Field.text(),
            self.matchCoteField.text(),
            self.matchScoreField.text(),
            self.matchStateField.currentText(),
            code
        )
        if response == 'update_success':
            QMessageBox.about(self, 'Informations', response)
            self.new_match()
            self.loadDatas()
        else:
            QMessageBox.about(self, 'Erreur', response)

    def create_match_table(self, layout, header):
        self.table = QTableWidget()
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setObjectName("table")
        window_width = self.table.size().width()

        column_width = window_width // len(header)

        for i in range(len(header)):
            self.table.setColumnWidth(i, column_width)

        self.table.cellClicked.connect(self.myTableEvent)

        layout.addWidget(self.table)

    def loadDatas(self):
        lignes = MatchController().displayMatch()
        self.table.setRowCount(len(lignes))
        row = 0
        for ligne in lignes:
            self.table.setItem(row, 0, QTableWidgetItem(str(ligne[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(ligne[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(ligne[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(ligne[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(ligne[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(ligne[5])))
            self.table.setItem(row, 6, QTableWidgetItem(str(ligne[6])))
            self.table.setItem(row, 7, QTableWidgetItem(str(ligne[7])))
            self.table.setItem(row, 8, QTableWidgetItem(str(ligne[8])))
            self.table.setItem(row, 9, QTableWidgetItem(str(ligne[9])))
            row += 1

    def new_match(self):
        self.code.clear()
        self.typeMatch.setCurrentIndex(0),
        self.countryField.setCurrentIndex(0),
        self.matchDateField.setDate(date.today()),
        self.matchTimeField.setDisplayFormat("HH:mm"),
        self.matchTeam1Field.clear(),
        self.matchTeam2Field.clear(),
        self.matchCoteField.clear(),
        self.matchScoreField.clear(),
        self.matchStateField.setCurrentIndex(0)
        self.delete_match_info_button.setEnabled(False)
        self.update_match_info_button.setEnabled(False)
        self.save_match_info_button.setEnabled(True)

    def myTableEvent(self):
        index = self.table.currentRow()
        self.update_match_info_button.setEnabled(True)
        self.delete_match_info_button.setEnabled(True)
        self.save_match_info_button.setEnabled(True)
        row = self.match.selectMatchById(self.table.item(index, 0).text())
        self.code.setText(str(row[0]))
        self.typeMatch.setCurrentText(str(row[1]))
        self.countryField.setCurrentText(str(row[2]))
        self.matchDateField.setDate(date.fromisoformat(str(row[3])))
        self.matchTimeField.setDisplayFormat((str(row[4])))
        self.matchTeam1Field.setText(str(row[5]))
        self.matchTeam2Field.setText(str(row[6]))
        self.matchCoteField.setText(str(row[7]))
        self.matchScoreField.setText(str(row[8]))
        self.matchStateField.setCurrentText(str(row[9]))

    def delete_match(self):
        match_code = self.code.text()
        self.match.deleteMatch(match_code)
        self.loadDatas()
        self.new_match()
