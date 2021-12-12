#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from tkinter import IntVar

# Clase para realizar consulta dinámica con respecto al nombre de clientes
class filtro_nombre_cliente:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de la ventana
        self.root.geometry('300x200')
        # Se define el título de la ventana
        self.root.title("Filtrar clientes por nombre")
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
            command = self.valida_filtro, bg = 'green', fg = 'white')
        btn_ok.place(x = 50, y = 160, width = 80, height = 20)

        # Botón para cancelar la consulta
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 170, y = 160, width = 80, height = 20)

    def __config_label(self):
        # Instrucción para el usuario
        etiqueta = tk.Label(self.root, text = "Seleccione una opción:", bg = "light cyan")
        etiqueta.place(x = 40, y = 10, width = 160, height = 20)

    def __config_entry(self):
        self.var =IntVar()
        # Recibe filtro por nombre
        self.nom = tk.Entry(self.root)
        self.nom.place(x = 130, y = 50, width = 150, height = 20)
        # Ajustes radiobutton
        self.r1 = tk.Radiobutton(self.root, highlightthickness=0, bd = 0, bg ="light cyan", fg="blue", variable=self.var, text = "Nombre:", value = 1)
        self.r1.place(x = 30, y = 50)

        # Recibe filtro por apellido
        self.ape = tk.Entry(self.root)
        self.ape.place(x = 130, y = 100, width = 150, height = 20)
        # Ajustes radiobbutton
        self.r2 = tk.Radiobutton(self.root, highlightthickness=0, bd = 0, bg ="light cyan", fg="blue", variable=self.var, text = "Apellido:", value = 2)
        self.r2.place(x = 30, y = 100)

    def valida_filtro(self):
        # Se obtiene tipo de búsqueda elegida
        self.filtro = self.var.get()

        # Se determina parte de la consulta a realizar en la tabla cliente
        if self.filtro == 1:
            # Verifica contenido de string
            if self.nom.get() != "":
                filtro = "nom_clie like '%" + self.nom.get() + "%'"
                self.__query_dinamica(filtro)
            else:
                # String vacío
                texto_error = "Campo NOMBRE vacío."
                messagebox.showerror(message = texto_error, title = "Error")

        elif self.filtro == 2:
            # Verifica contenido de string
            if self.ape.get() != "":
                filtro = "ape_clie like '%" + self.ape.get() + "%'"
                self.__query_dinamica(filtro)
            else:
                # String vacío
                texto_error = "Campo APELLIDO vacío."
                messagebox.showerror(message = texto_error, title = "Error")
        else:
            # No selección
            texto_error = "No ha seleccionado ninguna opción."
            messagebox.showerror(message = texto_error, title = "Error")

    def __query_dinamica(self, op):
        sql = """SELECT rut_clie, nom_clie, ape_clie, tel_clie, dir_clie,
        nom_ciudad FROM cliente JOIN ciudad on cliente.id_ciudad = ciudad.id_ciudad
        WHERE %s """ % op

        # Se obtienen resultados de la consulta
        mod_select = self.db.run_select(sql)

        if(mod_select) != []:
            # Se pasa como parámetro todo el resultado del sql
            select_cliente(self.db, mod_select)
        else:
            # No hay pizzas dentro del rango pedido
            texto = "¿Desea intentar con otra opción?"
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

class select_cliente:
    def __init__(self, db, mod_select):
        self.db = db
        self.data = []
        self.mod_select = mod_select

        # Ventana emergente
        self.tabla = tk.Toplevel()

        # Ajustes de ventana
        self.tabla.geometry('500x300')
        texto_titulo = "Clientes"
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

        #  Configuración del treeview
        self.__config_treeview_filtro()

    def __config_treeview_filtro(self):
        self.treeview = ttk.Treeview(self.tabla)
        # Configuración de títulos de columnas
        self.treeview.configure(show = "headings", columns = ("rut_clie", "nom_clie",
        "ape_clie", "tel_clie", "dir_clie", "nom_ciudad"))
        self.treeview.heading("rut_clie", text = "Rut")
        self.treeview.heading("nom_clie", text = "Nombre")
        self.treeview.heading("ape_clie", text = "Apellido")
        self.treeview.heading("tel_clie", text = "Teléfono")
        self.treeview.heading("dir_clie", text = "Teléfono")
        self.treeview.heading("nom_ciudad", text = "Ciudad")

        # Configuración de tamaños de cada columna
        self.treeview.column("rut_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("ape_clie", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("tel_clie", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("dir_clie", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("nom_ciudad", minwidth = 150, width = 150, stretch = False)

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
