#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ciudad:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Ventana emergente que permite observar treeview de ciudad y realizar operaciones
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Ciudad")
        self.root.config(bg="light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de ciudades registradas en la base de datos
        self.__config_treeview_ciudad()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_ciudad()

    def __config_treeview_ciudad(self):
        # Creación del treeview de la ventana
        self.treeview = ttk.Treeview(self.root)
        
        # Se determinan las columnas que van a mostrarse
        self.treeview.configure(show = "headings", columns = ("id_ciudad", "nom_ciudad"))
        
        # Columnas se identifican con nombres representativos
        self.treeview.heading("id_ciudad", text = "ID")
        self.treeview.heading("nom_ciudad", text = "Nombre")
        
        # Configuraciones de tamaño de cada columna
        self.treeview.column("id_ciudad", minwidth = 150, width = 300, stretch = False)
        self.treeview.column("nom_ciudad", minwidth = 150, width = 300, stretch = False)
        # Ubicación del treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 600)
        
        # Llenado del treeview
        self.llenar_treeview_ciudad()
        self.root.after(0, self.llenar_treeview_ciudad)

    def __crear_botones_ciudad(self):
        # Botón permite abrir una ventana para insertar una ciudad
        b1 = tk.Button(self.root, text = "Insertar ciudad", bg='snow',
            fg='green', command = self.__insertar_ciudad)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        
        # Botón permite abrir una ventana para modificar una ciudad seleccionada
        b2 = tk.Button(self.root, text = "Modificar ciudad", bg='snow',
            fg='orange', command = self.__modificar_ciudad)
        b2.place(x = 150, y = 350, width = 150, height = 50)
        
        # Botón permite eliminar una ciudad
        b3 = tk.Button(self.root, text = "Eliminar ciudad", bg='snow',
            fg='red', command = self.__eliminar_ciudad)
        b3.place(x = 300, y = 350, width = 150, height = 50)
        
        # Botón para cerrar la ventana de ciudad
        b4 = tk.Button(self.root, text = "Salir", bg='red', fg='white',
            command=self.root.destroy)
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
        # Llama a clase para insertar una ciudad
        insertar_ciudad(self.db, self)

    def __eliminar_ciudad(self):
        # Se chequea que haya selección
        if(self.treeview.focus() != ""):
            # Confirmación de la eliminación
            if messagebox.askyesno(message="¿Realmente quieres borrar la ciudad?", title = "Alerta")==True:
                operation = "DELETE FROM ciudad where id_ciudad = %(id)s"
                # Si se confirma, se elimina la ciudad seleccionada
                self.db.run_sql(operation, {"id": self.treeview.focus()}, "D")
                
                # Luego de la eliminación, se actualiza el treeview
                self.llenar_treeview_ciudad()

    def __modificar_ciudad(self):
        # Se chequea que haya selección
        if(self.treeview.focus() != ""):
            # Confirmación de la modificación
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT id_ciudad, nom_ciudad from ciudad where id_ciudad = %(id)s"""

                # Se consulta en la tabla ciudad por el id del registro a modificar y se obtienen datos
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]
                # Se llama a clase para modificar ciudad con los datos obtenidos
                modificar_ciudad(self.db, self, mod_select)

class insertar_ciudad:
    def __init__(self, db, padre):
        # Ventana padre es la ventana principal de ciudad
        self.padre = padre
        self.db = db

        # Nueva ventana emergente para insertar ciudad
        self.insert_datos = tk.Toplevel()

        # Funcionalidades de la ventana
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('290x200')
        self.insert_datos.title("Insertar ciudad")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Definición de etiquetas
        # Solo permite ingreso del nombre, id es autoincremental en bd
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 70, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar nombre de ciudad nueva
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 70, width = 150, height = 20)

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
        btn_ok.place(x=50, y =150, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x=160, y =150, width = 80, height = 20)

    def __insertar(self):
        # Consulta para la inserción de ciudad
        sql = """insert ciudad (nom_ciudad) values (%(nombre)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"nombre": self.nombre.get()}, "I")
        
        # Se destruye la ventana
        self.insert_datos.destroy()
        
        # Actualización del treeview en la ventana principal
        self.padre.llenar_treeview_ciudad()

class modificar_ciudad:
    def __init__(self, db, padre, mod_select):
        # Padre es ventana principal de ciudad
        self.padre = padre
        self.db = db
        # Recibe información del registro a modificar
        self.mod_select = mod_select
        self.insert_datos = tk.Toplevel()
        self.insert_datos.attributes("-topmost", 1)
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('290x200')
        self.insert_datos.title("Modificar ciudad")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Definición de entradas de texto para la clase ciudad
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 45, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 90, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar ciudades
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 45, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 90, width = 150, height = 20)

        # Se insertan datos actuales del registro
        self.id.config(state = 'normal')
        self.id.insert(0, self.mod_select[0])
        self.id.config(state = 'disabled')
        self.nombre.insert(0, self.mod_select[1])

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar la ciudad
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 50, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x = 160, y = 160, width = 80, height = 20)

    def __modificar(self):
        # Modificar registro
        opEdicion = """update ciudad set nom_ciudad = %(nombre)s
        where id_ciudad = %(id)s"""

        self.db.run_sql(opEdicion, {"id": self.id.get(),"nombre": self.nombre.get()}, "U")

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_ciudad()
