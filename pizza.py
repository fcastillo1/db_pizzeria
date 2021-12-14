#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox

class pizza:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Ventana emergente para mostrar información de la tabla pizza
        self.root = tk.Toplevel()
        
        # Configuraciones de la ventana
        self.root.geometry('600x400')
        self.root.title("Pizzas")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de pizzas registradas en la base de datos
        self.__config_treeview_pizza()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_pizza()

    def __config_treeview_pizza(self):
        # Se crea el treeview que muestra registros de la tabla pizza
        self.treeview = ttk.Treeview(self.root)
        # Se definen las columnas que mostrará el treeview
        self.treeview.configure(show = "headings", columns = ("id_piz", "nom_piz", "id_tam", "precio_piz"))
        
        # Para cada columna se establece un nombre representativo
        self.treeview.heading("id_piz", text = "ID")
        self.treeview.heading("nom_piz", text = "Nombre")
        self.treeview.heading("id_tam", text = "Tamaño")
        self.treeview.heading("precio_piz", text = "Precio")
        
        # Ajustes de tamaño para cada columna
        self.treeview.column("id_piz", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("nom_piz", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("id_tam", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("precio_piz", minwidth = 150, width = 150, stretch = False)
        
        # Ubicación del treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 600)
        
        # Llenado del treeview
        self.llenar_treeview_pizza()
        self.root.after(0, self.llenar_treeview_pizza)

    def __crear_botones_pizza(self):
        # Se define un botón que permite abrir una nueva ventana para insertar una pizza
        b1 = tk.Button(self.root, text = "Insertar pizza", bg='snow',
            fg='green', command = self.__insertar_pizza)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        
        # Se define un botón para modificar un registro seleccionado
        b2 = tk.Button(self.root, text = "Modificar pizza", bg='snow',
            fg='orange', command = self.__modificar_pizza)
        b2.place(x = 150, y = 350, width = 150, height = 50)
        
        # Permite la eliminación de un registro del treeview
        b3 = tk.Button(self.root, text = "Eliminar pizza", bg='snow', fg='red',
        command = self.__eliminar_pizza)
        b3.place(x = 300, y = 350, width = 150, height = 50)
        
        # Destruye la ventana que muestra las pizzas
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy,
            bg='red', fg='white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_pizza(self):
        # Se obtienen pizzas que están en la tabla pizza y el nombre del tamaño
        opTreeview = """SELECT id_piz, nom_piz, nom_tam, precio_piz from pizza
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
        # Llama a clase que permite ingresar pizza
        insertar_pizza(self.db, self)

    def __eliminar_pizza(self):
        # Consulta si hay un registro seleccionado en el treeview
        if(self.treeview.focus() != ""):
            # Confirma eliminación del registro seleccionado
            if messagebox.askyesno(message="¿Realmente quieres borrar el registro?", title = "Alerta")== True:
                # Consulta para eliminar el registro de acuerdo a id
                opEliminar = "DELETE FROM pizza where id_piz = %(id_piz)s"
                # Ejuta la eliminación del registro
                self.db.run_sql(opEliminar, {"id_piz": self.treeview.focus()}, "D")
                
                # Actualiza el treeview
                self.llenar_treeview_pizza()

    def __modificar_pizza(self):
         # Consulta si hay un registro seleccionado en el treeview
        if(self.treeview.focus() != ""):
            # Confirma la modificación del registro seleccionado
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                # Consulta para obtener información del registro seleccionado según id
                opModificar = """SELECT id_piz, nom_piz, nom_tam, precio_piz from pizza
                join tamano on pizza.id_tam = tamano.id_tam WHERE id_piz = %(id)s"""

                # Se consulta en la tabla pizza por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]
                # Llama a clase que permite modificar el registro
                modificar_pizza(self.db, self, mod_select)

class insertar_pizza:
    def __init__(self, db, padre):
        # Padre corresponde a la ventana principal de las pizzas
        self.padre = padre
        self.db = db

        # Ventana emergente para insertar nueva pizza
        self.insert_datos = tk.Toplevel()

        # Funcionalidades de la ventana
        self.__config_button()
        self.__config_window()
        self.__config_label()
        self.__config_entry()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x250')
        self.insert_datos.title("Insertar pizza")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Etiquetas para organizar entradas de texto para la clase pizza
        id_lab = tk.Label(self.insert_datos, text = "ID: ")
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 60, width = 120, height = 20)
        precio_lab = tk.Label(self.insert_datos, text = "Precio: ")
        precio_lab.place(x = 10, y = 100, width = 120, height = 20)
        tam_lab = tk.Label(self.insert_datos, text = "Tamaño: ")
        tam_lab.place(x = 10, y = 140, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas mediante entradas de texto
        # Permite ingresar id de la pizza,, nombre y precio
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 20, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 60, width = 150, height = 20)
        self.precio = tk.Entry(self.insert_datos)
        self.precio.place(x = 110, y = 100, width = 150, height = 20)

        # Combobox para elegir el tamaño de pizza
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 140, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        # Validación de combobox de tamaños
        if self.ids != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla tamano
            texto = "Ingresar registros en TAMANO"
            messagebox.showerror("Problema de inserción", texto)
            # Destruye ventana de ingreso de pizzas
            self.insert_datos.destroy()

    def __llenar_combo(self):
        # Consulta en tabla tamano para obtener información
        opLCombo = "SELECT id_tam, nom_tam FROM tamano"
        self.data = self.db.run_select(opLCombo)
        
        # Retorna nombre de tamaño e id
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
        # Inserción de pizza en la base de datos
        opInsert = """INSERT pizza (id_piz, nom_piz, id_tam, precio_piz) values
            (%(id)s, %(nombre)s, %(tamano)s, %(precio)s)"""

        # Se ejecuta consulta
        self.db.run_sql(opInsert, {"id": self.id.get(),"nombre": self.nombre.get(),
        "precio": self.precio.get(), "tamano": self.ids[self.combo.current()]}, "I")
        
        # Se destruye ventana de ingreso
        self.insert_datos.destroy()
        # Se actualiza el treeview de la ventana principal
        self.padre.llenar_treeview_pizza()

class modificar_pizza:
    def __init__(self, db, padre, mod_select):
        # Se recibe ventana principal
        self.padre = padre
        self.db = db
        
        # Información actual del registro a modificar
        self.mod_select = mod_select
        
        # Creación de ventana emergente para la modificación
        self.insert_datos = tk.Toplevel()
        
        # Funcionalidades de la ventana
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
        id_lab.place(x = 10, y = 20, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 60, width = 120, height = 20)
        precio_lab = tk.Label(self.insert_datos, text = "Precio: ")
        precio_lab.place(x = 10, y = 100, width = 120, height = 20)
        tam_lab = tk.Label(self.insert_datos, text = "Tamaño: ")
        tam_lab.place(x = 10, y = 140, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas
        # Permite modificar id, nombre y precio
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 20, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 60, width = 150, height = 20)
        self.precio = tk.Entry(self.insert_datos)
        self.precio.place(x = 110, y = 100, width = 150, height = 20)

        # Combobox que permite modificar el tamaño
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 140, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()
        
        # Se obtiene id actual del registro a modificar
        self.id_viejo = self.mod_select[0]
        
        # Se insertan valores actuales del registro a modificar
        self.id.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])
        self.combo.insert(0, self.mod_select[2])
        self.combo.config(state = "readonly")
        self.precio.insert(0, self.mod_select[3])

    def __llenar_combo(self):
        # Obtiene la información de la tabla tamaño
        opLCombo = "SELECT id_tam, nom_tam FROM tamano"
        self.data = self.db.run_select(opLCombo)
        
        # Se retorna el nombre e id del tamaño
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
        # Consulta que permite actualizar el registro seleccionado usando id 
        opEdicion = """UPDATE pizza set id_piz = %(id)s, nom_piz = %(nombre)s,
            id_tam = %(tamano)s, precio_piz = %(precio)s WHERE id_piz = %(id_viejo)s"""
        
        # Se ejecuta consulta
        self.db.run_sql(opEdicion, {"id": self.id.get(),"nombre": self.nombre.get(),
        "precio": self.precio.get(), "tamano": self.ids[self.combo.current()], "id_viejo": self.id_viejo}, "U")
        
        # Destruye ventana de modificación
        self.insert_datos.destroy()
        
        # Actualiza treeview
        self.padre.llenar_treeview_pizza()
