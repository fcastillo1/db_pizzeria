import mysql.connector

class DB_pizzeria:
    def __init__(self):
        self.db = None
        self.cursor = None

        # Intenta conectarse a db_pizzeria
        try:
            self.db = mysql.connector.connect(
            host="localhost",
            user="pizza",
            passwd='Password123#@!',
            database="db_pizzeria")

            self.cursor = self.db.cursor()
            print("Se ha conectado exitosamente.")

        except mysql.connector.Error as error:
            # Avisa del error
            print("No se ha conectado. Reintente.")
            print(error)
            # Termina la aplicación
            exit()
