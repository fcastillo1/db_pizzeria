#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from tkinter import messagebox

class DB_pizzeria:
    def __init__(self):
        self.db = None
        self.cursor = None

        try:
            # Intenta conectarse a db_pizzeria
            self.db = mysql.connector.connect(
            host="localhost",
            user="pizza",
            passwd='Password123#@!',
            database="db_pizzeria")

            self.cursor = self.db.cursor()
            print("Se ha conectado exitosamente a la DB.")

        except mysql.connector.Error as err:
            # Avisa del error generado
            print("No se ha conectado. Reintente.")
            print(err)
            # Termina la aplicación
            exit()

    # Función que corre una consulta select
    def run_select(self, sql):
        try:
            # Ejecuta el select
            self.cursor.execute(sql)
            # Guarda el resultado del cursor
            resultado = self.cursor.fetchall()

        except mysql.connector.Error as err:
            # Avisa del error al hacer select
            print("No se pueden obtener los datos")
            print(err)

        # Retorna resultado del select
        return resultado

    # Función que corre una consulta select para un registro específico
    def run_select_filter(self, sql, params):
        try:
            # Ejecuta consulta
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()

        except mysql.connector.Error as err:
            # Avisa del error
            print("No se pueden obtener los datos")
            print(err)

        # Retorna resultado del select
        return result

    # Corre una consulta de inserción, actualización o eliminación
    def run_sql(self, sql, params):
        try:
            # Ejecuta consulta
            self.cursor.execute(sql, params)
            texto = "Operación realizada con éxito"
            messagebox.showinfo(message = texto, title = "Aviso")
            # Cambios en la base de datos
            self.db.commit()

        except mysql.connector.Error as err:
            # Da cuenta del error
            texto_error = "No se puede realizar la operación"
            messagebox.showerror(message = texto_error, title = "Error")
            print(err)
