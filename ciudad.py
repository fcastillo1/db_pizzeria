#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class ciudad:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Clientes")
        self.root.config(bg="light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de clientes registrados en la base de datos
        self.__config_treeview_ciudad()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_ciudad()

    def __config_treeview_ciudad(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("id_ciudad", "nom_ciudad"))
        self.treeview.heading("id_ciudad", text = "ID")
        self.treeview.heading("nom_ciudad", text = "Nombre")
        self.treeview.column("id_ciudad", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_ciudad", minwidth = 150, width = 100, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # Llenado del treeview
        self.llenar_treeview_ciudad()

        self.root.after(0, self.llenar_treeview_ciudad)

    def __crear_botones_ciudad(self):
        b1 = tk.Button(self.root, text = "Insertar ciudad", bg='snow',
            fg='green', command = self.__insertar_ciudad)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text = "Modificar ciudad", bg='snow',
            fg='orange')
        b2.place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar ciudad", bg='snow', fg='red')
        b3.place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy, bg='red', fg='white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_ciudad(self):
        # Se obtienen ciudades ingresadas
        sql = """select id_ciudad, nom_ciudad from ciudad;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(sql)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:2])

            self.data = data

    def __insertar_ciudad(self):
        insertar_ciudad(self.db, self)

class insertar_ciudad:
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        # Ventana emergente
        self.insert_datos = tk.Toplevel()

        # Funcionalidades
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x200')
        self.insert_datos.title("Insertar ciudad")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Definición de entradas de texto para la clase cliente
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "NOMBRE: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar clientes
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
        btn_ok.place(x=100, y =160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x=210, y =160, width = 80, height = 20)

    def __insertar(self): #Insercion en la base de datos.
        # Inserción de ciudad
        sql = """insert ciudad (id_ciudad, nom_ciudad) values (%(id)s, %(nombre)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"id": self.rut.get(),"nombre": self.nombre.get()})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_ciudad()
