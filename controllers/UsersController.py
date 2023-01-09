
from PyQt5.QtCore import Qt
import time
from Helpers import Helpers
from SessionManager import SessionManager
from authentification import Login
from controllers.Controller import Controller

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


class UsersController():

    def __init__(self) -> None:
        self.TABLE_NAME = TABLE_NAME
        self.controller = Controller(PATH_NAME)
        self.COLUMNS_NAME = COLUMNS_NAME
        self.createTable()
        self.BALANCE_NULL = -1000
        self.BALANCE_INSUFFISANTE = -100
        self.help_func = Helpers()

    def get_user_datas(self):
        user_id = SessionManager.getItem('userStorage')
        if user_id and int(user_id) > 0:
            where_data = f"id = {user_id}"
            result = self.controller.select(self.TABLE_NAME, where_data)
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
                'is_admin': result[0][11],
            }
            return data

    def pay_with_balance(self, user_id, amount):
        
        if not user_id or not amount:
            return None
        user_balance = self.get_user_balance(user_id)
        if  self.help_func.is_float_in_range(user_balance) :            
            user_balance = float(user_balance)
            if user_balance >= amount:
                new_balance = user_balance - amount
                data_to_update = [('balance', new_balance)]
                where_user=f"id = {user_id}"
                result = self.controller.update(self.TABLE_NAME, data_to_update,where_user)
                
                return result
            else:
                return self.BALANCE_INSUFFISANTE
        
        return None

    def get_user_balance(self, user_id):
        """Get actual balance for user """
        if not user_id:
            return None

        where_cond = f"id = {user_id}"        
        user = self.controller.select(self.TABLE_NAME, where_cond)
        if user:
            return user[0][9]

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
