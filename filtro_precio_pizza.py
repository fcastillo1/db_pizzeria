#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from tkinter import IntVar

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
            command = self.valida_filtro, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Botón para cancelar la consulta
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __config_label(self):
        # Definición de entradas de texto
        precio_lab = tk.Label(self.root, text = "Seleccione una opción:", bg = "light cyan")
        precio_lab.place(x = 40, y = 10, width = 160, height = 20)


    def __config_entry(self):
        self.var =IntVar()
        # Recibe filtro menor o igual a
        self.num1 = tk.Entry(self.root)
        self.num1.place(x = 180, y = 40, width = 60, height = 20)
        # Ajustes radiobutton
        self.r1 = tk.Radiobutton(self.root, highlightthickness=0, bd = 0, bg ="light cyan", variable=self.var, text = "Menor o igual a:", value = 1)
        self.r1.place(x = 40, y = 40)

        # Recibe filtro menor o igual a
        self.num2 = tk.Entry(self.root)
        self.num2.place(x = 180, y = 80, width = 60, height = 20)
        # Ajustes radiobbutton
        self.r2 = tk.Radiobutton(self.root, highlightthickness=0, bd = 0, bg ="light cyan", variable=self.var, text = "Mayor o igual a:", value = 2)
        self.r2.place(x = 40, y = 80)

    def transforma_int(self, valor):
        # Intenta transformar a int
        try:
            valor = int(valor)
            # Retorna true y nuevo valor
            return valor

        except ValueError as err:
            return False

    def valida_filtro(self):
        # Se obtiene el rango de precio elegido por el usuario en el combobox
        self.filtro = self.var.get()

        # Se determina parte de la consulta a realizar en la tabla pizza
        if self.filtro == 1:
            # Recibe bandera e int
            numero = self.transforma_int(self.num1.get())
            if numero != False:
                print("ahahah")
                op = "<= '%d'" % (numero)
                # Llama método con parámetro del where
                self.__query_dinamica(op)
            else:
                # Error de transformación a int
                texto_error = "Valor ingresado no es correcto."
                messagebox.showerror(message = texto_error, title = "Error")

        elif self.filtro == 2:
            # Recibe bandera e int
            numero = self.transforma_int(self.num2.get())
            if numero != False:
                op = ">= '%d'" % (numero)
                # Llama método con parámetro del where
                self.__query_dinamica(op)
            else:
                # Error de transformación a int
                texto_error = "Valor ingresado no es correcto."
                messagebox.showerror(message = texto_error, title = "Error")
        else:
            # No selección
            texto_error = "No se ha seleccionado opción."
            messagebox.showerror(message = texto_error, title = "Error")

    def __query_dinamica(self, op):

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
