import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit, \
    QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QDateTimeEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog
from SessionManager import SessionManager
from controllers.BetsController import BetsController
from controllers.UsersController import UsersController

class BetsView(QDialog):
    def __init__(self, parent):
        super(BetsView, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Payments - JetBrainsBet")
        self.setMinimumSize(900, 600)
        self.mainLayout = QHBoxLayout()
        self.bets_controller = BetsController()
        self.user_contr = UsersController()
        self.center()
        self.ui()
        self.listTableWidget()

    def ui(self):
        self.groupBox = QGroupBox()
        self.groupBox.setMinimumSize(300, 600)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.horizontalLayout = QHBoxLayout()

        # enregistrer payment
        self.lbl_title_box = QLabel("Payment:")
        self.lbl_title_box.setStyleSheet("text-align: center;")
        # id pariage
        self.bet_id_lbl = QLabel("Id pariage: ")
        self.bet_id_Field = QLineEdit()
        self.bet_id_Field.setEnabled(False)
        
        # amount
        self.amount_lbl = QLabel("Montant: ")
        self.amount_Field = QLineEdit()
        self.amount_Field.setPlaceholderText("Montant")
        self.amount_Field.setValidator(QDoubleValidator(25, 100000000, 2, self))
        self.amount_Field.setEnabled(False)
        # dateTime
        self.date_time_lbl = QLabel("Date payment: ")
        self.date_time_QDTM = QDateTimeEdit()
        self.date_time_QDTM.setDisplayFormat("yyyy/MM/dd HH:mm:ss")
        self.date_time_QDTM.setCalendarPopup(True)
        self.date_time_QDTM.setEnabled(False)
        #
        #
        self.errorMsgLbl = QLabel("")
        self.errorMsgLbl.setVisible(False)
        self.errorMsgLbl.setStyleSheet("color: red; margin: 5px 0px")

        self.updateBEtBtn = QPushButton('Modifier', self)
        self.updateBEtBtn.setEnabled(False)
        # add to layout
        self.verticalLayout.addWidget(
            self.lbl_title_box, alignment=Qt.AlignCenter)
        self.verticalLayout.addWidget(self.bet_id_Field)
        self.verticalLayout.addWidget(self.amount_Field)
        self.verticalLayout.addWidget(self.date_time_QDTM)
        self.verticalLayout.addWidget(self.updateBEtBtn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)
        user= self.user_contr.get_user_datas()
        # print(f"US: {user}")
        # if user and user['is_admin'] == 1:
        #     # show 
        #     self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        self.mainLayout.setStretch(500, 500)
        self.setLayout(self.mainLayout)
        self.show()

        # ******************************************************** #
        self.updateBEtBtn.clicked.connect(
            lambda: self.manageUpdateBet())

    def center(self):
        # Ajout de cette méthode pour centrer la fenêtre
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def listTableWidget(self):

        self.table_WDG = QTableWidget()
        self.table_WDG.setStyleSheet("background-color: #667373;color: white")
        # self.table_WDG.cellClicked.connect(lambda: self.eventOnTable())
        header = ("Utilisateur", "Match", "Score prevue","cote","Montant", "Date")

        self.table_WDG.setColumnCount(len(header))
        self.table_WDG.setHorizontalHeaderLabels(header)
        # add button
        self.printBtn = QPushButton("Imprimer")
        self.printBtn.clicked.connect(lambda:self.printBetCallback())
        
        # add layout
        self.mainLayout.addWidget(self.printBtn,)
        self.mainLayout.addWidget(self.table_WDG,)

    def load_datas(self, list_datas):
        """
        cette fonction va remplir le tableau avec des elements
        - Arguments:
            - list_datas : `list[dict]`
        - Return `NoneType`
        """
        self.table_WDG.setRowCount(len(list_datas))

        row = 0
        for i in list_datas:
            # ("Utilisateur", "Match", "Score prevue","cote","Montant", "Date")
            self.table_WDG.setItem(
                row, 0, QTableWidgetItem(str(f"{i['user']}")))
            self.table_WDG.setItem(
                row, 1, QTableWidgetItem(str(f"{i['match']}")))
            self.table_WDG.setItem(
                row, 2, QTableWidgetItem(str(f"{i['score_prevu']}")))
            self.table_WDG.setItem(
                row, 3, QTableWidgetItem(str(f"{i['cote']}")))
            self.table_WDG.setItem(
                row, 4, QTableWidgetItem(str(f"{i['montant_depense']}")))
            self.table_WDG.setItem(
                row, 5, QTableWidgetItem(str(f"{i['date']}")))
            row += 1

    def refresh_datas(self):
        """
        Cette fonction permet de mettre a jour les données du pari
        """
        # WITH USER ID
        FOR_USER_ID = 1
        get_datas = self.bets_controller.get_bets(FOR_USER_ID)
        if get_datas:
            self.load_datas(get_datas)
        else:
            # self.empty_data()
            print("no data found")

    
    def eventOnTable(self):

        self.updateBEtBtn.setEnabled(True)
        self.amount_Field.setEnabled(True)
        # open score

        index = self.table_WDG.currentRow()
        id = self.table_WDG.item(index, 0).text()
        if id:
            row = self.bets_controller.get_bet_by_id(id)
            if row:
                # fill form
                self.bet_id_Field.setText(str(row['id']))
                self.amount_Field.setText(str(row['amount']))
                # self.dateTimeMatch_Field.setDateTime(datetime.fromisoformat(str(row['date'])))
                
            else:
                print("No data found")
        else:
            print("No id selected")


    def manageUpdateBet(self):
        """
        toute la logique de traitment pour enregistrer un payment
        """
        amount = self.amount_Field.text()
        self.errorMsgLbl.setVisible(False)

        isValid = self._isPaymentFielsValid(amount)

        if isValid:
            amount = amount.replace(",", ".")
            if float(amount) and float(amount) > 0 and float(amount) < 100000000:
                # Preparations pour update
                pay_data = [
                    ("amount", amount),
                ]
                whre_query = f" id = '{id}'"
                # Envoi des données de l'utilisateur au contrôleur pour modification
                result = self.bets_controller.updatePaymentAmount(pay_data, whre_query)
                # nettoyages
                self.emptyFields()
                
            else:
                self.errorMsgLbl.setText(
                    "Veuillez le montant")
                self.errorMsgLbl.setVisible(True)

        else:
            self.errorMsgLbl.setText("Veuillez remplir tous les champs SVP!")
            self.errorMsgLbl.setVisible(True)

    def _isPaymentFielsValid(self, amount):

        if amount != "":
            return True

        return False

    def emptyFields(self):
        # 
        self.errorMsgLbl.setText("")
        self.errorMsgLbl.setVisible(False)
        self.updateBEtBtn.setEnabled(False)
        # 
        self.amount_Field.setEnabled(False)



    def printBetCallback(self):
        printer = QPrinter()
        
        app = QApplication.instance()
        active_window = app.activeWindow()
        if active_window:
            # Création de la boîte de dialogue d'impression et affichage
            printDialog = QPrintDialog(printer, app.activeWindow())
            printDialog.open()

            # Impression si l'utilisateur clique sur "Imprimer"
            if printDialog.result() == QPrintDialog.Accepted:
                app.activeWindow().render(printer)
                printer.print()

        else:
            QMessageBox.warning(
                    None, "Error", "On ne peux pas lance la fenetre d'impression pour l'instant", QMessageBox.Ok)