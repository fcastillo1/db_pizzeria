#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox

# Se define la clase de  resumen_tipo que permite filtrar por tipo de vehículo
class resumen_tipo:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('270x185')
        # Se define el título de la ventana
        self.root.title("RESUMEN DE TIPO")
        # Se añade color al fondo de la ventana
        self.root.config(bg = "light cyan")
        # Esta opción permite cambiar el tamano de la ventana
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Configuraciones de widgets en ventana
        self.__config_button()
        self.__config_label()
        self.__config_entry()

    # Se define la configuracion del boton de la ventana que tendra 2 opciones
    def __config_button(self):
         # la primera opcion es que se pueda generar la muestra del resumen
        btn_ok = tk.Button(self.root, text = "Generar",
            command = self.__query_dinamica, bg = 'green', fg = 'white')
        # se define la ubicacion del boton
        btn_ok.place(x = 40, y = 140, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.root, text = "Cancelar",
            command = self.root.destroy, bg = 'red', fg = 'white')
        # se define la ubicacion del boton
        btn_cancel.place(x = 160, y = 140, width = 80, height = 20)
        
    # se define el label que permitira la entrada del texto o seleccion con combobox
    def __config_label(self):
        # Definición de entradas de texto
        pedido_lab = tk.Label(self.root, text = "Tipo: ", bg = "light cyan")
        # se define el lugar donde estara la entrada de texto
        pedido_lab.place(x = 5, y = 60, width = 105, height = 20)

    # Se define como sera la configuracion de la entrada de los datos
    def __config_entry(self):
        # Combobox para seleccionar el tipo
        self.combo = ttk.Combobox(self.root)
        # Se define la posicion del combobox
        self.combo.place(x = 90, y = 60, width = 150, height= 20)
        # Recepción de columna nombre e ids de tabla tipo
        self.combo["values"], self.ids = self.__llenar_combo_tipo()

        # Validación de combobox
        if self.ids != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla tipo
            texto = "Ingresar registros en TIPO"
            messagebox.showwarning("Listado vacío", texto)
            # Destruye ventana
            self.root.destroy()

    # se crea la funcion que permitira que se llene el combobox con la informacion
    def __llenar_combo_tipo(self):
        # Consulta para obtener detalles del combo
        opLCombo = "SELECT id_tipo, nom_tipo FROM tipo"
        # se lleva a cabo la consulta de llenarlo con mysql
        self.data = self.db.run_select(opLCombo)

        # Se retorna nombre del timpo y el id correspondiente
        return [i[1] for i in self.data], [i[0] for i in self.data]

    # Se genera la funcion que permitira la creacion de la consulta dinamica
    def __query_dinamica(self):
        # se lleva a cabo la consulta mediante el uso de sql y de los comandos de este
        sql = """SELECT vehiculo.id_veh,
        patente, capacidad_tipo FROM tipo JOIN vehiculo ON tipo.id_tipo = vehiculo.id_tipo
        WHERE tipo.id_tipo = %(id)s;"""

        # Se obtienen resultados de la consulta
        tipo = self.db.run_select_filter(sql, {"id": self.ids[self.combo.current()]})
        # se establece la condicion de que si el tipo es diferente a vacio
        if(tipo) != []:
            # Se pasa como parámetro todo el resultado del sql
            select_resumen_tipo(self.db, tipo)
        else:
            # No hay vehículos registrados para el tipo
            texto = "¿Desea intentar con otra opción?"
            # imprime el mensaje con la condicion
            opcion = messagebox.askretrycancel("Sin resultados", texto)

            # Sale de la ventana
            if opcion == False:
                self.root.destroy()

                
# se crea la clase que permite la seleccion del resumen del tipo (vehiculo)
class select_resumen_tipo:
    # se define la funcion con los parametros iniciales
    def __init__(self, db, tipo):
        self.db = db
        self.data = []

        # Tipo de vehículo escogido para mostrar
        self.tipo = tipo

        # Ventana emergente
        self.tabla = tk.Toplevel()

        # Ajustes de ventana
        # se define el tamaño de la ventana
        self.tabla.geometry('500x300')
        # se define el titulo de la ventana y algunas caracteristicas
        texto_titulo = "Listado de VEHÍCULOS según TIPO "
        self.tabla.title(texto_titulo)
        self.tabla.resizable(width = 0, height = 0)

        # Configuración del treeview
        self.__config_treeview_vista()
        # configuracion de los botones de la ventana de resumen
        self.__crear_botones_resumen_tipo()

    # se define la funcion que permite mostrar el treeview de la vista
    def __config_treeview_vista(self):
        self.treeview = ttk.Treeview(self.tabla)
        # Configuración de nombres de cada columna
        self.treeview.configure(show = "headings", columns = ("id_veh", "patente", "capacidad_tipo"))
        self.treeview.heading("id_veh", text = "ID")
        self.treeview.heading("patente", text = "Patente")
        self.treeview.heading("capacidad_tipo", text = "Capacidad")

        # Configuración de tamaños de cada columna
        self.treeview.column("id_veh", minwidth = 150, width = 165, stretch = False)
        self.treeview.column("patente", minwidth = 150, width = 170, stretch = False)
        self.treeview.column("capacidad_tipo", minwidth = 150, width = 165, stretch = False)

        # Ubica treeview
        self.treeview.place(x = 0, y = 0, height = 500, width = 850)
        # Llenado del treeview
        self.llenar_treeview_vista()
        self.tabla.after(0, self.llenar_treeview_vista)

    # se genera la funcion que permite llenar el treeview de la vista
    def llenar_treeview_vista(self):
        # Guarda info obtenida tras la consulta
        data = self.tipo

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:5])

            self.data = data

    # se define la funcion que permite la configuracion del boton
    def __crear_botones_resumen_tipo(self):
         # el boton sera aceptar y se definen algunas caracteristicas fisicas
        b4 = tk.Button(self.tabla, text = "Aceptar", bg='green', fg='white',
            command=self.tabla.destroy)
        # se define cual sera la ubicacion del boton
        b4.place(x = 150, y = 245, width = 200, height = 40)
