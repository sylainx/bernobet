import sqlite3


class Controller:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        # Vérifier si la table existe déjà
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if self.cursor.fetchone():
            return  # La table existe déjà, on ne fait rien

        # Générer la commande SQL pour créer la table
        column_defs = ", ".join([f"{name} {datatype}" for name, datatype in columns])
        sql = f"CREATE TABLE {table_name} ({column_defs})"

        # Exécuter la commande SQL
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name, values):
        try:
            # Générer la commande SQL pour insérer un enregistrement
            column_names = ", ".join([name for name, _ in values])
            placeholders = ", ".join(["?" for _, _ in values])
            sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            # Exécuter la commande SQL avec les valeurs
            self.cursor.execute(sql, [value for _, value in values])
            self.conn.commit()
        except :
            raise Exception(f"Erreur ")

    def select(self, table_name, where=None, order_by=None):
        # Générer la commande SQL pour sélectionner des enregistrements
        sql = f"SELECT * FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY {order_by}"

        # Exécuter la commande SQL et récupérer les résultats
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, table_name, values, where):
        # Générer la commande SQL pour mettre à jour un enregistrement
        updates = ", ".join([f"{name} = ?" for name, _ in values])
        sql = f"UPDATE {table_name} SET {updates} WHERE {where}"

        # Exécuter la commande SQL avec les valeurs
        self.cursor.execute(sql, [value for _, value in values])
        self.conn.commit()

    def delete(self, table_name, where):
        # Générer la commande SQL pour supprimer un enregistrement
        sql = f"DELETE FROM {table_name} WHERE {where}"
        # Exécuter la commande SQL
        self.cursor.execute(sql)
        self.conn.commit()


    