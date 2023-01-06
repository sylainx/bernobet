import sqlite3
from PyQt5.QtWidgets import QMessageBox


class Controller:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_table(self, table_name, columns):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if self.is_table_exist(table_name):
                return  # La table est déja là, on ne fait rien

            # Générer la commande SQL pour créer la table
            column_defs = ", ".join([f"{name} {datatype}" for name, datatype in columns])
            sql = f"CREATE TABLE {table_name} ({column_defs})"

            # Exécuter la commande SQL
            cursor.execute(sql)
            conn.commit()

            # Vérifier si la table a été créée
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            return cursor.fetchone() is not None  # La table est créée si fetchone() retourne un résultat

    def select(self, table_name, where=None, order_by=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if not self.is_table_exist(table_name):
                return  # La table n'est pas presente, on ne fait rien

            # Générer la commande SQL pour sélectionner des enregistrements
            sql = f"SELECT * FROM {table_name}"
            if where:
                sql += f" WHERE {where}"
            if order_by:
                sql += f" ORDER BY {order_by}"
            # Exécuter la commande SQL et récupérer les résultats
            cursor.execute(sql)
            return cursor.fetchall()

    def select_by_id(self, table_name, id_):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if not self.is_table_exist(table_name):
                return  # La table n'est pas presente, on ne fait rien

            # Générer la commande SQL pour sélectionner l'enregistrement avec l'ID spécifié
            sql = f"SELECT * FROM {table_name} WHERE id = ?"
            cursor.execute(sql, (id_,))
            return cursor.fetchone()

    def insert(self, table_name, values):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if not self.is_table_exist(table_name):
                return # La table n'est pas presente, on ne fait rien

            # Générer la commande SQL pour insérer un enregistrement
            column_names = ", ".join([name for name, _ in values])
            placeholders = ", ".join(["?" for _, _ in values])
            sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            print(f"SQL: {sql}")
            # Exécuter la commande SQL avec les valeurs
        cursor.execute(sql, [value for _, value in values])
        conn.commit()

        # Get the ID of the inserted row
        inserted_id = cursor.lastrowid
        # Execute a SELECT statement to retrieve the inserted row
        cursor.execute(f"SELECT * FROM {table_name} WHERE {values[0][0]} = {inserted_id}")
        conn.commit()

        # Fetch the inserted row
        inserted_row = cursor.fetchone()
        # Check the inserted row
        # if inserted_row:
            # Data has been inserted successfully
        return inserted_id
        # else:
        #     QMessageBox.warning(
        #         None, "Error", "Insertion - Quelque chose ne va pas", QMessageBox.Ok)
        #     return False

    def update(self, table_name, values, where):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Générer la commande SQL pour mettre à jour un enregistrement
            updates = ", ".join([f"{name} = ?" for name, _ in values])
            sql = f"UPDATE {table_name} SET {updates} WHERE {where}"
            print(f"UPD: {values}")
            # Exécuter la commande SQL avec les valeurs
            cursor.execute(sql, [value for _, value in values])
            conn.commit()
            # Vérifier si la mise à jour a réussi
            cursor.execute(f"SELECT * FROM {table_name} WHERE {where}")
            updated_row = cursor.fetchone()
            if updated_row:
                return True  # La mise à jour a réussi
            else:
                QMessageBox.warning(
                    None, "Error", "Quelque chose ne va pas", QMessageBox.Ok)
                return False

    def table_structure(self, table_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if not self.is_table_exist(table_name):
                return  # La table n'est pas presente, on ne fait rien

            # Générer la commande SQL pour récupérer la structure de la table
            sql = f"PRAGMA table_info('{table_name}')"
            cursor.execute(sql)
            return cursor.fetchall()

    def drop(self, table_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if not self.is_table_exist(table_name):
                return  # La table n'existe pas, on ne fait rien

            # Générer la commande SQL pour supprimer la table
            sql = f"DROP TABLE {table_name}"
            cursor.execute(sql)
            conn.commit()

            # Vérifier si la table a été supprimée
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            return cursor.fetchone() is None  # La table a été supprimée si fetchone() retourne None

    def is_table_exist(self, table_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            return cursor.fetchone() is not None  # La table existe si fetchone() retourne un résultat


