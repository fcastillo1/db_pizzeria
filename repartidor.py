#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Se definen las librerias de Tkinter a utilizar 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Se define la clase que pertenecera al repartidor
class repartidor:
    # Se crea la funcion del self y del root que permite la construccion de las ventanas de esta opcion de la pizzeria
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Se crea una ventana top level que es superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de esta
        self.root.geometry('600x400')
        # se escribe el titulo que tendra la ventana
        self.root.title("Repartidores")
        # se definen aspectos de su color y configuracion
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de repartidoress registrados en la base de datos
        self.__config_treeview_repartidor()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_repartidor()

     # Se genera una funcion que muestra el trevieew
    def __config_treeview_repartidor(self):
        self.treeview = ttk.Treeview(self.root)
        # Se define el encabezado y el nombre de las columnas
        self.treeview.configure(show = "headings", columns = ("rut_rep", "nom_rep", "ape_rep", "tel_rep"))
        # se detalla cada treeview y la posicion que este tendra
        self.treeview.heading("rut_rep", text = "Rut")
        self.treeview.heading("nom_rep", text = "Nombre")
        self.treeview.heading("ape_rep", text = "Apellido")
        self.treeview.heading("tel_rep", text = "Teléfono")
        self.treeview.column("rut_rep", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("nom_rep", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("ape_rep", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("tel_rep", minwidth = 150, width = 150, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 600)
        # Llenado del treeview
        self.llenar_treeview_repartidor()
        self.root.after(0, self.llenar_treeview_repartidor)

     # Se crea una funcion que permite generar los botones de la ventana
    def __crear_botones_repartidor(self):
        #  se crea el primer boton que permite la insercion
        b1 = tk.Button(self.root, text = "Insertar repartidor", bg ='snow',
            fg = 'green', command = self.__insertar_repartidor)
        # se definen sus aspectos y posicion
        b1.place(x = 0, y = 350, width = 150, height = 50)
        
         #  se crea el segundo boton que permite la insercion
        b2 = tk.Button(self.root, text = "Modificar repartidor", bg ='snow',
            fg = 'orange', command = self.__modificar_repartidor)
        # se definen sus aspectos y posicion
        b2.place(x = 150, y = 350, width = 150, height = 50)
        
         #  se crea el tercer boton que permite la insercion
        b3 = tk.Button(self.root, text = "Eliminar repartidor", bg = 'snow',
            fg = 'red', command = self.__eliminar_repartidor)
         # se definen sus aspectos y posicion
        b3.place(x = 300, y = 350, width = 150, height = 50)
        
         #  se crea el cuarto boton que permite la insercion
        b4 = tk.Button(self.root, text = "Salir", command = self.root.destroy,
            bg = 'red', fg = 'white')
         # se definen sus aspectos y posicion
        b4.place(x = 450, y = 350, width = 150, height = 50)
        
 #  se crea la funcion que permite llenar el treeview desde los datos de mysql
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
            
   # se crea la funcion que permite la insercion a partir de la clase
    def __insertar_repartidor(self):
        insertar_repartidor(self.db, self)
        
     #  se crea la funcion que permite la eliminacion del repartidor
    def __eliminar_repartidor(self):
        if(self.treeview.focus() != ""):
             #  imprime un mensaje de alerta
            if messagebox.askyesno(message = "¿Realmente quieres borrar el repartidor?", title = "Alerta")==True:
                operation = "DELETE FROM repartidor WHERE rut_rep = %(rut_rep)s"
                # se lleva a cabo la operacion
                self.db.run_sql(operation, {"rut_rep": self.treeview.focus()}, "D")
                self.llenar_treeview_repartidor()
                
    #  se crea la funcion que permite la modificacion del repartidor
    def __modificar_repartidor(self):
        if(self.treeview.focus() != ""):
            #  imprime un mensaje de alerta
            if messagebox.askyesno(message = "¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT rut_rep, nom_rep, ape_rep, tel_rep FROM repartidor WHERE rut_rep = %(rut_rep)s"""
                # Se consulta en la tabla repartidor por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"rut_rep": self.treeview.focus()})[0]
                modificar_repartidor(self.db, self, mod_select)

#  se crea la clase de la insercion del repartidor
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

    # Se define la funcion que tiene que ver con la configuracion de la ventana
    def __config_window(self):
        # Ajustes de ventana en tamano
        self.insert_datos.geometry('300x200')
         # Titulo de la ventana
        self.insert_datos.title("Insertar repartidor")
        self.insert_datos.resizable(width = 0, height = 0)

    # Se define la funcion que se encarga de las entradas de texto (label)
    def __config_label(self):
        # Definición de entradas de texto para la clase repartidor y su posicion especifica
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)

    # Se define la funcion que permite la entrada de texto o de los datos. 
    def __config_entry(self):
        # Se obtiene texto para ingresar datos del repartidor en este caso rut, nombre, apellido y telefono
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)
        
    # Se define la funcion que permite la configuracion del boton de la ventana de ingreso
    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg = 'green', fg = 'white')
        btn_ok.place(x= 90, y = 160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x= 200, y = 160, width = 80, height = 20)

    # Se define la funcion que permite la insercion de los datos a partir del mysql
    def __insertar(self):
        # Inserción de repartidor
        sql = """insert repartidor (rut_rep, nom_rep, ape_rep, tel_rep) values
                (%(rut)s, %(nombre)s, %(apellido)s, %(telefono)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get()}, "I")

        self.insert_datos.destroy()
        self.padre.llenar_treeview_repartidor()

# Se genera la clase que permite la modificacion de los datos del repartidor
class modificar_repartidor:
    def __init__(self, db, padre, mod_select):
        # se conecta con la base de datos y con la base de datos padre para la modificacion
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        self.insert_datos = tk.Toplevel()

        # Funcionalidades
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    # Se define la ventana que permite la configuracion de la ventana
    def __config_window(self):
        # Ajustes de ventana en cuanto a tamaño
        self.insert_datos.geometry('300x200')
        # se define el titulo que tendra la ventana y su posicion
        self.insert_datos.title("Modificar repartidor")
        self.insert_datos.resizable(width = 0, height = 0)
        
    # se genera la funcion que tiene que ver con el label (entrada de texto)
    def __config_label(self):
        # Definición de entradas de texto para la clase repartidor cuando se modifica
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)

     # esta funcion permite que se pueda obtener el texto que ingresa el usuario 
     # tambien se muestra la posicion en donde la informacion es almacenada
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

        # Se insertan datos actuales del registro, en este caso rut_viejo se modificara con el nuevo
        self.rut_viejo = self.mod_select[0]
        self.rut.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])
        self.apellido.insert(0, self.mod_select[2])
        self.telefono.insert(0, self.mod_select[3])
        
    # se crea la funcion que permite la creacion de los botones de la ventana modificar
    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar el repartidor
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 90, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 200, y = 160, width = 80, height = 20)

     # se genera la funcion modificar que permite que los datos se cambien utilizando operatorias de mysql
    def __modificar(self):
        # Modificar registro
        opEdicion = """UPDATE repartidor SET rut_rep = %(rut)s, nom_rep = %(nombre)s,
        ape_rep = %(apellido)s, tel_rep = %(telefono)s WHERE rut_rep = %(rut_viejo)s"""

        self.db.run_sql(opEdicion, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "rut_viejo": self.rut_viejo}, "U")

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_repartidor()
