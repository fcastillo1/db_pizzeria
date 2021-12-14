#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Se definen las librerias de Tkinter a utilizar
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox

# Se define la clase que pertenecerá al vehiculo de la pizzería
class vehiculo:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Se crea una ventana top level que es superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de esta
        self.root.geometry('600x400')
        # Se escribe el título que tendrá la ventana
        self.root.title("Vehículos")
        # Se definen aspectos de su color y configuración
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de vehículos registrados
        self.__config_treeview_vehiculo()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_vehiculo()

    # Se genera una función que muestra el treeview
    def __config_treeview_vehiculo(self):
        # Se genera el treeview
        self.treeview = ttk.Treeview(self.root)
        # Se define el encabezado y el nombre de las columnas
        self.treeview.configure(show = "headings", columns = ("id_veh", "patente", "nom_tipo"))
        # Se detalla cada columna y la posición que tienen en el treeview
        self.treeview.heading("id_veh", text = "ID")
        self.treeview.heading("patente", text = "Patente")
        self.treeview.heading("nom_tipo", text = "Tipo")
        self.treeview.column("id_veh", minwidth = 150, width = 200, stretch = False)
        self.treeview.column("patente", minwidth = 150, width = 200, stretch = False)
        self.treeview.column("nom_tipo", minwidth = 150, width = 200, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 600)
        # Llenado del treeview
        self.llenar_treeview_vehiculo()
        self.root.after(0, self.llenar_treeview_vehiculo)

    # Se crea la función que tiene los botones para la funcionalidad de la ventana de vehículo
    def __crear_botones_vehiculo(self):
        # Botón para insertar
        b1 = tk.Button(self.root, text = "Insertar vehículo", bg = 'snow',
            fg = 'green', command = self.__insertar_vehiculo)
        # Se define su posición
        b1.place(x = 0, y = 350, width = 150, height = 50)

        # Botón para modificar
        b2 = tk.Button(self.root, text = "Modificar vehículo", bg = 'snow',
            fg = 'orange', command = self.__modificar_vehiculo)
         # Se define su posición
        b2.place(x = 150, y = 350, width = 150, height = 50)

        # Botón para eliminar
        b3 = tk.Button(self.root, text = "Eliminar vehículo", bg = 'snow',
            fg='red', command = self.__eliminar_vehiculo)
         # se define su posicion
        b3.place(x = 300, y = 350, width = 150, height = 50)

        # Botón para salir
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy,
            bg = 'red', fg = 'white')
         # se define su posicion
        b4.place(x = 450, y = 350, width = 150, height = 50)

    #  Se crea la función que permite llenar el treeview desde los datos de mysql
    def llenar_treeview_vehiculo(self):
        # Se obtienen vehículos ingresadas
        opTreeview = """SELECT id_veh, patente, nom_tipo from vehiculo join tipo
        on vehiculo.id_tipo = tipo.id_tipo;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(opTreeview)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:3])
            self.data = data

    # Se crea la función que permite la inserción del vehículo
    def __insertar_vehiculo(self):
        # Llamada a clase para hacer inserción
        insertar_vehiculo(self.db, self)

   #  Se crea la función que permite la eliminación del vehículo
    def __eliminar_vehiculo(self):
        if(self.treeview.focus() != ""):
            # se imprime un mensaje de advertencia
            if messagebox.askyesno(message = "¿Realmente quieres borrar el registro?", title = "Alerta")== True:
                # se lleva a cabo la operación (comandos mysql)
                opEliminar = "DELETE FROM vehiculo where id_veh = %(id_veh)s"
                self.db.run_sql(opEliminar, {"id_veh": self.treeview.focus()}, "D")

                # se actualiza el treeview
                self.llenar_treeview_vehiculo()

    # se genera la función que permite que el vehículo pueda ser modificado
    def __modificar_vehiculo(self):
        if(self.treeview.focus() != ""):
            # se imprime un mensaje de advertencia
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                # se lleva a cabo la operación (comandos mysql)
                opModificar = """SELECT id_veh, patente, nom_tipo from vehiculo
                join tipo on vehiculo.id_tipo = tipo.id_tipo WHERE id_veh = %(id)s"""
                # Se consulta tabla vehiculo por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]

                # llamada a clase de modificación con el registro actual
                modificar_vehiculo(self.db, self, mod_select)

    # se lleva a cabo la función que permite mostrar el tipo del vehículo a partir de dicha clase
    def __mostrar_tipo(self):
        tipo(self.root, self.db)

#  se crea la clase de la inserción del vehículo
class insertar_vehiculo:
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        # Ventana emergente
        self.insert_datos = tk.Toplevel()

        # Funcionalidades
        self.__config_button()
        self.__config_window()
        self.__config_label()
        self.__config_entry()

    # Se define la función que tiene que ver con la configuración de la ventana
    def __config_window(self):
        # Ajustes de ventana en tamano
        self.insert_datos.geometry('300x200')
         # Título de la ventana
        self.insert_datos.title("Insertar vehiculo")
        self.insert_datos.resizable(width = 0, height = 0)

     # Se define la función que se encarga de las entradas de texto (label)
    def __config_label(self):
        # Definición de entradas de texto para la tabla vehículo y su posición específica
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        patente_lab = tk.Label(self.insert_datos, text = "Patente: ")
        patente_lab.place(x = 10, y = 60, width = 120, height = 20)
        tipo_lab = tk.Label(self.insert_datos, text = "Tipo: ")
        tipo_lab.place(x = 10, y = 100, width = 120, height = 20)

    # Se define la función que permite la entrada de texto o de los datos
    def __config_entry(self):
        # Se obtiene texto para ingresar vehículos
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 20, width = 150, height = 20)
        self.patente = tk.Entry(self.insert_datos)
        self.patente.place(x = 110, y = 60, width = 150, height = 20)

        # Combobox para elegir tipo de vehículo
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 100, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        # Validación de combobox de tipos de vehículo
        if self.ids != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla tipo
            texto = "Ingresar registros en TIPO"
            messagebox.showerror("Problema de inserción", texto)
            # Destruye ventana
            self.insert_datos.destroy()

    # se crea la función que permite llenar el combobox a partir del tipo con su nombre y id
    def __llenar_combo(self):
        # se define la operatoria del combobox
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        self.data = self.db.run_select(opLCombo)
        # Se retorna nombre del tipo e id
        return [i[1] for i in self.data], [i[0] for i in self.data]

    # se define la función que permite la configuracion del boton de la ventana de insercion de vehiculo
    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg = 'green', fg = 'white')
        # se define su posicion
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        # se define su posicion
        btn_cancel.place(x = 210, y =160, width = 80, height = 20)

    # finalmente se genera la función que permite la insercion de los datos
    def __insertar(self):
        # Inserción en tabla vehichulo de la base de datos
        opInsert = """INSERT vehiculo (id_veh, patente, id_tipo) values
            (%(id)s, %(patente)s, %(tipo)s)"""

        # Se ejecuta consulta
        self.db.run_sql(opInsert, {"id": self.id.get(), "patente": self.patente.get(),
        "tipo": self.ids[self.combo.current()]}, "I")

        self.insert_datos.destroy()
        self.padre.llenar_treeview_vehiculo()

# se genera la clase que permite la modificación de los datos del vehiculo
class modificar_vehiculo:
    def __init__(self, db, padre, mod_select):
        # se conecta con la base de datos y con la base de datos padre para la modificación
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        # se genera la ventana para la modificación
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
        self.insert_datos.title("Modificar vehiculo")
        self.insert_datos.resizable(width = 0, height = 0)

     # se genera la función que tiene que ver con el label (entrada de texto)
    def __config_label(self):
        # Definición de entradas de texto para la tabla vehiculo y tambien la posición
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        patente_lab = tk.Label(self.insert_datos, text = "Patente: ")
        patente_lab.place(x = 10, y = 60, width = 120, height = 20)
        tipo_lab = tk.Label(self.insert_datos, text = "Tipo: ")
        tipo_lab.place(x = 10, y = 100, width = 120, height = 20)

     # esta función permite que se pueda obtener el texto que ingresa el usuario
     # tambien se muestra la posición en donde la información  es almacenada
    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas
        self.id = tk.Entry(self.insert_datos)
        # se define la ubicacion
        self.id.place(x = 110, y = 20, width = 150, height = 20)
        self.patente = tk.Entry(self.insert_datos)
        self.patente.place(x = 110, y = 60, width = 150, height = 20)

        # detalles para la entrada de datos del Combobox
        self.combo = ttk.Combobox(self.insert_datos)
        # se define la ubicacion
        self.combo.place(x = 110, y = 100, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        self.id_viejo = self.mod_select[0]
        # Se insertan valores actuales
        self.id.insert(0, self.mod_select[0])
        self.patente.insert(0, self.mod_select[1])
        self.combo.insert(0, self.mod_select[2])
        self.combo.config(state = "readonly")

    # se crea la función que permite que el combobox se llene
    def __llenar_combo(self):
        # se ingresa la opción para que se complete (comando mysql)
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        self.data = self.db.run_select(opLCombo)
        # Retorna nombre del tipo e id
        return [i[1] for i in self.data], [i[0] for i in self.data]

    # se crea la función que permite la creacion de los botones de la ventana modificar
    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar pizza
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        # se define su ubicacion
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        # se define su ubicacion
        btn_cancel.place(x = 210, y = 160, width = 80, height = 20)

    # se genera la función modificar que permite que los datos se cambien utilizando operatorias de mysql
    def __modificar(self):
        # se lleva a cabo la modificación  del registro y se utiliza el comando para la edicion de mysql
        opEdicion = """UPDATE vehiculo set id_veh = %(id)s, patente = %(patente)s,
            id_tipo = %(tipo)s WHERE id_veh = %(id_viejo)s"""

        # se genera la modificación  de los siguientes datos
        self.db.run_sql(opEdicion, {"id": self.id.get(),"patente": self.patente.get(),
        "tipo": self.ids[self.combo.current()], "id_viejo": self.id_viejo}, "U")
        self.insert_datos.destroy()

        # registros son actualizados a la ventana principal de vehiculo
        self.padre.llenar_treeview_vehiculo()
