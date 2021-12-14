#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Se definen las librerias de Tkinter a utilizar 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Se define la clase que pertenecera al tipo
class tipo:
    def __init__(self, root, db):
         # Se crea la funcion del self y del root que permite la construccion de las ventanas de esta opcion de la pizzeria
        self.db = db
        self.data = []

        # Se crea una ventana top level que es superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de esta
        self.root.geometry('600x400')
        # se escribe el titulo que tendra la ventana
        self.root.title("Tipos de Vehículos")
        # se definen aspectos de su color y configuracion
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de tipos registrados en la base de datos
        self.__config_treeview_tipo()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_tipo()

    # Se genera una funcion que muestra el trevieew
    def __config_treeview_tipo(self):
        self.treeview = ttk.Treeview(self.root)
        # Se define el encabezado y el nombre de las columnas
        self.treeview.configure(show = "headings", columns = ("id_tipo", "nom_tipo", "capacidad_tipo"))
        # se detalla cada treeview y la posicion que este tendra
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

     # Se crea una funcion que permite generar los botones de la ventana
    def __crear_botones_tipo(self):
        #  se crea el primer boton que permite la insercion de los datos
        b1 = tk.Button(self.root, text = "Insertar tipo", bg ='snow',
            fg = 'green', command = self.__insertar_tipo)
        # se define su ubicacion
        b1.place(x = 0, y = 350, width = 150, height = 50)
        
          #  se crea el primer boton que permite la modificacion de datos
        b2 = tk.Button(self.root, text = "Modificar tipo", bg ='snow',
            fg = 'orange', command = self.__modificar_tipo)
         # se define su ubicacion
        b2.place(x = 150, y = 350, width = 150, height = 50)
        
          #  se crea el primer boton que permite la eliminacion de datos
        b3 = tk.Button(self.root, text = "Eliminar tipo", bg='snow',
            fg = 'red', command = self.__eliminar_tipo)
         # se define su ubicacion
        b3.place(x = 300, y = 350, width = 150, height = 50)
        
          #  se crea el primer boton que permite la salida de la ventana
        b4 = tk.Button(self.root, text = "Salir", command = self.root.destroy,
            bg = 'red', fg = 'white')
         # se define su ubicacion
        b4.place(x = 450, y = 350, width = 150, height = 50)

     #  se crea la funcion que permite llenar el treeview desde los datos de mysql
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

     # se crea la funcion que permite la insercion del tipo a partir de la clase
    def __insertar_tipo(self):
        insertar_tipo(self.db, self)

    #  se crea la funcion que permite la eliminacion del tipo
    def __eliminar_tipo(self):
        if(self.treeview.focus() != ""):
            #  imprime un mensaje de alerta
            if messagebox.askyesno(message="¿Realmente quieres borrar el tipo?", title = "Alerta")==True:
                operation = "DELETE FROM tipo where id_tipo = %(id_tipo)s"
                # se lleva a cabo la operacion
                self.db.run_sql(operation, {"id_tipo": self.treeview.focus()}, "D")
                self.llenar_treeview_tipo()

    # se crea la funcion que permite que el tipo si pueda ser modificado de manera correcta
    def __modificar_tipo(self):
        if(self.treeview.focus() != ""):
            # se imprime un mensaje de alerta
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                # se lleva a cabo la operacion
                opModificar = """SELECT id_tipo, nom_tipo, capacidad_tipo from tipo where id_tipo = %(id_tipo)s"""
                # Se consulta en la tabla tipo por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id_tipo": self.treeview.focus()})[0]
                modificar_tipo(self.db, self, mod_select)

#  se crea la clase de la insercion del tipo (vehiculo)
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

    
    # Se define la funcion que tiene que ver con la configuracion de la ventana
    def __config_window(self):
        # Ajustes de ventana en tamano
        self.insert_datos.geometry('300x200')
         # Titulo de la ventana
        self.insert_datos.title("Insertar tipo")
        self.insert_datos.resizable(width = 0, height = 0)

    # Se define la funcion que se encarga de las entradas de texto (label)
    def __config_label(self):
        # Definición de entradas de texto para la clase tipo y tambien la posicion de esta
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        cap_lab = tk.Label(self.insert_datos, text = "Capacidad: ")
        cap_lab.place(x = 10, y = 80, width = 120, height = 20)

    # Se define la funcion que permite la entrada de texto o de los datos. 
    def __config_entry(self):
        # Se obtiene texto para ingresar tipo para el nombre y capacidad
        # en este caso el id no se copleta porque su valor se autoincrementa
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.capacidad = tk.Entry(self.insert_datos)
        self.capacidad.place(x = 110, y = 80, width = 150, height = 20)

    # Se define la funcion que permite la configuracion del boton de la ventana de ingreso
    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
        # se define la ubicacion
        btn_ok.place(x=100, y =160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        # se define la ubicacion
        btn_cancel.place(x=210, y =160, width = 80, height = 20)

    # Se define la funcion que permite la insercion de los datos a partir del mysql
    def __insertar(self): #Insercion en la base de datos.
        # Inserción de tipo
        sql = """INSERT tipo (nom_tipo, capacidad_tipo) VALUES (%(nombre)s,
        %(capacidad)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"nombre": self.nombre.get(),
        "capacidad": self.capacidad.get()}, "I")

        self.insert_datos.destroy()
        self.padre.llenar_treeview_tipo()

# Se genera la clase que permite la modificacion de los datos del tipo
class modificar_tipo:
    def __init__(self, db, padre, mod_select):
        # se conecta con la base de datos y con la base de datos padre para la modificacion
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        # se procede a la creacion de una ventana para la modificacion
        self.insert_datos = tk.Toplevel()
        # se definen las funcionalidades
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    # Se define la ventana que permite la configuracion de la ventana
    def __config_window(self):
        # Ajustes de ventana en cuanto a tamaño
        self.insert_datos.geometry('300x200')
        # se define el titulo que tendra la ventana y su posicion
        self.insert_datos.title("Modificar tipo")
        self.insert_datos.resizable(width = 0, height = 0)

     # se genera la funcion que tiene que ver con el label (entrada de texto)
    def __config_label(self):
        # Definición de entradas de texto para la clase tipo y su ubicacion por coordenadas
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 60, width = 120, height = 20)
        cap_lab = tk.Label(self.insert_datos, text = "Capacidad: ")
        cap_lab.place(x = 10, y = 100, width = 120, height = 20)

     # esta funcion permite que se pueda obtener el texto que ingresa el usuario 
     # tambien se muestra la posicion en donde la informacion es almacenada
    def __config_entry(self):
        # Se obtiene texto para ingresar tipos y tambien la posicion(coordenadas)donde ira
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

    # se crea la funcion que permite la creacion de los botones de la ventana modificar
    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar el tipo
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        # se define su ubicacion
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        # se define su ubicacion
        btn_cancel.place(x = 210, y = 160, width = 80, height = 20)

    # se genera la funcion modificar que permite que los datos se cambien utilizando operatorias de mysql
    def __modificar(self):
        # Modificar registro
        opEdicion = """UPDATE tipo SET nom_tipo = %(nombre)s, capacidad_tipo = %(capacidad)s
        WHERE id_tipo = %(id)s"""
        # se lleva a cabo la operacion
        self.db.run_sql(opEdicion, {"id": self.id.get(),"nombre": self.nombre.get(),
        "capacidad": self.capacidad.get()}, "U")

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_tipo()
