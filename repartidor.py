#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class repartidor:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Repartidores")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de repartidoress registrados en la base de datos
        self.__config_treeview_repartidor()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_repartidor()

    def __config_treeview_repartidor(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("rut_rep", "nom_rep", "ape_rep", "tel_rep"))
        self.treeview.heading("rut_rep", text = "Rut")
        self.treeview.heading("nom_rep", text = "Nombre")
        self.treeview.heading("ape_rep", text = "Apellido")
        self.treeview.heading("tel_rep", text = "Teléfono")
        self.treeview.column("rut_rep", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_rep", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("ape_rep", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("tel_rep", minwidth = 150, width = 100, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # Llenado del treeview
        self.llenar_treeview_repartidor()
        self.root.after(0, self.llenar_treeview_repartidor)

    def __crear_botones_repartidor(self):
        b1 = tk.Button(self.root, text = "Insertar repartidor", bg ='snow',
            fg = 'green', command = self.__insertar_repartidor)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text = "Modificar repartidor", bg ='snow',
            fg = 'orange', command = self.__modificar_repartidor)
        b2.place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar repartidor", bg = 'snow',
            fg = 'red', command = self.__eliminar_repartidor)
        b3.place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command = self.root.destroy,
            bg = 'red', fg = 'white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_repartidor(self):
        # Se obtienen repartidores ingresados
        sql = """SELECT rut_rep, nom_rep, ape_rep, tel_rep FROM repartidor;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(sql)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:4])

            self.data = data

    def __insertar_repartidor(self):
        insertar_repartidor(self.db, self)

    def __eliminar_repartidor(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message = "¿Realmente quieres borrar el repartidor?", title = "Alerta")==True:
                operation = "DELETE FROM repartidor WHERE rut_rep = %(rut_rep)s"
                self.db.run_sql(operation, {"rut_rep": self.treeview.focus()})
                self.llenar_treeview_repartidor()

    def __modificar_repartidor(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message = "¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT rut_rep, nom_rep, ape_rep, tel_rep FROM repartidor WHERE rut_rep = %(rut_rep)s"""

                # Se consulta en la tabla repartidor por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"rut_rep": self.treeview.focus()})[0]
                modificar_repartidor(self.db, self, mod_select)

class insertar_repartidor:
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
        self.insert_datos.title("Insertar repartidor")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase repartidor
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar repartidor
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg = 'green', fg = 'white')
        btn_ok.place(x=100, y =160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x=210, y =160, width = 80, height = 20)

    def __insertar(self):
        # Inserción de repartidor
        sql = """insert repartidor (rut_rep, nom_rep, ape_rep, tel_rep) values
                (%(rut)s, %(nombre)s, %(apellido)s, %(telefono)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get()})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_repartidor()

class modificar_repartidor:
    def __init__(self, db, padre, mod_select):
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        self.insert_datos = tk.Toplevel()

        # Funcionalidades
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x250')
        self.insert_datos.title("Modificar repartidor")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase repartidor
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar repartidoress
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)

        # Se insertan datos actuales del registro
        self.rut_viejo = self.mod_select[0]
        self.rut.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])
        self.apellido.insert(0, self.mod_select[2])
        self.telefono.insert(0, self.mod_select[3])

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar el repartidor
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 200, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 200, width = 80, height = 20)

    def __modificar(self):
        # Modificar registro
        opEdicion = """UPDATE repartidor SET rut_rep = %(rut)s, nom_rep = %(nombre)s,
        ape_rep = %(apellido)s, tel_rep = %(telefono)s WHERE rut_rep = %(rut_viejo)s"""

        self.db.run_sql(opEdicion, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "rut_viejo": self.rut_viejo})

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_repartidor()
