#!/usr/bin/env python
# -*- coding: utf-8 -*-

# se importa el conector para poder que pueda funcionar la app con la base de datos
import mysql.connector
from mysql.connector import errorcode
# se importa tkinder y una libreria necesaria
from tkinter import messagebox

# se da comienzo a la clase de la base de datos
class DB_pizzeria:
    def __init__(self):
       # Se actualiza atributo con la database y tambien del cursor
        self.db = None
        self.cursor = None
        # se realiza una excepcion
        try:
            # se intenta conectarse a db_pizzeria ingresando el datos principales
            self.db = mysql.connector.connect(
            host="localhost",
            user="pizza",
            passwd='Password123#@!',
            database="db_pizzeria")
            # se genera el cursor que permitira la conexion con la base de datos
            self.cursor = self.db.cursor()
            # Se imprime un mensaje que la base de datos se conecto de manera exitosa
            print("Se ha conectado exitosamente a la DB.")

        # Si la excepcion no se cumple se generara un error de conexion
        except mysql.connector.Error as err:
            # Avisa del error generado
            print("No se ha conectado. Reintente.")
            print(err)
            # Termina la aplicación
            exit()

    # Función que corre una consulta select
    def run_select(self, sql):
        # realiza la excepcion para obtener los datos (tablas) de la base de datos
        try:
            # Ejecuta el select
            self.cursor.execute(sql)
            # Guarda el resultado del cursor por lo tanto los datos son obtenidos y almacenados
            resultado = self.cursor.fetchall()

        # si la excepcion no se cumple arrojara error
        except mysql.connector.Error as err:
            # Avisa del error al hacer select y los datos no se pueden obtener
            print("No se pueden obtener los datos")
            print(err)
        # Retorna resultado del select
        return resultado

    # Función que corre una consulta select para un registro específico
    def run_select_filter(self, sql, params):
        # realiza la excepcion para obtener los datos (tablas) de la base de datos
        try:
            # Ejecuta consulta
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()

        # si la excepcion no se cumple arrojara error
        except mysql.connector.Error as err:
            # Avisa del error
            print("No se pueden obtener los datos")
            print(err)
        # Retorna resultado del select
        return result

    # Corre una consulta de inserción, actualización o eliminación
    def run_sql(self, sql, params, operacion):
        # permite poder validar que se este ejecutando bien el sql
        if validar_run_sql(params) is True:
            try:
                # Ejecuta consulta
                self.cursor.execute(sql, params)
                # se imprime un mensaje donde la operacion se realiza con exito
                texto = "Operación realizada con éxito"
                messagebox.showinfo(message = texto, title = "Aviso")
                # Cambios en la base de datos
                self.db.commit()

            # si existen excepciones y errores de conexion con mysql se imprimen mensajes
            except mysql.connector.Error as err:
                # Da cuenta del error imprimiendo el mensaje y mostrandolo en una ventana con ese mensaje
                if operacion == "I":
                    texto_error = "No se puede realizar la inserción. "
                # Da cuenta de un error de actulizacion en la operacion y se muestra en una ventana
                elif operacion == "U":
                    texto_error = "No se puede realizar la actualización. "
                # Da cuenta de un error de eliminacion y se muestra en una ventana
                elif operacion == "D":
                    texto_error = "No se puede realizar la eliminación. "
                # si exite el error 1451 quiere decir que el registro no se elimina porque esta en otra tabla
                if err.errno == 1451:
                    texto_error = texto_error + "El registro se referencia en otra tabla."
                # si existe un error 1366 quiere decir que hay un error en el tipo de dato
                elif err.errno == 1366:
                    texto_error = texto_error + "Error en valor(es) numéricos enteros."
                # si existe un error 1062 indicara que ya existe un registro con ese ID o rut segun sea el caso
                elif err.errno == 1062:
                    texto_error = texto_error + "Ya hay un registro con el mismo id/rut."
                # esta es la ventana que mostrara el error
                messagebox.showerror(message = texto_error, title = "Error")
                print(err)
        # si el error es porque falta un campo por llenar se imprime ese mensaje
        else:
            texto_error = "Debe llenar todos los campos"
            messagebox.showerror(message = texto_error, title = "Error")

# se crea una funcion que permita validar el funcionamiento del mysql
def validar_run_sql(params):
    # se genera una bandera
    bandera = 0;

    for key in params:
        # si la patente es null la bandera sumara 1
        if params[key] == '':
            if (key != "patente"):
                # esto se hace por el caso de las bicicleta que no cuentan con patente
                bandera += 1;
    # si la bandera es igual a 0 se retorna un true
    if bandera == 0:
        return True
