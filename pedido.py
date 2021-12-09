#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

from cliente import cliente
from repartidor import repartidor
from vehiculo import vehiculo

class pedido:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('850x400')
        self.root.title("Pedido")
        self.root.config(bg = "light cyan")
        self.root.resizable(width = 0, height = 0)

        # Ventana nueva
        self.root.transient(root)

        # Visualización de pizzas registradas en la base de datos
        self.__config_treeview_pedido()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_pedido()

    def __config_treeview_pedido(self):
        self.treeview = ttk.Treeview(self.root)
        self.treeview.configure(show = "headings", columns = ("id_pedido", "total_pedido", "fecha_pedido", "fecha_reparto", "rut_clie", "rut_rep", "id_veh"))
        self.treeview.heading("id_pedido", text = "ID")
        self.treeview.heading("total_pedido", text = "Total")
        self.treeview.heading("fecha_pedido", text = "Fecha Pedido")
        self.treeview.heading("fecha_reparto", text = "Fecha Reparto")
        self.treeview.heading("rut_clie", text = "Rut Cliente")
        self.treeview.heading("rut_rep", text = "Rut Repartidor")
        self.treeview.heading("id_veh", text = "Vehículo")

        self.treeview.column("id_pedido", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("total_pedido", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("fecha_pedido", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("fecha_reparto", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("rut_clie", minwidth = 150, width = 120, stretch = False)
        self.treeview.column("rut_rep", minwidth = 150, width = 120, stretch = False)
        self.treeview.column("id_veh", minwidth = 150, width = 105, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 850)
        # Llenado del treeview
        self.llenar_treeview_pedido()
        self.root.after(0, self.llenar_treeview_pedido)

    def __crear_botones_pedido(self):
        # Botón para insertar
        b1 = tk.Button(self.root, text = "Insertar pedido", bg = 'snow',
            fg = 'green', command = self.__insertar_pedido)
        b1.place(x = 0, y = 350, width = 225, height = 50)

        # Botón para modificar
        b2 = tk.Button(self.root, text = "Modificar pedido", bg = 'snow',
            fg = 'orange', command = self.__modificar_pedido)
        b2.place(x = 200, y = 350, width = 225, height = 50)

        # Botón para eliminar
        b3 = tk.Button(self.root, text = "Eliminar pedido", bg = 'snow',
            fg='red', command = self.__eliminar_pedido)
        b3.place(x = 400, y = 350, width = 225, height = 50)

        # Botón para salir
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy,
            bg = 'red', fg = 'white')
        b4.place(x = 625, y = 350, width = 225, height = 50)

    def llenar_treeview_pedido(self):
        # Se obtienen vehículos ingresadas
        opTreeview = """SELECT id_pedido, total_pedido, fecha_pedido, fecha_reparto,
        rut_clie, rut_rep, id_veh FROM pedido;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(opTreeview)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:7])

            self.data = data

    def __insertar_pedido(self):
        insertar_pedido(self.db, self)

    def __eliminar_pedido(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message = "¿Realmente quieres borrar el registro?", title = "Alerta")== True:
                opEliminar = "DELETE FROM pedido where id_pedido = %(id_pedido)s"
                self.db.run_sql(opEliminar, {"id_pedido": self.treeview.focus()})
                self.llenar_treeview_pedido()

    def __modificar_pedido(self):
        if(self.treeview.focus() != ""):
            if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
                opModificar = """SELECT id_pedido, total_pedido, fecha_pedido, fecha_reparto, rut_clie, rut_rep, id_veh FROM pedido WHERE id_pedido = %(id)s"""

                # Se consulta tabla pedido por el id del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"id": self.treeview.focus()})[0]
                modificar_pedido(self.db, self, mod_select)


    def __mostrar_detalle(self):
        detalle(self.root, self.db)

class insertar_pedido:
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        # Ventana emergente
        self.insert_datos = tk.Toplevel()

        # Funcionalidades
        #self.__calendar()
    #    self.__grad_date()
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __calendar(self):
        self.insert_datos.geometry("400x400")
        cal = Calendar(self.insert_datos, selectmode = 'day', year = 2020, month = 5)
        cal.pack(pady = 20)

    def __grad_date(self):
        date.config(text = "Selected Date is: " + cal.get_date())
        # Add Button and Label
        boton_calendar = tk.Button(self.insert_datos, text = "Get Date", command = self.__grad_date).pack(pady = 20)
        date = Label(self.insert_datos, text = "")
        date.pack(pady = 20)

        # Execute Tkinter
        #self.root.mainloop()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x270')
        self.insert_datos.title("Insertar pedido")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase pedido
        id_lab = tk.Label(self.insert_datos, text = "ID pedido: ")
        id_lab.place(x = 10, y = 30, width = 120, height = 20)
        fecha_pedido_lab = tk.Label(self.insert_datos, text = "Fecha pedido: ")
        fecha_pedido_lab.place(x = 5, y = 60, width = 120, height = 20)
        fecha_reparto_lab = tk.Label(self.insert_datos, text = "Fecha reparto: ")
        fecha_reparto_lab.place(x = 3, y = 90, width = 120, height = 20)
        cliente_lab = tk.Label(self.insert_datos, text = "Rut cliente: ")
        cliente_lab.place(x = 10, y = 120, width = 120, height = 20)
        repartidor_lab = tk.Label(self.insert_datos, text = "Rut repartidor:" )
        repartidor_lab.place(x = 1, y = 150, width = 120, height = 20)
        vehiculo_lab = tk.Label(self.insert_datos, text = "ID vehículo: ")
        vehiculo_lab.place(x = 10, y = 180, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar vehículos
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 30, width = 150, height = 20)
        self.fecha_pedido = tk.Entry(self.insert_datos)
        self.fecha_pedido.place(x = 110, y = 60, width = 150, height = 20)
        self.fecha_reparto = tk.Entry(self.insert_datos)
        self.fecha_reparto.place(x = 110, y = 90, width = 150, height = 20)
        self.cliente = tk.Entry(self.insert_datos)
        self.cliente.place(x = 110, y = 120, width = 150, height = 20)
        self.repartidor = tk.Entry(self.insert_datos)
        self.repartidor.place(x = 110, y = 150, width = 150, height = 20)
        self.vehiculo = tk.Entry(self.insert_datos)
        self.vehiculo.place(x = 110, y = 180, width = 150, height = 20)

        # Combobox para elegir id cliente
        self.combo_cliente = ttk.Combobox(self.insert_datos)
        self.combo_cliente.place(x = 110, y = 120, width = 150, height= 20)
        self.combo_cliente["values"], self.ids_clie = self.__llenar_combo1()

        # Combo repartidor
        self.combo_repartidor = ttk.Combobox(self.insert_datos)
        self.combo_repartidor.place(x = 110, y = 150, width = 150, height= 20)
        self.combo_repartidor["values"], self.ids_rep = self.__llenar_combo2()

        # Combo vehiculo
        self.combo_vehiculo = ttk.Combobox(self.insert_datos)
        self.combo_vehiculo.place(x = 110, y = 180, width = 150, height= 20)
        self.combo_vehiculo["values"], self.ids_veh = self.__llenar_combo3()

    def __llenar_combo1(self):
        opLCombo1 = "SELECT rut_clie FROM cliente"
        self.data = self.db.run_select(opLCombo1)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo2(self):
        opLCombo2 = "SELECT rut_rep FROM repartidor"
        self.data = self.db.run_select(opLCombo2)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo3(self):
        opLCombo3 = "SELECT id_veh FROM vehiculo"
        self.data = self.db.run_select(opLCombo3)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]


    def __config_button(self):
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __insertar(self):
        # Inserción en tabla vehichulo de la base de datos
        opInsert = """INSERT pedido (id_pedido, total_pedido, fecha_pedido, fecha_reparto, rut_clie, rut_rep, id_veh) values
            (%(id)s, 0, %(fecha_pedido)s, %(fecha_reparto)s, %(cliente)s, %(repartidor)s, %(vehiculo)s)"""

        # Se ejecuta consulta
        self.db.run_sql(opInsert, {"id": self.id.get(), "fecha_pedido": self.fecha_pedido.get(), "fecha_reparto": self.fecha_reparto.get(),
        "cliente": self.ids_clie[self.combo_cliente.current()], "repartidor": self.ids_rep[self.combo_repartidor.current()],
        "vehiculo": self.ids_veh[self.combo_vehiculo.current()]})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_pedido()

class modificar_pedido:
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
        self.insert_datos.geometry('300x270')
        self.insert_datos.title("Modificar pedido")
        self.insert_datos.resizable(width = 0, height = 0)

    def __config_label(self):
        # Definición de entradas de texto para la clase pedido
        id_lab = tk.Label(self.insert_datos, text = "ID pedido: ")
        id_lab.place(x = 10, y = 10, width = 120, height = 20)
        total_lab = tk.Label(self.insert_datos, text = "Total: ")
        total_lab.place(x = 10, y = 40, width = 120, height = 20)
        fecha_pedido_lab = tk.Label(self.insert_datos, text = "Fecha pedido: ")
        fecha_pedido_lab.place(x = 5, y = 70, width = 120, height = 20)
        fecha_reparto_lab = tk.Label(self.insert_datos, text = "Fecha reparto: ")
        fecha_reparto_lab.place(x = 3, y = 100, width = 120, height = 20)
        cliente_lab = tk.Label(self.insert_datos, text = "Rut cliente: ")
        cliente_lab.place(x = 10, y = 130, width = 120, height = 20)
        repartidor_lab = tk.Label(self.insert_datos, text = "Rut repartidor:" )
        repartidor_lab.place(x = 1, y = 160, width = 120, height = 20)
        vehiculo_lab = tk.Label(self.insert_datos, text = "ID vehículo: ")
        vehiculo_lab.place(x = 10, y = 190, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar pizzas
        self.id = tk.Entry(self.insert_datos)
        self.id.place(x = 110, y = 10, width = 150, height = 20)
        self.total = tk.Entry(self.insert_datos)
        self.total.place(x = 110, y = 40, width = 150, height = 20)
        self.fecha_pedido = tk.Entry(self.insert_datos)
        self.fecha_pedido.place(x = 110, y = 70, width = 150, height = 20)
        self.fecha_reparto = tk.Entry(self.insert_datos)
        self.fecha_reparto.place(x = 110, y = 100, width = 150, height = 20)
        self.cliente = tk.Entry(self.insert_datos)
        self.cliente.place(x = 110, y = 130, width = 150, height = 20)
        self.repartidor = tk.Entry(self.insert_datos)
        self.repartidor.place(x = 110, y = 160, width = 150, height = 20)
        self.vehiculo = tk.Entry(self.insert_datos)
        self.vehiculo.place(x = 110, y = 190, width = 150, height = 20)

        # Combobox para elegir id cliente
        self.combo_cliente = ttk.Combobox(self.insert_datos)
        self.combo_cliente.place(x = 110, y = 130, width = 150, height= 20)
        self.combo_cliente["values"], self.ids_clie = self.__llenar_combo1()

        # Combo repartidor
        self.combo_repartidor = ttk.Combobox(self.insert_datos)
        self.combo_repartidor.place(x = 110, y = 160, width = 150, height= 20)
        self.combo_repartidor["values"], self.ids_rep = self.__llenar_combo2()

        # Combo vehículo
        self.combo_vehiculo = ttk.Combobox(self.insert_datos)
        self.combo_vehiculo.place(x = 110, y = 190, width = 150, height= 20)
        self.combo_vehiculo["values"], self.ids_veh = self.__llenar_combo3()

        self.id_viejo = self.mod_select[0]
        # Se insertan valores actuales
        self.id.insert(0, self.mod_select[0])
        self.total.config(state = 'normal')
        self.total.insert(0, self.mod_select[1])
        self.total.config(state = 'disabled')
        self.fecha_pedido.insert(0, self.mod_select[2])
        self.fecha_reparto.insert(0, self.mod_select[3])
        self.combo_cliente.insert(0, self.mod_select[4])
        self.combo_repartidor.insert(0, self.mod_select[5])
        self.combo_vehiculo.insert(0, self.mod_select[6])

    def __llenar_combo1(self):
        opLCombo1 = "SELECT rut_clie FROM cliente"
        self.data = self.db.run_select(opLCombo1)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo2(self):
        opLCombo2 = "SELECT rut_rep FROM repartidor"
        self.data = self.db.run_select(opLCombo2)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo3(self):
        opLCombo3 = "SELECT id_veh FROM vehiculo"
        self.data = self.db.run_select(opLCombo3)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]


    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar pizza
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __modificar(self):
        opEdicion = """UPDATE pedido set id_pedido = %(id)s, total_pedido = %(total)s,
            fecha_pedido = %(fecha_pedido)s, fecha_reparto = %(fecha_reparto)s,
            rut_clie = %(cliente)s, rut_rep = %(repartidor)s, id_veh = %(vehiculo)s
            WHERE id_pedido = %(id_viejo)s"""

        self.db.run_sql(opEdicion, {"id": self.id.get(),"total": self.total.get(),
        "fecha_pedido": self.fecha_pedido.get(), "fecha_reparto": self.fecha_reparto.get(),
        "cliente": self.ids_clie[self.combo_cliente.current()], "repartidor": self.ids_rep[self.combo_repartidor.current()],
        "vehiculo": self.ids_veh[self.combo_vehiculo.current()], "id_viejo" : self.id_viejo})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_pedido()
