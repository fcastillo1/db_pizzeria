#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Se importan las librerias que son necesarias para las graficas en histograma
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Se crea una clase de histograma
class histograma:
    def __init__(self, root, db):
        # se define el root y la base de datos
        self.root = root
        self.db = db
        # se define la ventana que mostrara el histograma
        self.graph = tk.Toplevel()
        # se define el tamano de la ventana
        self.graph.geometry('600x400')
        # se define el nombre de la ventana
        self.graph.title("Histograma")

        # se llama a la funcion que permite la configuracion de la grafica
        self.__config_grafica()

    # Se define la funcion de la configuracion de grafica
    def __config_grafica(self):
        # se define la figura que hara el plot
        figura_canva, ax = plot.subplots()
        # el eje x e y se obtendra de la funcion que obtiene el data
        x, y = self.__obtencion_datos()
        # se define el titulo del plot (histograma)
        plot.title("Histograma tipos de pizza - matplotlib")
        # se define el nombre del eje X
        plot.xlabel("Tipos de Pizza")
        # se define el nombre del eje Y
        plot.ylabel("Count Tamano")
        # se define el color de las barras en este caso sera cyan
        plot.bar(x, y, color = "cyan")
        # para el canva se definen parametros visuales de la grafica
        canvas = tk.Canvas(self.graph, width=600, height=500, background="white")
        # la figura del canva generara la grafica
        canvas = FigureCanvasTkAgg(figura_canva, master = self.graph)
        # se procede al dibujo del canva
        canvas.draw()
        # se procede a generar el widget del canva que puede incluir cambios graficos, se añade el pack (ubicacion)
        canvas.get_tk_widget().pack()



# se crea una funcion que permite obtener los datos desde sql
    def __obtencion_datos(self):
        # se añade el comando desde sql que nos permite obtener el nombre de la pizza y graficar segun un count del tamano
        sql = """SELECT pizza.nom_piz, COUNT(tamano.id_tam) FROM pizza
                JOIN tamano ON tamano.id_tam = pizza.id_tam
                GROUP BY pizza.nom_piz;"""
        # se correra el sql que inicie
        data = self.db.run_select(sql)
        # el eje X tomara el dato de la primera (0) posicion
        x = [i[0] for i in data]
        # el eje Y tomara el dato de la segunda (1) posicion
        y = [i[1] for i in data]
        return x, y
