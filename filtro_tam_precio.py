#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Se importan las librerías que son necesarias para las gráficas en histograma
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class filtro_tam_precio:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamaño de la ventana
        self.root.geometry('320x270')
        # Se define el título de la ventana
        self.root.title("Filtrar tamaño")
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
        # Instrucción de selección de repartidor para el usuario
        etiqueta = tk.Label(self.root, text = "Seleccione un tamaño:", bg = "light cyan")
        etiqueta.place(x = 40, y = 10, width = 160, height = 20)

    def __config_entry(self):
        # Combobox para seleccionar el tamano
        self.combo = ttk.Combobox(self.root)
        self.combo.place(x = 90, y = 60, width = 150, height= 20)

        # Recepción de columna nombre e ids de tabla tamano
        self.combo["values"], self.ids = self.__llenar_combo_tamano()

        # Validación de combobox
        if self.ids != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla tipo
            texto = "Ingresar registros en TAMANO"
            messagebox.showwarning("Listado vacío", texto)
            # Destruye ventana
            self.root.destroy()

    def __llenar_combo_tamano(self):
        # Consulta para obtener detalles del combo
        opLCombo = "SELECT id_tam, nom_tam FROM tamano"
        self.data = self.db.run_select(opLCombo)

        # Se retorna nombre del tamano y el id correspondiente
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __query_dinamica(self):
        sql = """SELECT id_piz, precio_piz FROM pizza JOIN tamano ON
        tamano.id_tam = pizza.id_tam WHERE tamano.id_tam = %(id)s;"""

        # Se obtienen resultados de la consulta
        tamano = self.db.run_select_filter(sql, {"id": self.ids[self.combo.current()]})

        if(tamano) != []:
            # Se pasa como parámetro todo el resultado del sql
            select_tamano(self.db, tamano)
        else:
            # No hay pizzas registradas para el tamaño
            texto = "¿Desea intentar con otra opción?"
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

class select_tamano:
    def __init__(self, db, tamano):
        self.db = db
        self.data = []
        self.tamano = tamano

        # Se define la ventana que muestra el histograma
        self.graph = tk.Toplevel()
        # Se define el tamaño de la ventana
        self.graph.geometry('600x400')
        # Se define el nombre de la ventana
        self.graph.title("Histograma")

        # Se llama a la función que permite la configuración de la gráfica
        self.__config_grafica()

    # Se define la función de la configuración de gráfica
    def __config_grafica(self):
        # Se define la figura que hara el plot
        figura_canva, ax = plot.subplots()
        # El eje x e y se obtiene de la función que obtiene el data

        # Id_piz y el precio correspondiente obtenidos para el tamaño especificado
        pizza_precios = self.tamano

        # Se cuenta la frecuencia de cada precio
        data = Counter(i[1] for i in pizza_precios)

        # Data para crear el histograma
        # Eje x corresponde a precios
        x = ['$' + str(i) for i in data.keys()]
        # Eje y corresponde a la cantidad de pizzas que hay para el tamaño
        y = data.values()

        plot.title("Histograma tamaños de pizza - matplotlib")
        # Se define el nombre del eje X
        plot.xlabel("Precios")
        # Se define el nombre del eje Y
        plot.ylabel("Cantidad de pizzas")
        # Se define el color de las barras
        plot.bar(x, y, color = "cyan", alpha = 0.5)
        # Para el canva se definen parámetros visuales de la gráfica
        canvas = tk.Canvas(self.graph, width=600, height=500, background="white")
        # La figura del canva genera la gráfica
        canvas = FigureCanvasTkAgg(figura_canva, master = self.graph)
        # se procede al dibujo del canva
        canvas.draw()
        # se procede a generar el widget del canva que puede incluir cambios graficos, se añade el pack (ubicacion)
        canvas.get_tk_widget().pack()
