#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Se define la clase de ciudad(tabla)
class ciudad:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea un que e sun aventana superior a la principal
        self.root = tk.Toplevel()
        # se define el tamaño de la ventana
        self.root.geometry('600x400')
        # se define el titulo que tendra la ventana
        self.root.title("Ciudad")
        # mediante esta opcion de configuracion la ventana tendra un color de fondo
        self.root.config(bg="light cyan")
        # Esta opcion permite cambiar el tamano de la venta segun las necesidades del usuario
        self.root.resizable(width = 0, height = 0)

        # Se permite la creacion de una ventana nueva
        self.root.transient(root)

        # Visualización de ciudades registradas en la base de datos
        self.__config_treeview_ciudad()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_ciudad()

    # Esta funcion permitira poder hacer un treeview que solicitara los datos al user
    def __config_treeview_ciudad(self):
        self.treeview = ttk.Treeview(self.root)
        # en este caso solo existira para ingresar el id de la ciduad y su nombre
        self.treeview.configure(show = "headings", columns = ("id_ciudad", "nom_ciudad"))
        self.treeview.heading("id_ciudad", text = "ID")
        self.treeview.heading("nom_ciudad", text = "Nombre")
        # estas opciones permiten localizar la posicion donde estara el treeview
        self.treeview.column("id_ciudad", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_ciudad", minwidth = 150, width = 100, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # esto permite que sea llenado el treeview
        self.llenar_treeview_ciudad()
        self.root.after(0, self.llenar_treeview_ciudad)

    # Esta funcion permite la creacion de los botones
    def __crear_botones_ciudad(self):
        # este boton permitira que se pueda insertar la ciudad y el formato de este
        btn_insert = tk.Button(self.root, text = "Insertar ciudad", bg='snow',
            fg='green', command = self.__insertar_ciudad)
        # aqui se describe la posicion del boton
        btn_insert.place(x = 0, y = 350, width = 150, height = 50)
        # este boton permitira que se pueda modificar la ciudad y el formato de este
        btn_modificar = tk.Button(self.root, text = "Modificar ciudad", bg='snow',
            fg='orange', command = self.__modificar_ciudad)
        # aqui se describe la posicion del boton
        btn_modificar.place(x = 150, y = 350, width = 150, height = 50)
        # este boton permitira que se pueda eliminar la ciudad y el formato de este
        btn_delete = tk.Button(self.root, text = "Eliminar ciudad", bg='snow',
            fg='red', command = self.__eliminar_ciudad)
        # aqui se describe la posicion del boton
        btn_delete.place(x = 300, y = 350, width = 150, height = 50)
        # este boton permitira que se pueda salir la ciudad y el formato de este
        btn_exit = tk.Button(self.root, text = "Salir", bg='red', fg='white',
            command=self.root.destroy)
        # aqui se describe la posicion del boton
        btn_exit.place(x = 450, y = 350, width = 150, height = 50)

    # esta funcion permite que el treeview se llene
    def llenar_treeview_ciudad(self):
        # Se obtienen ciudades ingresadas
        sql = """select id_ciudad, nom_ciudad from ciudad;"""

        # Guarda la informacion obtenida tras la consulta
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

    # esta funcion llama a la otra que permite que se inserte la ciudad
    def __insertar_ciudad(self):
        insertar_ciudad(self.db, self)

    # esta funcion permite que la ciudad se eliminada
    def __eliminar_ciudad(self):
        if(self.treeview.focus() != ""):
            # se imprime el mensaje box para advertir que se borra el mensaje
            if messagebox.askyesno(message="¿Realmente quieres borrar la ciudad?", title = "Alerta")==True:
                # se indica cual sera la operacion a realizar
                opEliminar = "DELETE FROM ciudad where id_ciudad = %(id)s"
                # se elimina desde la base de datos por el id
                self.db.run_sql(opEliminar, {"id": self.treeview.focus()})
                self.llenar_treeview_ciudad()

    # esta funcion permite que se modifique la ciudad
    def __modificar_ciudad(self):
        if(self.treeview.focus() != ""):
            # se imprime el mensaje box para advertir que se modifica el mensaje
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                # se indica cual sera la operacion a realizar en este caso modificar
                opModificar = """SELECT id_ciudad, nom_ciudad from ciudad where id_ciudad = %(id)s"""
                # Se consulta en la tabla ciudad por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]
                modificar_ciudad(self.db, self, mod_select)

# Se genera una clase que permite que la ciudad sea insertada
class insertar_ciudad:
    def __init__(self, db, padre):
        # se definen los self de la base de datos y del padre
        self.padre = padre
        self.db = db

        # Se genera una ventana emergente
        self.insert_datos = tk.Toplevel()

        # Se procede a llamar a cada una de las funciones necesarias
        self.__configuracion_ventana()
        self.__configuracion_label()
        self.__configuracion_text_entrada()
        self.__configuracion_boton()

    # esta funcion permite la configuracion de la ventana
    def __configuracion_ventana(self):
        # Se define el tamano de la ventana
        self.insert_datos.geometry('300x200')
        # Se define el título de la ventana
        self.insert_datos.title("Insertar ciudad")
        self.insert_datos.resizable(width=0, height=0)

    # Se define la clase que vera la configuracion del label
    def __configuracion_label(self):
        # Definición de entradas de texto para la clase ciudad del ID
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        # se define la posicion de donde esta la entrada de texto
        id_lab.place(x = 10, y = 10, width = 120, height = 20)
        # Definición de entradas de texto para la clase ciudad del nombre
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        # se define la posicion de donde esta la entrada de texto
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)

    # Se define la clase que vera la configuracion del texto que entrada
    def __configuracion_text_entrada(self):
        # Se obtiene texto para ingresar el id de ciudad
        self.id = tk.Entry(self.insert_datos)
        # al obtener el texto se ingresa donde se ubicara
        self.id.place(x = 110, y = 10, width = 150, height = 20)
        # Se obtiene texto para ingresar el nombre de ciudad
        self.nombre = tk.Entry(self.insert_datos)
        # al obtener el texto se ingresa donde se ubicara
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)

    # Se define la clase que vera la configuracion del boton
    def __configuracion_boton(self):
        # Crea botón aceptar ingreso y se enlaza a evento, se detallan configuraciones
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
        # se define la ubicacion del boton
        btn_ok.place(x=100, y =160, width = 80, height = 20)

        # Crea botón cancelar ingreso y se enlaza a evento, se detallan configuraciones
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        # se define la ubicacion del boton
        btn_cancel.place(x=210, y =160, width = 80, height = 20)

    # se define la funcion que permite la Insercion en la base de datos.
    def __insertar(self):
        # Inserción de ciudad
        sql = """insert ciudad (id_ciudad, nom_ciudad) values (%(id)s, %(nombre)s)"""
        # Se ejecuta consulta
        self.db.run_sql(sql, {"id": self.id.get(),"nombre": self.nombre.get()})
        self.insert_datos.destroy()
        self.padre.llenar_treeview_ciudad()

# se crea la clase que modifica la ciudad
class modificar_ciudad:
    def __init__(self, db, padre, mod_select):
        # se definen los self de la base de datos y del padre
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        # Se genera una ventana emergente
        self.insert_datos = tk.Toplevel()
        # Se procede a llamar a cada una de las funciones necesarias
        self.__configuracion_ventana()
        self.__configuracion_label()
        self.__configuracion_text_entrada()
        self.__configuracion_boton()

    # esta funcion permite la configuracion de la ventana
    def __configuracion_ventana(self):
        # Se define el tamano de la ventana
        self.insert_datos.geometry('300x200')
        # Se define el título de la ventana
        self.insert_datos.title("Insertar ciudad")
        self.insert_datos.resizable(width=0, height=0)

    # Se define la clase que vera la configuracion del label
    def __configuracion_label(self):
        # Definición de entradas de texto para la clase ciudad del ID
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        # se define la posicion de donde esta la entrada de texto
        id_lab.place(x = 10, y = 10, width = 120, height = 20)
        # Definición de entradas de texto para la clase ciudad del nombre
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        # se define la posicion de donde esta la entrada de texto
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)


    # Se define la clase que vera la configuracion del texto que entrada
    def __configuracion_text_entrada(self):
        # Se obtiene texto para ingresar el id de ciudad
        self.id = tk.Entry(self.insert_datos)
        # al obtener el texto se ingresa donde se ubicara
        self.id.place(x = 110, y = 10, width = 150, height = 20)
        # Se obtiene texto para ingresar el nombre de ciudad
        self.nombre = tk.Entry(self.insert_datos)
        # al obtener el texto se ingresa donde se ubicara
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)

        # Se insertan datos actuales del registro
        self.id.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])


    # Se define la clase que vera la configuracion del boton
    def __configuracion_boton(self):
        # Crea botón aceptar y se enlaza a evento para modificar la ciudad
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 200, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x = 210, y = 200, width = 80, height = 20)

    def __modificar(self):
        # Modificar registro
        opEdicion = """update ciudad set id_ciudad = %(id)s, nom_ciudad = %(nombre)s
        where id_ciudad = %(id)s"""

        self.db.run_sql(opEdicion, {"id": self.id.get(),"nombre": self.nombre.get()})

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_ciudad()
