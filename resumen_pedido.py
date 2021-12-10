#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
# from tkinter import Message
# from tkinter import filedialog

# Se define la clase de ayuda que mostrará un texto que puede ser útil para el usuario
class resumen_pedido:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('300x270')
        # Se define el título de la ventana
        self.root.title("PIZZAS POR PEDIDO")
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
        pedido_lab = tk.Label(self.root, text = "Pedido: ", bg = "light cyan")
        pedido_lab.place(x = 10, y = 35, width = 140, height = 20)

    def __config_entry(self):
        self.combo = ttk.Combobox(self.root)
        self.combo.place(x = 110, y = 35, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo_ped()

    def __llenar_combo_ped(self):
        opLCombo = "SELECT id_pedido FROM pedido"
        self.data = self.db.run_select(opLCombo)
        # Se muestra nom_tipo
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        btn_ok = tk.Button(self.root, text = "Generar",
            command = self.__generar_vista, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __generar_vista(self):
        sql = """CREATE OR REPLACE VIEW resumen_pedido AS select nom_piz, nom_tam,
        cantidad, detalle.precio_piz from detalle join pizza on
        detalle.id_piz = pizza.id_piz join tamano on pizza.id_tam = tamano.id_tam
        where id_pedido = %(id)s; """

        self.db.run_sql_vista(sql, {"id": self.ids[self.combo.current()]})

        imprimir_resumen_pedido(self.db, self.ids[self.combo.current()])

class imprimir_resumen_pedido:
    def __init__(self, db, pedido):
        self.db = db
        self.data = []
        self.pedido = pedido

        # Ventana emergente
        self.tabla = tk.Toplevel()

        # Funcionalidades
        self.__config_window()
        self.__config_treeview_vista()

        # Visualización de pizzas para cada pedido
        self.llenar_treeview_vista()

    def __config_window(self):
        # Ajustes de ventana
        self.tabla.geometry('500x300')
        texto_titulo = "Listado de PIZZAS en PEDIDO " + str(self.pedido)
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

    def __config_treeview_vista(self):
        self.treeview = ttk.Treeview(self.tabla)
        self.treeview.configure(show = "headings", columns = ("nom_piz", "nom_tam", "cantidad", "precio_piz"))
        self.treeview.heading("nom_piz", text = "Pizza")
        self.treeview.heading("nom_tam", text = "Tamaño")
        self.treeview.heading("cantidad", text = "Cantidad")
        self.treeview.heading("precio_piz", text = "Precio unitario")

        self.treeview.column("nom_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_tam", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("cantidad", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("precio_piz", minwidth = 150, width = 150, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 850)
        # Llenado del treeview
        self.llenar_treeview_vista()
        self.tabla.after(0, self.llenar_treeview_vista)

    def llenar_treeview_vista(self):
        # Se obtienen vehículos ingresadas
        opTreeview = """SELECT nom_piz, nom_tam, cantidad, precio_piz FROM resumen_pedido;"""

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
