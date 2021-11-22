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

    def run_select(self, sql):#Función que corre un select
        #sql se un string con un select en lenguaje sql
        try:
            self.cursor.execute(sql)#ejecuta
            result = self.cursor.fetchall() #Guarda el resultado en result
        except mysql.connector.Error as err:#Si no resulta, avisa
            print("No se pueden obtener los datos")
            print(err)
        return result#Retorna result

    def run_select_filter(self, sql, params):
        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("No se pueden obtener los datos")
            print(err)
        return result

    def run_sql(self, sql, params):
        try:
            self.cursor.execute(sql, params)
            self.db.commit()
        except mysql.connector.Error as err:
            print("No se puede realizar la sql")
            print(err)

