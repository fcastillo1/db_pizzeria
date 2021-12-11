#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from tkinter import StringVar
from tkinter import OptionMenu

# Clase para realizar consulta dinámica con respecto al precio de las pizzas
class filtro_precio_pizza:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de la ventana
        self.root.geometry('300x270')
        # Se define el título de la ventana
        self.root.title("Filtrar pizzas por precio")
        # Se añade color al fondo de la ventana
        self.root.config(bg = "light cyan")
        # Esta opción permite cambiar el tamano de la venta
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Widgets a usar
        self.__config_button()
        self.__config_label()
        self.__config_entry()

    def __config_button(self):
        # Botón para realizar la consulta y generar tabla
        btn_ok = tk.Button(self.root, text = "Consultar",
            command = self.__query_dinamica, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Botón para cancelar la consulta
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __config_label(self):
        # Definición de entradas de texto
        precio_lab = tk.Label(self.root, text = "Precios: ", bg = "light cyan")
        precio_lab.place(x = 20, y = 10, width = 140, height = 20)

    def __config_entry(self):
        # Se establece el combobox para hacer el filtro por precios
        self.combo = ttk.Combobox(self.root)
        self.combo.place(x = 140, y = 10, width = 150, height= 20)
        self.combo["values"] = ["Menor a $5000", "Entre $5000 y $10000", "Más de $10.000"]
        # Se coloca por defecto primer ítem de combo
        self.combo.insert(0, self.combo["values"][0])
        self.combo.config(state = "readonly")

    def __query_dinamica(self):
        # Se obtiene el rango de precio elegido por el usuario en el combobox
        self.filtro = self.combo.current()

        # Se determina parte de la consulta a realizar en la tabla pizza
        if self.filtro == 0:
            op = "< '5000'"
        elif self.filtro == 1:
            op = ">= '5000' and precio_piz <= '10000'"
        elif self.filtro == 2:
            op = "> '10000'"

        sql = """SELECT id_piz, nom_piz, nom_tam, precio_piz FROM pizza JOIN tamano
        ON pizza.id_tam = tamano.id_tam WHERE precio_piz %s""" % op

        # Se obtienen resultados de la consulta
        mod_select = self.db.run_select(sql)

        if(mod_select) != []:
            # Se pasa como parámetro todo el resultado del sql
            select_pizza(self.db, mod_select)
        else:
            # No hay pizzas dentro del rango pedido
            texto = "¿Desea intentar con otra opción?"
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

class select_pizza:
    def __init__(self, db, mod_select):
        self.db = db
        self.data = []
        self.mod_select = mod_select

        # Ventana emergente
        self.tabla = tk.Toplevel()

        # Ajustes de ventana
        self.tabla.geometry('500x300')
        texto_titulo = "Pizzas"
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

        #  Configuración del treeview
        self.__config_treeview_filtro()

    def __config_treeview_filtro(self):
        self.treeview = ttk.Treeview(self.tabla)
        # Configuración de títulos de columnas
        self.treeview.configure(show = "headings", columns = ("id_piz", "nom_piz", "nom_tam", "precio_piz"))
        self.treeview.heading("id_piz", text = "ID")
        self.treeview.heading("nom_piz", text = "Nombre")
        self.treeview.heading("nom_tam", text = "Tamaño")
        self.treeview.heading("precio_piz", text = "Precio")

        # Configuración de tamaños de cada columna
        self.treeview.column("id_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_tam", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("precio_piz", minwidth = 150, width = 150, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 850)

        # Llenado del treeview
        self.llenar_treeview_filtro()
        self.tabla.after(0, self.llenar_treeview_filtro)

    def llenar_treeview_filtro(self):
        # Se actualiza data con el resultado de la query dinámica
        data = self.mod_select

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:4])

            self.data = data
