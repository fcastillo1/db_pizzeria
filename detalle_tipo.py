#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox

# Se define la clase de  detalle_tipo que permite
class detalle_tipo:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('300x270')
        # Se define el título de la ventana
        self.root.title("DETALLE DE TIPO")
        # Se añade color al fondo de la ventana
        self.root.config(bg = "light cyan")
        # Esta opción permite cambiar el tamano de la venta
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Configuraciones de widgets en ventana
        self.__config_button()
        self.__config_label()
        self.__config_entry()

    def __config_button(self):
        btn_ok = tk.Button(self.root, text = "Generar",
            command = self.__generar_vista, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 230, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        btn_cancel.place(x = 210, y = 230, width = 80, height = 20)

    def __config_label(self):
        # Definición de entradas de texto
        pedido_lab = tk.Label(self.root, text = "Tipo: ", bg = "light cyan")
        pedido_lab.place(x = 10, y = 35, width = 140, height = 20)

    def __config_entry(self):
        # Combobox para seleccionar el tipo
        self.combo = ttk.Combobox(self.root)
        self.combo.place(x = 110, y = 35, width = 150, height= 20)

        # Recepción de columna nombre e ids de tabla tipo
        self.combo["values"], self.ids = self.__llenar_combo_tipo()

        # Validación de combobox
        if self.validar_combo_tipo() == True:
            # Si está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla tipo
            texto = "Ingresar registros en TIPO"
            messagebox.showwarning("Listado vacío", texto)
            # Destruye ventana
            self.root.destroy()

    def validar_combo_tipo(self):
        # Si hay registros en tabla tipo, retorna true
        if self.ids != []:
            return True

    def __llenar_combo_tipo(self):
        # Consulta para obtener detalles del combo
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        self.data = self.db.run_select(opLCombo)

        # Se retorna nombre del timpo y el id correspondiente
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __generar_vista(self):
        # SQL para generar una vista
        sql = """CREATE OR REPLACE VIEW detalle_tipo AS SELECT vehiculo.id_veh,
        patente, capacidad_tipo FROM tipo JOIN vehiculo ON tipo.id_tipo = vehiculo.id_tipo
        WHERE tipo.id_tipo = %(id)s;"""

        self.db.run_sql_vista(sql, {"id": self.ids[self.combo.current()]})

        if self.validar_vista() == True:
            # Se pasa como parámetro el tipo seleccionado
            imprimir_detalle_tipo(self.db, self.combo["values"][self.combo.current()])

        else:
            # No hay registros en la tabla vehículo
            texto = "¿Desea intentar con otra opción?"
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

    def validar_vista(self):
        sql = "SELECT id_veh, patente, capacidad_tipo FROM detalle_tipo"
        select_vista = self.db.run_select(sql)

        if select_vista != []:
            return True

class imprimir_detalle_tipo:
    def __init__(self, db, tipo):
        self.db = db
        self.data = []

        # Tipo de vehículo escogido para mostrar
        self.tipo = tipo

        # Ventana emergente
        self.tabla = tk.Toplevel()

        # Ajustes de ventana
        self.tabla.geometry('500x250')
        texto_titulo = "Listado de VEHÍCULOS según TIPO " + str(self.tipo)
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

        # Configuración del treeview
        self.__config_treeview_vista()

    def __config_treeview_vista(self):
        self.treeview = ttk.Treeview(self.tabla)
        # Configuración de nombres de cada columna
        self.treeview.configure(show = "headings", columns = ("id_veh", "patente", "capacidad_tipo"))
        self.treeview.heading("id_veh", text = "ID")
        self.treeview.heading("patente", text = "Patente")
        self.treeview.heading("capacidad_tipo", text = "Capacidad")

        # Configuración de tamaños de cada columna
        self.treeview.column("id_veh", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("patente", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("capacidad_tipo", minwidth = 150, width = 100, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 350, width = 850)
        # Llenado del treeview
        self.llenar_treeview_vista()
        self.tabla.after(0, self.llenar_treeview_vista)

    def llenar_treeview_vista(self):
        # Se obtienen registros de la vista detalle_tipo
        opTreeview = "SELECT id_veh, patente, capacidad_tipo FROM detalle_tipo"

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
