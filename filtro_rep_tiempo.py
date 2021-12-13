#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Librerías para pie chart
from tkinter import *
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from tkinter import IntVar

# Clase para realizar consulta dinámica con respecto al rut del repartidor
class filtro_rep_tiempo:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de la ventana
        self.root.geometry('320x230')
        # Se define el título de la ventana
        self.root.title("Tiempo de entrega según repartidor")
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
        btn_ok.place(x = 50, y = 180, width = 80, height = 20)

        # Botón para cancelar la consulta
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 170, y = 180, width = 80, height = 20)

    def __config_label(self):
        # Instrucción de selección de repartidor para el usuario
        etiqueta = tk.Label(self.root, text = "Seleccione un repartidor:", bg = "light cyan")
        etiqueta.place(x = 40, y = 25, width = 160, height = 20)

        # Selección de análisis por ciudad o en general
        etiqueta = tk.Label(self.root, text = "Seleccione una opción:", bg = "light cyan")
        etiqueta.place(x = 35, y = 80, width = 160, height = 20)

    def __config_entry(self):
        # Combobox para seleccionar el repartidor
        self.combo_rep = ttk.Combobox(self.root)
        self.combo_rep.place(x = 40, y = 50, width = 150, height= 20)

        # Recepción de columna nombre e ids de tabla tipo
        self.combo_rep["values"], self.ids_rep = self.__llenar_combo_rep()

        self.var =IntVar()

        # Ajustes radiobutton1 de selección de una ciudad
        self.r1 = tk.Radiobutton(self.root, highlightthickness=0, bd = 0, bg ="light cyan", variable=self.var, text = "Por ciudad:", value = 1)
        self.r1.place(x = 40, y = 105)

        # Combobox de ciudades ingresadas
        self.combo_ciudad = ttk.Combobox(self.root)
        self.combo_ciudad.place(x = 145, y = 105, width = 150, height= 20)

        # Recepción de ciudades e ids correspondientes
        self.combo_ciudad["values"], self.ids_ciudad = self.__llenar_combo_ciudad()

        # Ajustes radiobbutton2 general
        self.r2 = tk.Radiobutton(self.root, highlightthickness=0, bd = 0, bg = "light cyan", variable=self.var, text = "Ver general", value = 2)
        self.r2.place(x = 40, y = 140)

        # Validación de combobox ciudad
        if self.ids_ciudad != []:
            # Se coloca por defecto el primer ítem
            self.combo_ciudad.insert(0, self.combo_ciudad["values"][0])
            self.combo_ciudad.config(state = "readonly")

        # Validación de combobox de repartidor
        if self.ids_rep != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo_rep.insert(0, self.combo_rep["values"][0])
            self.combo_rep.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla repartidor
            texto = "Ingresar registros en REPARTIDOR"
            messagebox.showwarning("Listado vacío", texto)
            # Destruye ventana
            self.root.destroy()


    def valida_filtro(self):
        # Se obtiene opción elegido por el usuario
        self.opcion = self.var.get()

        # Se obtiene id del repartidor seleccionado en el combobox
        self.rep = self.ids_rep[self.combo_rep.current()]

        # Análisis por ciudad r1
        if self.opcion == 1:
            # Consulta si hay registros en ciudad
            if self.ids_ciudad != []:
                # Recibe id de ciudad elegida
                ciudad = self.ids_ciudad[self.combo_ciudad.current()]
                # Llamar a método filtrando por repartidor y ciudad
                filtro = "repartidor.rut_rep = '%s' and ciudad.id_ciudad = %d" % (self.rep, ciudad)
                self.__query_dinamica(filtro)

            # No hay registros en ciudad
            else:
                # Advierte que no hay registros en la tabla ciudad
                texto = "Ingresar registros en CIUDAD"
                messagebox.showwarning("Listado vacío", texto)
                # Destruye ventana
                self.root.destroy()

        # Análisis general r2
        elif self.opcion == 2:
            # Filtra solo por repartidor
            filtro = "repartidor.rut_rep = '%s'" % (self.rep)
            self.__query_dinamica(filtro)

        else:
            # No selección
            texto_error = "No se ha seleccionado opción."
            messagebox.showerror(message = texto_error, title = "Error")

    def __llenar_combo_ciudad(self):
        opLCombo = "SELECT id_ciudad, nom_ciudad FROM ciudad"
        self.data = self.db.run_select(opLCombo)
        # Retorna nombre de ciudad e id
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __llenar_combo_rep(self):
        # Consulta a tabla repartidor para obtener detalles del combo
        opLCombo = "SELECT rut_rep, nom_rep, ape_rep FROM repartidor"
        self.data = self.db.run_select(opLCombo)

        # Se retorna nombre y apellido del repartidor, y el id
        return [i[1:3] for i in self.data], [i[0] for i in self.data]

    def __query_dinamica(self, filtro):
        # Consulta obtiene id_pedido y tiempo de entrega en horas para un
        # repartidor escogido por el usuario
        sql = """SELECT repartidor.rut_rep, timestampdiff(hour, fecha_pedido, fecha_reparto)
        FROM repartidor JOIN pedido ON repartidor.rut_rep = pedido.rut_rep JOIN cliente ON
        pedido.rut_clie = cliente.rut_clie JOIN ciudad ON cliente.id_ciudad = ciudad.id_ciudad WHERE %s""" % filtro

        # Se obtienen resultados de la consulta
        seleccion = self.db.run_select(sql)

        # Se obtienen resultados
        if(seleccion) != []:
            # Se pasa como parámetro todo el resultado del sql
            select_rep(self.db, seleccion)
        else:
            # El repartidor no ha participado en ningún pedido
            texto = "¿Desea intentar con otra opción?"
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

class select_rep:
    def __init__(self, db, seleccion):
        self.db = db
        self.data = []
        self.seleccion = seleccion

        # Ventana emergente
        self.ventana= tk.Toplevel()
        self.ventana.geometry("700x500")
        self.ventana.title("Cantidad de horas por pedido")
        self.ventana.config(bg = "white")

        self.__grafica()
        self.__config_button()

    def __grafica(self):
        # Cuenta las ocurrencias de cada hora y genera diccionario donde la llave
        # corresponde a la cantidad de horas y el valor al n° de pedidos que se han
        # demorado ese tiempo en entregar
        data = Counter(i[1] for i in self.seleccion)

        # Plot
        fig = plt.figure(figsize = (6, 6), dpi = 100)
        fig.set_size_inches(6, 4)

        # Data para crear el pie
        horas = data.keys()
        num_pedidos = data.values()

        texto = "Total de pedido(s): %s" % str(len(num_pedidos))
        titulo = tk.Label(self.ventana, text = texto, bg = "white")
        titulo.place(x = 40, y = 10)

        # Agrega texto a etiquetas para especificar que son horas
        etiqueta_horas = [None] * len(horas)
        contador = 0;

        for i in horas:
            if i == 1:
                etiqueta_horas[contador] = str(i) + " hora"
            else:
                etiqueta_horas[contador] = str(i) + " horas"
            contador = contador + 1;

        # Plot pie chart
        plt.pie(num_pedidos, labels = etiqueta_horas, autopct = '%1.1f%%')

        # Crea círculo
        plt.axis('equal')

        canvasbar = FigureCanvasTkAgg(fig, master = self.ventana)
        canvasbar.draw()
        canvasbar.get_tk_widget().place(x = 0, y = 40)

    def __config_button(self):
        boton_salir = Button(self.ventana, text = "Salir", command = self.ventana.destroy,
        width = 25, bg='green', fg='white').place(x = 210, y = 450)
