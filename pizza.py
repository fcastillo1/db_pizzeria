#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox

from tamano import tamano

class pizza:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Pizzas")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Menubar
        self.__crear_menu()

        # Visualización de pizzas registradas en la base de datos
        self.__config_treeview_pizza()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_pizza()

    def __config_treeview_pizza(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("id_piz", "nom_piz", "precio_piz",
            "id_tam"))
        self.treeview.heading("id_piz", text = "ID")
        self.treeview.heading("nom_piz", text = "Nombre")
        self.treeview.heading("precio_piz", text = "Precio")
        self.treeview.heading("id_tam", text = "Tamaño")
        self.treeview.column("id_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("precio_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("id_tam", minwidth = 150, width = 100, stretch = False)
        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # Llenado del treeview
        self.llenar_treeview_pizza()
        self.root.after(0, self.llenar_treeview_pizza)

    def __crear_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu = menubar)

        # Se construye el menú de la información con su color
        info_menu = Menu(menubar, tearoff = 0, bg = "white")
        menubar.add_cascade(label = "Opciones", menu = info_menu)

        info_menu.add_command(label = "Ver tamaños", command = self.__mostrar_tamano)

    def __crear_botones_pizza(self):
        b1 = tk.Button(self.root, text = "Insertar pizza", bg='snow',
            fg='green', command = self.__insertar_pizza)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text = "Modificar pizza", bg='snow',
            fg='orange', command = self.__modificar_pizza)
        b2.place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar pizza", bg='snow', fg='red',
        command = self.__eliminar_pizza)
        b3.place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy,
            bg='red', fg='white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_pizza(self):
        # Se obtienen pizzas ingresadas
        opTreeview = """SELECT id_piz, nom_piz, precio_piz, nom_tam from pizza
        join tamano on pizza.id_tam = tamano.id_tam;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(opTreeview)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:4])

            self.data = data

    def __insertar_pizza(self):
        insertar_pizza(self.db, self)

    def __eliminar_pizza(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message="¿Realmente quieres borrar el registro?", title = "Alerta")== True:
                opEliminar = "DELETE FROM pizza where id_piz = %(id_piz)s"
                self.db.run_sql(opEliminar, {"id_piz": self.treeview.focus()})
                self.llenar_treeview_pizza()

    def __modificar_pizza(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT id_piz, nom_piz, precio_piz, nom_tam from pizza
                join tamano on pizza.id_tam = tamano.id_tam WHERE id_piz = %(id)s"""

                # Se consulta en la tabla pizza por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]
                modificar_pizza(self.db, self, mod_select)

    def __mostrar_tamano(self):
        tamano(self.root, self.db)

class insertar_pizza:
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
        self.insert_datos.geometry('300x250')
        self.insert_datos.title("Insertar pizza")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Definición de entradas de texto para la clase pizza
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        precio_lab = tk.Label(self.insert_datos, text = "Precio: ")
        precio_lab.place(x = 10, y = 70, width = 120, height = 20)
        tam_lab = tk.Label(self.insert_datos, text = "Tamaño: ")
        tam_lab.place(x = 10, y = 100, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.precio = tk.Entry(self.insert_datos)
        self.precio.place(x = 110, y = 70, width = 150, height = 20)

        # Combobox para elegir el tamaño de pizza
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 100, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

    def __llenar_combo(self):
        opLCombo = "SELECT id_tam, nom_tam FROM tamano"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tam
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
        btn_ok.place(x=100, y =200, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x=210, y =200, width = 80, height = 20)

    def __insertar(self): #Insercion en la base de datos.
        # Inserción de pizza
        opInsert = """INSERT pizza (id_piz, nom_piz, precio_piz, id_tam) values
            (%(id)s, %(nombre)s, %(precio)s, %(tamano)s)"""

        # Se ejecuta consulta
        self.db.run_sql(opInsert, {"id": self.id.get(),"nombre": self.nombre.get(),
        "precio": self.precio.get(), "tamano": self.ids[self.combo.current()]})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_pizza()

class modificar_pizza:
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
        self.insert_datos.geometry('300x250')
        self.insert_datos.title("Modificar pizza")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase pizza
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        precio_lab = tk.Label(self.insert_datos, text = "Precio: ")
        precio_lab.place(x = 10, y = 70, width = 120, height = 20)
        tam_lab = tk.Label(self.insert_datos, text = "Tamaño: ")
        tam_lab.place(x = 10, y = 100, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.precio = tk.Entry(self.insert_datos)
        self.precio.place(x = 110, y = 70, width = 150, height = 20)

        # Combobox
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 100, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        # Se insertan valores actuales
        self.id_viejo = self.mod_select[0]
        self.id.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])
        self.precio.insert(0, self.mod_select[2])
        self.combo.insert(0, self.mod_select[3])

    def __llenar_combo(self):
        opLCombo = "SELECT id_tam, nom_tam FROM tamano"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tam
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar pizza
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 200, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x = 210, y = 200, width = 80, height = 20)

    def __modificar(self):
        opEdicion = """UPDATE pizza set id_piz = %(id)s, nom_piz = %(nombre)s,
            precio_piz = %(precio)s, id_tam = %(tamano)s WHERE id_piz = %(id_viejo)s"""

        self.db.run_sql(opEdicion, {"id": self.id.get(),"nombre": self.nombre.get(),
        "precio": self.precio.get(), "tamano": self.ids[self.combo.current()], "id_viejo": self.id_viejo})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_pizza()
