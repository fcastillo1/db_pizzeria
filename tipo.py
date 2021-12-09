#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class tipo:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Tipos de vehículo")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de tipos registrados en la base de datos
        self.__config_treeview_tipo()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_tipo()

    def __config_treeview_tipo(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("id_tipo", "nom_tipo", "capacidad_tipo"))
        self.treeview.heading("id_tipo", text = "ID")
        self.treeview.heading("nom_tipo", text = "Nombre")
        self.treeview.heading("capacidad_tipo", text = "Capacidad")
        self.treeview.column("id_tipo", minwidth = 150, width = 200, stretch = False)
        self.treeview.column("nom_tipo", minwidth = 150, width = 200, stretch = False)
        self.treeview.column("capacidad_tipo", minwidth = 150, width = 200, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 600)
        # Llenado del treeview
        self.llenar_treeview_tipo()

        self.root.after(0, self.llenar_treeview_tipo)

    def __crear_botones_tipo(self):
        b1 = tk.Button(self.root, text = "Insertar tipo", bg ='snow',
            fg = 'green', command = self.__insertar_tipo)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text = "Modificar tipo", bg ='snow',
            fg = 'orange', command = self.__modificar_tipo)
        b2.place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar tipo", bg='snow',
            fg = 'red', command = self.__eliminar_tipo)
        b3.place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command = self.root.destroy,
            bg = 'red', fg = 'white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_tipo(self):
        # Se obtienen tipos ingresadas
        sql = """select id_tipo, nom_tipo, capacidad_tipo from tipo;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(sql)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:3])

            self.data = data

    def __insertar_tipo(self):
        insertar_tipo(self.db, self)

    def __eliminar_tipo(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message="¿Realmente quieres borrar el tipo?", title = "Alerta")==True:
                operation = "DELETE FROM tipo where id_tipo = %(id_tipo)s"
                self.db.run_sql(operation, {"id_tipo": self.treeview.focus()})
                self.llenar_treeview_tipo()

    def __modificar_tipo(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT id_tipo, nom_tipo, capacidad_tipo from tipo where id_tipo = %(id_tipo)s"""

                # Se consulta en la tabla tipo por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id_tipo": self.treeview.focus()})[0]
                modificar_tipo(self.db, self, mod_select)

class insertar_tipo:
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
        self.insert_datos.title("Insertar tipo")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase tipo
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        cap_lab = tk.Label(self.insert_datos, text = "Capacidad: ")
        cap_lab.place(x = 10, y = 80, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar tipo
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.capacidad = tk.Entry(self.insert_datos)
        self.capacidad.place(x = 110, y = 80, width = 150, height = 20)

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
        # Inserción de tipo
        sql = """INSERT tipo (nom_tipo, capacidad_tipo) VALUES (%(nombre)s,
        %(capacidad)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"nombre": self.nombre.get(),
        "capacidad": self.capacidad.get()})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_tipo()


class modificar_tipo:
    def __init__(self, db, padre, mod_select):
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        self.insert_datos = tk.Toplevel()
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x200')
        self.insert_datos.title("Modificar tipo")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase tipo
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 60, width = 120, height = 20)
        cap_lab = tk.Label(self.insert_datos, text = "Capacidad: ")
        cap_lab.place(x = 10, y = 100, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar tipos
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 20, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 60, width = 150, height = 20)
        self.capacidad = tk.Entry(self.insert_datos)
        self.capacidad.place(x = 110, y = 100, width = 150, height = 20)

        # Se insertan datos actuales del registro
        self.id.config(state = 'normal')
        self.id.insert(0, self.mod_select[0])
        self.id.config(state = 'disabled')
        self.nombre.insert(0, self.mod_select[1])
        self.capacidad.insert(0, self.mod_select[2])

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar el tipo
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 160, width = 80, height = 20)

    def __modificar(self):
        # Modificar registro
        opEdicion = """UPDATE tipo SET nom_tipo = %(nombre)s, capacidad_tipo = %(capacidad)s
        WHERE id_tipo = %(id)s"""

        self.db.run_sql(opEdicion, {"id": self.id.get(),"nombre": self.nombre.get(),
        "capacidad": self.capacidad.get()})

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_tipo()
