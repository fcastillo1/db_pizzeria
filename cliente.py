#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class cliente:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Clientes")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de clientes registrados en la base de datos
        self.__config_treeview_cliente()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_cliente()

    def __config_treeview_cliente(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("rut_cli", "nom_clie", "ape_clie",
            "tel_clie", "dir_clie"))
        self.treeview.heading("rut_cli", text = "Rut")
        self.treeview.heading("nom_clie", text = "Nombre")
        self.treeview.heading("ape_clie", text = "Apellido")
        self.treeview.heading("tel_clie", text = "Teléfono")
        self.treeview.heading("dir_clie", text = "Dirección")
        self.treeview.column("rut_cli", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("ape_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("tel_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("dir_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # Llenado del treeview
        self.llenar_treeview_cliente()

        self.root.after(0, self.llenar_treeview_cliente)

    def __crear_botones_cliente(self):
        b1 = tk.Button(self.root, text = "Insertar cliente",
            command = self.__insertar_cliente)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text = "Modificar cliente")
        b2.place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar cliente")
        b3.place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy)
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_cliente(self):
        # Se obtienen clientes ingresados
        sql = """select rut_cli, nom_clie, ape_clie, tel_clie, dir_clie
        from cliente;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(sql)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:5])

            self.data = data

    def __insertar_cliente(self):
        insertar_cliente(self.db, self)
    #
    # def __modificar_jugador(self):
    #     if(self.treeview.focus() != ""):
    #         sql = """select id_jugador, nom_jugador, ape_jugador, equipo.nom_equipo
    #         from jugador join equipo on jugador.id_equipo = equipo.id_equipo
    #         where id_jugador = %(id_jugador)s"""
    #
    #         row_data = self.db.run_select_filter(sql, {"id_jugador": self.treeview.focus()})[0]
    #         modificar_jugador(self.db, self, row_data)

    # def __eliminar_jugador(self):
    #     sql = "delete from jugador where id_jugador = %(id_jugador)s"
    #     self.db.run_sql(sql, {"id_jugador": self.treeview.focus()})
    #     self.llenar_treeview_jugador()

class insertar_cliente:
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
        self.insert_datos.title("Insertar cliente")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Definición de entradas de texto para la clase cliente
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)
        dir_lab = tk.Label(self.insert_datos, text = "Dirección: ")
        dir_lab.place(x = 10, y = 130, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar clientes
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)
        self.direccion = tk.Entry(self.insert_datos)
        self.direccion.place(x = 110, y = 130, width = 150, height = 20)

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar)
        btn_ok.place(x=100, y =160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy)
        btn_cancel.place(x=210, y =160, width = 80, height = 20)

    def __insertar(self): #Insercion en la base de datos.
        # Inserción de cliente
        sql = """insert cliente (rut_cli, nom_clie, ape_clie, tel_clie, dir_clie)
                values (%(rut)s, %(nombre)s, %(apellido)s, %(telefono)s, %(direccion)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get()})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_cliente()

# class modificar_jugador:
#     def __init__(self, db, padre, row_data):
#         self.padre = padre
#         self.db = db
#         self.row_data = row_data
#         self.insert_datos = tk.Toplevel()
#         self.config_window()
#         self.config_label()
#         self.config_entry()
#         self.config_button()
#
#     def config_window(self): #Settings
#         self.insert_datos.geometry('200x120')
#         self.insert_datos.title("Modificar jugador")
#         self.insert_datos.resizable(width=0, height=0)
#
#     def config_label(self): #Labels
#         tk.Label(self.insert_datos, text = "Nombre: ").place(x = 10, y = 10, width = 80, height = 20)
#         tk.Label(self.insert_datos, text = "Apellido: ").place(x = 10, y = 40, width = 80, height = 20)
#         tk.Label(self.insert_datos, text = "Equipo: ").place(x = 10, y = 70, width = 80, height = 20)
#
#     def config_entry(self):#Se configuran los inputs
#         self.entry_nombre = tk.Entry(self.insert_datos)
#         self.entry_nombre.place(x = 110, y = 10, width = 80, height = 20)
#         self.entry_apellido = tk.Entry(self.insert_datos)
#         self.entry_apellido.place(x = 110, y = 40, width = 80, height = 20)
#         self.combo = ttk.Combobox(self.insert_datos)
#         self.combo.place(x = 110, y = 70, width = 80, height= 20)
#         self.combo["values"], self.ids = self.fill_combo()
#         self.entry_nombre.insert(0, self.row_data[1])
#         self.entry_apellido.insert(0, self.row_data[2])
#         self.combo.insert(0, self.row_data[3])
#
#     def config_button(self): #Botón aceptar, llama a la función modificar cuando es clickeado.
#         tk.Button(self.insert_datos, text = "Aceptar",
#             command = self.modificar).place(x=0, y =100, width = 200, height = 20)
#
#     def modificar(self): #Insercion en la base de datos.
#         sql = """update jugador set nom_jugador = %(nom_jugador)s, ape_jugador = %(ape_jugador)s,
#             id_equipo = %(id_equipo)s where id_jugador = %(id_jugador)s"""
#         self.db.run_sql(sql, {"nom_jugador": self.entry_nombre.get(),
#             "ape_jugador": self.entry_apellido.get(), "id_equipo": self.ids[self.combo.current()],
#                 "id_jugador": int(self.row_data[0])})
#         self.insert_datos.destroy()
#         self.padre.llenar_treeview_jugador()
#

