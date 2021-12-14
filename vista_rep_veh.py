#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox

# Se define la clase de  vista_rep_veh que permite visualizar  el nombre y apellido
# del repartidor que usa un determinado vehículo para un pedido
class vista_rep_veh:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('800x400')
        # Se define el título de la ventana
        self.root.title("REPARTIDOR CON VEHÍCULO")
        # Se añade color al fondo de la ventana
        self.root.config(bg = "light cyan")
        # Esta opción permite cambiar el tamano de la ventana
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Creación de la vista
        self.__generar_vista()

        # Visualización de repartidores y vehiculos
        self.__config_treeview_vista()

        # Se crean los botones
        self.__crear_botones_vista()

    def __generar_vista(self):
        # SQL para generar una vista con id de pedido, datos del repartidor (rut,
        # nombre y teléfono), id del vehículo y patente del mismo
        sql = """CREATE OR REPLACE VIEW lista_rep_veh AS SELECT id_pedido, pedido.rut_rep,
        nom_rep, ape_rep, pedido.id_veh, patente FROM pedido JOIN repartidor ON
        pedido.rut_rep = repartidor.rut_rep JOIN vehiculo ON pedido.id_veh = vehiculo.id_veh;"""

        # Se ejecuta la sql en la base de datos
        self.db.run_sql_vista(sql)

    def __config_treeview_vista(self):
        # Se crea el treeview que permite visualizar la view
        self.treeview = ttk.Treeview(self.root)
        # Se definen las columnas del treeview
        self.treeview.configure(show = "headings", columns = ("id_pedido", "rut_rep", "nom_rep",
        "ape_rep", "id_veh", "patente"))

        # Cada columna toma un nombre representativo
        self.treeview.heading("id_pedido", text = "Pedido")
        self.treeview.heading("rut_rep", text = "Rut repartidor")
        self.treeview.heading("nom_rep", text = "Nombre repartidor")
        self.treeview.heading("ape_rep", text = "Apellido repartidor")
        self.treeview.heading("id_veh", text = "Vehículo")
        self.treeview.heading("patente", text = "Patente")

        # Ajustes de ancho de columna
        self.treeview.column("id_pedido", minwidth = 50, width = 100, stretch = False)
        self.treeview.column("rut_rep", minwidth = 100, width = 150, stretch = False)
        self.treeview.column("nom_rep", minwidth = 100, width = 150, stretch = False)
        self.treeview.column("ape_rep", minwidth = 100, width = 150, stretch = False)
        self.treeview.column("id_veh", minwidth = 50, width = 100, stretch = False)
        self.treeview.column("patente", minwidth = 50, width = 150, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 400, width = 800)

        # Llenado del treeview
        self.llenar_treeview_vista()
        self.root.after(0, self.llenar_treeview_vista)

    def llenar_treeview_vista(self):
        # Se obtienen registros ingresados donde estará el pedido, repartidor y vehículo
        sql = """SELECT id_pedido, rut_rep, nom_rep, ape_rep, id_veh, patente FROM lista_rep_veh"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(sql)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:6])

            self.data = data

    def __crear_botones_vista(self):
        # Creación de un botón para aceptar y salir de la vista
        btn_ok = tk.Button(self.root, text = "Aceptar", bg='green', fg='white',
            command=self.root.destroy)
        # Configuraciones del botón sobre ubicación del botón y tamaño
        btn_ok.place(x = 290, y = 350, width = 200, height = 40)
