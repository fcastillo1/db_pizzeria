#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
# from tkinter import Message
# from tkinter import filedialog

# Se define la clase de ayuda que mostrará un texto que puede ser útil para el usuario
class detalle_vehiculo:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('300x270')
        # Se define el título de la ventana
        self.root.title("DETALLE DE VEHÍCULO")
        # Se añade color al fondo de la ventana
        self.root.config(bg="light cyan")
        # Esta opción permite cambiar el tamano de la venta según las necesidades del usuario
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        self.__config_label()
        self.__config_entry()
        self.__config_button()

        self.root.mainloop()

    def __config_label(self):
        # Definición de entradas de texto
        pedido_lab = tk.Label(self.root, text = "Tipo: ", bg = "light cyan")
        pedido_lab.place(x = 10, y = 35, width = 140, height = 20)

    def __config_entry(self):
        self.combo = ttk.Combobox(self.root)
        self.combo.place(x = 110, y = 35, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo_tipo()

    def __llenar_combo_tipo(self):
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        btn_ok = tk.Button(self.root, text = "Generar",
            command = self.__generar_vista, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __generar_vista(self):
        sql = """CREATE OR REPLACE VIEW detalle_vehiculo AS select vehiculo.id_veh,
        patente, capacidad_tipo from tipo join vehiculo on tipo.id_tipo = vehiculo.id_tipo
        where tipo.id_tipo = %(id)s;"""

        self.db.run_sql_vista(sql, {"id": self.ids[self.combo.current()]})

        imprimir_detalle_vehiculo(self.db, self.combo["values"][self.combo.current()])

class imprimir_detalle_vehiculo:
    def __init__(self, db, tipo):
        self.db = db
        self.data = []
        self.tipo = tipo
        # Ventana emergente
        self.tabla = tk.Toplevel()

        # Funcionalidades
        self.__config_window()
        self.__config_treeview_vista()

        # Visualización de pizzas para cada pedido
        self.llenar_treeview_vista()

    def __config_window(self):
        # Ajustes de ventana
        self.tabla.geometry('500x250')
        texto_titulo = "Listado de VEHÍCULOS según TIPO " + str(self.tipo)
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

    def __config_treeview_vista(self):
        self.treeview = ttk.Treeview(self.tabla)
        self.treeview.configure(show = "headings", columns = ("id_veh", "patente", "capacidad_tipo"))
        self.treeview.heading("id_veh", text = "ID")
        self.treeview.heading("patente", text = "Patente")
        self.treeview.heading("capacidad_tipo", text = "Capacidad")

        self.treeview.column("id_veh", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("patente", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("capacidad_tipo", minwidth = 150, width = 100, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 850)
        # Llenado del treeview
        self.llenar_treeview_vista()
        self.tabla.after(0, self.llenar_treeview_vista)

    def llenar_treeview_vista(self):
        # Se obtienen vehículos ingresadas
        opTreeview = """select id_veh, patente, capacidad_tipo from detalle_vehiculo;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(opTreeview)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:5])

            self.data = data
