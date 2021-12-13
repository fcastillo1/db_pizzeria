#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox

# Se define la clase resumen_pedido
class resumen_pedido:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('270x185')
        # Se define el título de la ventana
        self.root.title("PIZZAS POR PEDIDO")
        # Se añade color al fondo de la ventana
        self.root.config(bg="light cyan")
        # Esta opción permite cambiar el tamano de la venta según las necesidades del usuario
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Configuraciones de widgets en ventana
        self.__config_button()
        self.__config_label()
        self.__config_entry()

    def __config_button(self):
        btn_ok = tk.Button(self.root, text = "Generar",
            command = self.__query_dinamica, bg = 'green', fg = 'white')
        btn_ok.place(x = 40, y = 140, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 160, y = 140, width = 80, height = 20)

    def __config_label(self):
        # Definición de entradas de texto
        pedido_lab = tk.Label(self.root, text = "Pedido: ", bg = "light cyan")
        pedido_lab.place(x = 5, y = 60, width = 105, height = 20)

    def __config_entry(self):
        # Combobox para seleccionar el pedido
        self.combo = ttk.Combobox(self.root)
        self.combo.place(x = 90, y = 60, width = 150, height= 20)
        # Recepción de columna con ids de tabla pedido
        self.combo["values"], self.ids = self.__llenar_combo_pedido()

        # Validación de combobox
        if self.ids != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla pedido
            texto = "Ingresar registros en PEDIDO"
            messagebox.showwarning("Listado vacío", texto)
            # Destruye ventana
            self.root.destroy()

    def __llenar_combo_pedido(self):
        # Consulta para obtener detalles del combo
        opLCombo = "SELECT id_pedido FROM pedido"
        self.data = self.db.run_select(opLCombo)
        # Retorna ids de pedidos
        return [i[0] for i in self.data], [i[0] for i in self.data]

    def __query_dinamica(self):
        sql = """SELECT nom_piz, nom_tam, cantidad, detalle.precio_piz FROM detalle JOIN pizza ON
        detalle.id_piz = pizza.id_piz JOIN tamano ON pizza.id_tam = tamano.id_tam
        WHERE id_pedido = %(pedido)s"""

        # Se obtienen resultados de la consulta
        mod_select = self.db.run_select_filter(sql, {"pedido": self.ids[self.combo.current()]})

        if(mod_select) != []:
            # Se pasa como parámetro todo el resultado del sql
            select_resumen_pedido(self.db, mod_select)
        else:
            # No hay pizzas registradas para el pedido
            texto = "¿Desea intentar con otra opción?"
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

class select_resumen_pedido:
    def __init__(self, db, pedido):
        self.db = db
        self.data = []
        self.mod_select = pedido

        # Ventana emergente
        self.tabla = tk.Toplevel()
        self.tabla.geometry('500x300')
        texto_titulo = "Listado de PIZZAS"
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

        self.__config_treeview_filtro()
        self.__crear_botones_resumen_pedido()

    def __config_treeview_filtro(self):
        self.treeview = ttk.Treeview(self.tabla)
        # Configuración de nombres de cada columna
        self.treeview.configure(show = "headings", columns = ("nom_piz", "nom_tam", "cantidad", "precio_piz"))
        self.treeview.heading("nom_piz", text = "Pizza")
        self.treeview.heading("nom_tam", text = "Tamaño")
        self.treeview.heading("cantidad", text = "Cantidad")
        self.treeview.heading("precio_piz", text = "Precio unitario")

        # Configuración de tamaños de cada columna
        self.treeview.column("nom_piz", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_tam", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("cantidad", minwidth = 150, width = 150, stretch = False)
        self.treeview.column("precio_piz", minwidth = 150, width = 150, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 850)
        # Llenado del treeview
        self.llenar_treeview_filtro()
        self.tabla.after(0, self.llenar_treeview_filtro)

    def llenar_treeview_filtro(self):
        # Guarda info obtenida tras la consulta
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

    def __crear_botones_resumen_pedido(self):
        b4 = tk.Button(self.tabla, text = "Aceptar", bg='green', fg='white',
            command=self.tabla.destroy)
        b4.place(x = 150, y = 245, width = 200, height = 40)
