#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox

class vehiculo:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Vehículos")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de pizzas registradas en la base de datos
        self.__config_treeview_vehiculo()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_vehiculo()

    def __config_treeview_vehiculo(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("id_veh", "patente", "nom_tipo"))
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

    def __crear_botones_vehiculo(self):
        # Botón para insertar
        b1 = tk.Button(self.root, text = "Insertar vehículo", bg = 'snow',
            fg = 'green', command = self.__insertar_vehiculo)
        b1.place(x = 0, y = 350, width = 150, height = 50)

        # Botón para modificar
        b2 = tk.Button(self.root, text = "Modificar vehículo", bg = 'snow',
            fg = 'orange', command = self.__modificar_vehiculo)
        b2.place(x = 150, y = 350, width = 150, height = 50)

        # Botón para eliminar
        b3 = tk.Button(self.root, text = "Eliminar vehículo", bg = 'snow',
            fg='red', command = self.__eliminar_vehiculo)
        b3.place(x = 300, y = 350, width = 150, height = 50)

        # Botón para salir
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy,
            bg = 'red', fg = 'white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

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

    def __insertar_vehiculo(self):
        insertar_vehiculo(self.db, self)

    def __eliminar_vehiculo(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message = "¿Realmente quieres borrar el registro?", title = "Alerta")== True:
                opEliminar = "DELETE FROM vehiculo where id_veh = %(id_veh)s"
                self.db.run_sql(opEliminar, {"id_veh": self.treeview.focus()})
                self.llenar_treeview_vehiculo()

    def __modificar_vehiculo(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT id_veh, patente, nom_tipo from vehiculo
                join tipo on vehiculo.id_tipo = tipo.id_tipo WHERE id_veh = %(id)s"""

                # Se consulta tabla vehiculo por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]
                modificar_vehiculo(self.db, self, mod_select)

    def __mostrar_tipo(self):
        tipo(self.root, self.db)

class insertar_vehiculo:
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
        self.insert_datos.title("Insertar pizza")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase vehiculo
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        patente_lab = tk.Label(self.insert_datos, text = "Patente: ")
        patente_lab.place(x = 10, y = 60, width = 120, height = 20)
        tipo_lab = tk.Label(self.insert_datos, text = "Tipo: ")
        tipo_lab.place(x = 10, y = 100, width = 120, height = 20)

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

    def __llenar_combo(self):
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y =160, width = 80, height = 20)

    def __insertar(self):
        # Inserción en tabla vehichulo de la base de datos
        opInsert = """INSERT vehiculo (id_veh, patente, id_tipo) values
            (%(id)s, %(patente)s, %(tipo)s)"""

        # Se ejecuta consulta
        self.db.run_sql(opInsert, {"id": self.id.get(),"": self.patente.get(),
        "patente": self.patente.get(), "tipo": self.ids[self.combo.current()]})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_vehiculo()

class modificar_vehiculo:
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
        self.insert_datos.title("Modificar vehiculo")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase vehiculo
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        patente_lab = tk.Label(self.insert_datos, text = "Patente: ")
        patente_lab.place(x = 10, y = 60, width = 120, height = 20)
        tipo_lab = tk.Label(self.insert_datos, text = "Tipo: ")
        tipo_lab.place(x = 10, y = 100, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 20, width = 150, height = 20)
        self.patente = tk.Entry(self.insert_datos)
        self.patente.place(x = 110, y = 60, width = 150, height = 20)

        # Combobox
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 100, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        # Se insertan valores actuales
        self.id_viejo = self.mod_select[0]
        self.id.insert(0, self.mod_select[0])
        self.patente.insert(0, self.mod_select[1])
        self.combo.insert(0, self.mod_select[2])

    def __llenar_combo(self):
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar pizza
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 160, width = 80, height = 20)

    def __modificar(self):
        opEdicion = """UPDATE vehiculo set id_veh = %(id)s, patente = %(patente)s,
            id_tipo = %(tipo)s WHERE id_veh = %(id_viejo)s"""

        self.db.run_sql(opEdicion, {"id": self.id.get(),"patente": self.patente.get(),
        "tipo": self.ids[self.combo.current()], "id_viejo": self.id_viejo})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_vehiculo()
