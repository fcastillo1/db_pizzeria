#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox

# Se define la clase de  vista_clie_ciudad que permite visualizar los detalles
# de un cliente para cada pedido
class vista_clie_ciudad:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('800x400')
        # Se define el título de la ventana
        self.root.title("CLIENTE CON CIUDAD")
        # Se añade color al fondo de la ventana
        self.root.config(bg = "light cyan")
        # Esta opción permite cambiar el tamano de la venta
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Crear vista
        self.__generar_vista()

        # Visualización de clientes y ciudades
        self.__config_treeview_vista()

        # Se crean los botones
        self.__crear_botones_vista()

    def __generar_vista(self):
        # SQL para generar una vista
        sql = """CREATE OR REPLACE VIEW lista_cliente_ciudad AS SELECT id_pedido,
        pedido.rut_clie, nom_clie, ape_clie, nom_ciudad FROM pedido JOIN cliente
        ON pedido.rut_clie = cliente.rut_clie JOIN ciudad ON cliente.id_ciudad = ciudad.id_ciudad;"""

        # Se ejecuta la consulta en la base de datos
        self.db.run_sql_vista(sql)

    def __config_treeview_vista(self):
        # Creación del treeview para visualizar la información de la nueva view
        self.treeview = ttk.Treeview(self.root)

        # Se determinan las columnas a mostrar
        self.treeview.configure(show = "headings", columns = ("id_pedido", "rut_clie", "nom_clie",
                                        "ape_clie", "nom_ciudad"))

        # Se asigna un nombre representativo para cada columna
        self.treeview.heading("id_pedido", text = "Pedido")
        self.treeview.heading("rut_clie", text = "Rut cliente")
        self.treeview.heading("nom_clie", text = "Nombre cliente")
        self.treeview.heading("ape_clie", text = "Apellido cliente")
        self.treeview.heading("nom_ciudad", text = "Ciudad")

        # Ajustes de tamaño para cada columna
        self.treeview.column("id_pedido", minwidth = 50, width = 160, stretch = False)
        self.treeview.column("rut_clie", minwidth = 100, width = 160, stretch = False)
        self.treeview.column("nom_clie", minwidth = 100, width = 160, stretch = False)
        self.treeview.column("ape_clie", minwidth = 100, width = 160, stretch = False)
        self.treeview.column("nom_ciudad", minwidth = 50, width = 160, stretch = False)
        # Configuraciones del treeview de tamaño y ubicación
        self.treeview.place(x = 0, y = 0, height = 400, width = 800)
        # Llenado del treeview
        self.llenar_treeview_vista()
        self.root.after(0, self.llenar_treeview_vista)

    def llenar_treeview_vista(self):
        # Se obtienen registros ingresados dond estará el pedido, cliente y ciudad
        sql = """SELECT id_pedido, rut_clie, nom_clie, ape_clie, nom_ciudad FROM lista_cliente_ciudad"""

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
        # Creación de un botón que permite salir de la vista
        btn_ok = tk.Button(self.root, text = "Aceptar", bg='green', fg='white',
            command=self.root.destroy)

        # Configuraciones del botón sobre ubicación del botón y tamaño
        btn_ok.place(x = 290, y = 350, width = 200, height = 40)
