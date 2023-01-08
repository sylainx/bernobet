
from PyQt5.QtCore import Qt
import time
from SessionManager import SessionManager
from authentification import Login
from controllers.Controller import Controller
from controllers.UsersController import UsersController

TABLE_NAME = "payments_test"
PATH_NAME = "./db/database.db"
COLUMNS_NAME = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "bet_id": "INT",
    "amount": "DOUBLE",
    "date": "DATETIME",
}


class PaymentsController():

    def __init__(self) -> None:
        self.TABLE_NAME = TABLE_NAME
        self.controller = Controller(PATH_NAME)
        self.COLUMNS_NAME = COLUMNS_NAME
        self.createTable()
        self.user_contr = UsersController()
        
    def get_available_payments(self):
        """
        Lister tous les payments disponibles
        """
        payment_datas = self.controller.select(self.TABLE_NAME)
        if payment_datas:
            list_of_payments = list()
            for m in payment_datas:
                dict_payment = {
                    'id': m[0],
                    "bet_id": m[1],
                    'amount': m[2],
                    'date': m[3],

                }
                list_of_payments.append(dict_payment)
            return list_of_payments

        return None

    def get_payment_by_id(self, payment_id):
        """
            Pour afficher un payment par son id
        """

        if not payment_id:
            return None

        whre_id = f"id ='{payment_id}'"

        payments_datas = self.controller.select(self.TABLE_NAME, whre_id)
        if payments_datas:
            dict_payment = {
                'id': payments_datas[0][0],
                "bet_id": payments_datas[0][1],
                'amount': payments_datas[0][2],
                'date': payments_datas[0][3],
            }
            return dict_payment
        return None

    def createTable(self):
        """
        pour creer la table en question
        si elle est deja presente, elle ne fait rien
        """
        result = self.controller.create_table(
            table_name=self.TABLE_NAME, columns=self.COLUMNS_NAME.items())

        if not result:
            print(f"Table : ```{self.TABLE_NAME}``` already exist")
        else:
            print(f"Table : ```{self.TABLE_NAME}``` vient d'etre créée")

    def dropTable(self):
        """
        use it only for drop table and delete all fields
        """
        self.controller.drop(self.TABLE_NAME)
        print(f"Table ```{self.TABLE_NAME.upper()}``` is dropped")

    def updatePaymentAmount(self, pay_data, whre_query):

        result = self.controller.update(
            self.TABLE_NAME, pay_data, whre_query)

        return result
