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
        self.root.geometry('720x400')
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
        self.treeview.configure(show = "headings", columns = ("id_pedido", "id_piz",
                                "nom_piz", "nom_tam", "cantidad", "precio_piz", "precio_total"))
        # Nombres para cada columna
        self.treeview.heading("id_pedido", text = "Pedido")
        self.treeview.heading("id_piz", text = "ID Pizza")
        self.treeview.heading("nom_piz", text = "Pizza")
        self.treeview.heading("nom_tam", text = "Tamaño")
        self.treeview.heading("cantidad", text = "Cantidad")
        self.treeview.heading("precio_piz", text = "Precio unitario")
        self.treeview.heading("precio_total", text = "Precio total")

        # Dimensiones para cada columna
        self.treeview.column("id_pedido", minwidth = 150, width = 80, stretch = False)
        self.treeview.column("id_piz", minwidth = 150, width = 80, stretch = False)
        self.treeview.column("nom_piz", minwidth = 150, width = 120, stretch = False)
        self.treeview.column("nom_tam", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("cantidad", minwidth = 100, width = 100, stretch = False)
        self.treeview.column("precio_piz", minwidth = 100, width = 120, stretch = False)
        self.treeview.column("precio_total", minwidth = 100, width = 120, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 810)
        # Llenado del treeview
        self.llenar_treeview_detalle()
        self.root.after(0, self.llenar_treeview_detalle)

        # Ajuste treeview para seleccionar registros con dos claves primarias
        self.treeview.bind('<ButtonRelease-1>', self.selec_registro)

    def __crear_botones_detalle(self):
        b1 = tk.Button(self.root, text = "Insertar detalle", bg ='snow',
            fg = 'green', command = self.__insertar_detalle)
        b1.place(x = 0, y = 350, width = 180, height = 50)
        b2 = tk.Button(self.root, text = "Modificar detalle", bg ='snow',
            fg = 'orange', command = self.__modificar_detalle)
        b2.place(x = 180, y = 350, width = 180, height = 50)
        b3 = tk.Button(self.root, text = "Eliminar detalle", bg='snow',
            fg = 'red', command = self.__eliminar_detalle)
        b3.place(x = 360, y = 350, width = 180, height = 50)
        b4 = tk.Button(self.root, text = "Salir", command = self.root.destroy,
            bg = 'red', fg = 'white')
        b4.place(x = 540, y = 350, width = 180, height = 50)

    def llenar_treeview_detalle(self):
        # Se obtienen detalles ingresadas
        sql = """SELECT id_pedido, pizza.id_piz, nom_piz, nom_tam, cantidad, detalle.precio_piz,
        precio_total FROM detalle JOIN pizza ON detalle.id_piz = pizza.id_piz JOIN tamano ON pizza.id_tam = tamano.id_tam"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(sql)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0:2], values = i[0:7])

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
                self.db.run_sql(operation, {"ped": self.actual[0], "piz": self.actual[1]}, "D")
                self.llenar_treeview_detalle()

    def __modificar_detalle(self):
        if(self.actual != ""):
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:

                # Consulta
                opModificar = """SELECT id_pedido, detalle.id_piz, nom_piz, nom_tam,
                cantidad, detalle.precio_piz, precio_total FROM detalle JOIN pizza ON detalle.id_piz = pizza.id_piz
                JOIN tamano ON pizza.id_tam = tamano.id_tam WHERE id_pedido = %(ped)s and
                detalle.id_piz = %(piz)s"""

                # Se consulta en la tabla detalle con base en claves primarias
                mod_select = self.db.run_select_filter(opModificar, {"ped": self.actual[0], "piz": self.actual[1]})[0]
                modificar_detalle(self.db, self, mod_select)

class insertar_detalle:
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

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x200')
        self.insert_datos.title("Insertar detalle")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase detalle
        pedido_lab = tk.Label(self.insert_datos, text = "Pedido: ")
        pedido_lab.place(x = 10, y = 35, width = 140, height = 20)
        pizza_lab = tk.Label(self.insert_datos, text = "Pizza: ")
        pizza_lab.place(x = 10, y = 70, width = 150, height = 20)
        cant_lab = tk.Label(self.insert_datos, text = "Cantidad: ")
        cant_lab.place(x = 10, y = 105, width = 140, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar detalle

        # Combobox para elegir pedido
        self.combo_ped = ttk.Combobox(self.insert_datos)
        self.combo_ped.place(x = 110, y = 35, width = 150, height= 20)
        self.combo_ped["values"], self.ids_ped = self.__llenar_combo_ped()

        # Combobox para elegir pizza
        self.combo_piz = ttk.Combobox(self.insert_datos)
        self.combo_piz.place(x = 110, y = 70, width = 150, height= 20)
        self.combo_piz["values"], self.ids_piz = self.__llenar_combo_piz()

        # Entrada de texto para cantidad
        self.cant = tk.Entry(self.insert_datos)
        self.cant.place(x = 110, y = 105, width = 150, height = 20)

        # Validación de combobox de pedido y pizza
        if (self.ids_ped != [] and self.ids_piz != []):
            # Si combo de pizzas no está vacío, se coloca por defecto el primer ítem
            self.combo_piz.insert(0, self.combo_piz["values"][0])
            self.combo_piz.config(state = "readonly")

            # Si combo de pedidos no está vacío, se coloca por defecto el primer ítem
            self.combo_ped.insert(0, self.combo_ped["values"][0])
            self.combo_ped.config(state = "readonly")
        else:
            # Si una de las tablas está vacía, muestra error
            texto = "Debe haber registros en PEDIDO y PIZZA"
            messagebox.showerror("Problema de inserción", texto)
            # Destruye ventana
            self.insert_datos.destroy()

    def __llenar_combo_ped(self):
        opLCombo = "SELECT id_pedido FROM pedido"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo_piz(self):
        opLCombo = """SELECT id_piz, nom_piz, nom_tam FROM pizza JOIN tamano ON
        pizza.id_tam = tamano.id_tam """
        self.data = self.db.run_select(opLCombo)
        # Se muestra nombre de la pizza
        return [i[1:3] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
        btn_ok.place(x=100, y =160, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x=210, y =160, width = 80, height = 20)

    def __insertar(self):
        # Inserción de detalle
        sql = """INSERT detalle (id_pedido, id_piz, cantidad) VALUES (%(pedido)s,
        %(pizza)s, %(cantidad)s)"""

        # Se ejecuta consulta
        self.db.run_sql(sql, {"pedido": self.ids_ped[self.combo_ped.current()],
        "pizza": self.ids_piz[self.combo_piz.current()], "cantidad": self.cant.get()}, "I")

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
        self.insert_datos.geometry('300x200')
        self.insert_datos.title("Modificar detalle")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase detalle
        pedido_lab = tk.Label(self.insert_datos, text = "Pedido: ")
        pedido_lab.place(x = 10, y = 35, width = 120, height = 20)
        pizza_lab = tk.Label(self.insert_datos, text = "Pizza: ")
        pizza_lab.place(x = 10, y = 70, width = 120, height = 20)
        cant_lab = tk.Label(self.insert_datos, text = "Cantidad: ")
        cant_lab.place(x = 10, y = 105, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar detalles

        self.combo_ped = ttk.Combobox(self.insert_datos)
        self.combo_ped.place(x = 110, y = 35, width = 150, height= 20)
        self.combo_ped["values"], self.ids_ped = self.__llenar_combo_ped()

        # Combobox para elegir pizza
        self.combo_piz = ttk.Combobox(self.insert_datos)
        self.combo_piz.place(x = 110, y = 70, width = 150, height= 20)
        self.combo_piz["values"], self.ids_piz = self.__llenar_combo_piz()

        # Entrada de cantidad
        self.cant = tk.Entry(self.insert_datos)
        self.cant.place(x = 110, y = 105, width = 150, height = 20)

        # Se guardan valores actuales de las claves primarias
        self.ped_viejo = self.mod_select[0]
        self.piz_viejo = self.mod_select[1]

        # Se insertan datos actuales del registro de detalle
        self.combo_ped.insert(0, self.mod_select[0])
        self.combo_ped.config(state = "readonly")
        self.combo_piz.insert(0, self.mod_select[2:4])
        self.combo_piz.config(state = "readonly")
        self.cant.insert(0, self.mod_select[4])

    def __llenar_combo_ped(self):
        opLCombo = "SELECT id_pedido FROM pedido"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo_piz(self):
        opLCombo = """SELECT id_piz, nom_piz, nom_tam FROM pizza JOIN tamano ON
        pizza.id_tam = tamano.id_tam """
        self.data = self.db.run_select(opLCombo)
        # Se muestra nombre de la pizza
        return [i[1:3] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar el detalle
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 160, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 160, width = 80, height = 20)

    def __modificar(self):
        # Modificar registro
        opEdicion = """UPDATE detalle SET id_pedido = %(ped)s, id_piz = %(piz)s, cantidad = %(cant)s WHERE id_pedido = %(ped_viejo)s and id_piz = %(piz_viejo)s"""

        self.db.run_sql(opEdicion, {"ped": self.ids_ped[self.combo_ped.current()],
        "piz": self.ids_piz[self.combo_piz.current()], "cant": self.cant.get(),
        "ped_viejo": self.ped_viejo, "piz_viejo": self.piz_viejo}, "U")

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_detalle()
