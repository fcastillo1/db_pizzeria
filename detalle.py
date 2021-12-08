#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class detalle:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Detalle")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de detalles registrados en la base de datos
        self.__config_treeview_detalle()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_detalle()

    def __config_treeview_detalle(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("id_pedido", "id_piz", "cantidad", "precio_piz"))
        self.treeview.heading("id_pedido", text = "Pedido")
        self.treeview.heading("id_piz", text = "Pizza")
        self.treeview.heading("cantidad", text = "Cantidad")
        self.treeview.heading("precio_piz", text = "Precio")

        self.treeview.bind('<ButtonRelease-1>', self.selec_registro)

        self.treeview.column("id_pedido", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("id_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("cantidad", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("precio_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # Llenado del treeview
        self.llenar_treeview_detalle()

        self.root.after(0, self.llenar_treeview_detalle)

    def __crear_botones_detalle(self):
        b1 = tk.Button(self.root, text = "Insertar detalle", bg ='snow',
            fg = 'green', command = self.__insertar_detalle)
        b1.place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text = "Modificar detalle", bg ='snow',
            fg = 'orange', command = self.__modificar_detalle)
        b2.place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar detalle", bg='snow',
            fg = 'red', command = self.__eliminar_detalle)
        b3.place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command = self.root.destroy,
            bg = 'red', fg = 'white')
        b4.place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_detalle(self):
        # Se obtienen detalles ingresadas
        sql = """select id_pedido, id_piz, cantidad, precio_piz from detalle;"""

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

    def selec_registro(self, valor):
        seleccion = self.treeview.item(self.treeview.focus())
        # Obtiene id del pedido e id de la pizza
        self.actual = seleccion["values"][0:2]

    def __insertar_detalle(self):
        insertar_detalle(self.db, self)

    def __eliminar_detalle(self):
        seleccion = self.treeview.item(self.treeview.focus())
        # Obtiene id del pedido e id de la pizza
        self.actual = seleccion["values"][0:2]

        if(self.actual != ""):
            if messagebox.askyesno(message="¿Realmente quieres borrar el detalle?", title = "Alerta")==True:
                operation = "DELETE FROM detalle where id_pedido = %(ped)s and id_piz = %(piz)s"
                self.db.run_sql(operation, {"ped": self.actual[0], "piz": self.actual[1]})
                self.llenar_treeview_detalle()

    def __modificar_detalle(self):
        if(self.actual != ""):
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT id_pedido, id_piz, cantidad, precio_piz from detalle where id_pedido = %(ped)s and id_piz = %(piz)s"""

                # Se consulta en la tabla detalle por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"ped": self.actual[0], "piz": self.actual[1]})[0]
                # print(mod_select)
                modificar_detalle(self.db, self, mod_select)


#
class insertar_detalle:
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
        self.insert_datos.title("Insertar detalle")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase detalle
        pedido_lab = tk.Label(self.insert_datos, text = "Pedido: ")
        pedido_lab.place(x = 10, y = 10, width = 120, height = 20)
        pizza_lab = tk.Label(self.insert_datos, text = "Pizza: ")
        pizza_lab.place(x = 10, y = 40, width = 120, height = 20)
        cant_lab = tk.Label(self.insert_datos, text = "Cantidad: ")
        cant_lab.place(x = 10, y = 70, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar detalle

        # Combobox para elegir pedido
        self.combo_ped = ttk.Combobox(self.insert_datos)
        self.combo_ped.place(x = 110, y = 10, width = 150, height= 20)
        self.combo_ped["values"], self.ids_ped = self.__llenar_combo_ped()

        # Combobox para elegir pizza
        self.combo_piz = ttk.Combobox(self.insert_datos)
        self.combo_piz.place(x = 110, y = 40, width = 150, height= 20)
        self.combo_piz["values"], self.ids_piz = self.__llenar_combo_piz()

        # Entrada de cantidad
        self.cant = tk.Entry(self.insert_datos)
        self.cant.place(x = 110, y = 70, width = 150, height = 20)

    def __llenar_combo_ped(self):
        opLCombo = "SELECT id_pedido FROM pedido"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo_piz(self):
        opLCombo = "SELECT id_piz, nom_piz FROM pizza"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nombre de la pizza
        return [i[1] for i in self.data], [i[0] for i in self.data]

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
        # Inserción de detalle
        sql = """INSERT detalle (id_pedido, id_piz, cantidad) VALUES (%(pedido)s,
        %(pizza)s, %(cantidad)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"pedido": self.ids_ped[self.combo_ped.current()],
        "pizza": self.ids_piz[self.combo_piz.current()], "cantidad": self.cant.get()})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_detalle()

class modificar_detalle:
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
        self.insert_datos.title("Modificar detalle")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase detalle
        pedido_lab = tk.Label(self.insert_datos, text = "Pedido: ")
        pedido_lab.place(x = 10, y = 10, width = 120, height = 20)
        pizza_lab = tk.Label(self.insert_datos, text = "Pizza: ")
        pizza_lab.place(x = 10, y = 40, width = 120, height = 20)
        cant_lab = tk.Label(self.insert_datos, text = "Cantidad: ")
        cant_lab.place(x = 10, y = 70, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar detalles

        self.combo_ped = ttk.Combobox(self.insert_datos)
        self.combo_ped.place(x = 110, y = 10, width = 150, height= 20)
        self.combo_ped["values"], self.ids_ped = self.__llenar_combo_ped()

        # Combobox para elegir pizza
        self.combo_piz = ttk.Combobox(self.insert_datos)
        self.combo_piz.place(x = 110, y = 40, width = 150, height= 20)
        self.combo_piz["values"], self.ids_piz = self.__llenar_combo_piz()

        # Entrada de cantidad
        self.cant = tk.Entry(self.insert_datos)
        self.cant.place(x = 110, y = 70, width = 150, height = 20)

        # Se insertan datos actuales del registro
        self.combo_ped.insert(0, self.mod_select[0])
        self.combo_piz.insert(0, self.mod_select[1])
        self.cant.insert(0, self.mod_select[2])

    def __llenar_combo_ped(self):
        opLCombo = "SELECT id_pedido FROM pedido"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo_piz(self):
        opLCombo = "SELECT id_piz, nom_piz FROM pizza"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nombre de la pizza
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar el detalle
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 200, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 200, width = 80, height = 20)

    def __modificar(self):
        # Modificar registro
        opEdicion = """UPDATE detalle SET id_pedido = %(ped)s, id_piz = %(piz)s, cantidad = %(cant)s WHERE id_pedido = %(ped)s and id_piz = %(piz)s"""

        self.db.run_sql(opEdicion, {"ped": self.ids_ped[self.combo_ped.current()],
        "piz": self.ids_piz[self.combo_piz.current()], "cant": self.cant.get()})

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_detalle()
