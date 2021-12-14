#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class cliente:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Se declara variable para abrir una ventana emergente sobre ventana principal
        self.root = tk.Toplevel()
        self.root.geometry('800x400')
        self.root.title("Clientes")
        self.root.config(bg="light cyan")
        self.root.resizable(width = 0, height = 0)
        # Es una ventana temporal de la ventana principal
        self.root.transient(root)

        # Visualización de clientes registrados en la base de datos
        self.__config_treeview_cliente()

        # Se crean los botones para indicar operaciones CRUD
        self.__crear_botones_cliente()

    def __config_treeview_cliente(self):
        # Generación del Treeview
        self.treeview = ttk.Treeview(self.root)
        # Se determinan los campos de las columnas
        self.treeview.configure(show = "headings", columns = ("rut_cli", "nom_clie",
                                "ape_clie", "tel_clie", "dir_clie", "id_ciudad"))

        # Para cada columna se especifica el nombre a mostrar
        self.treeview.heading("rut_cli", text = "Rut")
        self.treeview.heading("nom_clie", text = "Nombre")
        self.treeview.heading("ape_clie", text = "Apellido")
        self.treeview.heading("tel_clie", text = "Teléfono")
        self.treeview.heading("dir_clie", text = "Dirección")
        self.treeview.heading("id_ciudad", text = "Ciudad")

        # Configuraciones de cada columna
        self.treeview.column("rut_cli", minwidth = 150, width = 110, stretch = False)
        self.treeview.column("nom_clie", minwidth = 150, width = 120, stretch = False)
        self.treeview.column("ape_clie", minwidth = 150, width = 120, stretch = False)
        self.treeview.column("tel_clie", minwidth = 150, width = 120, stretch = False)
        self.treeview.column("dir_clie", minwidth = 150, width = 220, stretch = False)
        self.treeview.column("id_ciudad", minwidth = 150, width = 110, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 800)

        # Llenado del treeview
        self.llenar_treeview_cliente()
        self.root.after(0, self.llenar_treeview_cliente)

    def __crear_botones_cliente(self):
        # Botón abre nueva ventana para insertar un cliente
        b1 = tk.Button(self.root, text = "Insertar cliente", bg = 'snow',
                        fg = 'green', command = self.__insertar_cliente)
        b1.place(x = 0, y = 350, width = 200, height = 50)

        # Botón abre nueva ventana para modificar cliente seleccionado
        b2 = tk.Button(self.root, text = "Modificar cliente", bg = 'snow',
                        fg = 'orange', command = self.__modificar_cliente)
        b2.place(x = 200, y = 350, width = 200, height = 50)

        # Botón permite eliminar el cliente seleccionado
        b3 = tk.Button(self.root, text = "Eliminar cliente", bg = 'snow', fg = 'red',
                        command = self.__eliminar_cliente)
        b3.place(x = 400, y = 350, width = 200, height = 50)

        # Permite salir de la ventana de cliente
        b4 = tk.Button(self.root, text = "Salir", command=self.root.destroy, bg='red', fg='white')
        b4.place(x = 600, y = 350, width = 200, height = 50)

    def llenar_treeview_cliente(self):
        # Se obtienen clientes ingresados
        opTreeview = """SELECT rut_clie, nom_clie, ape_clie, tel_clie, dir_clie, nom_ciudad
        from cliente join ciudad on cliente.id_ciudad = ciudad.id_ciudad;"""

        # Guarda info obtenida tras la consulta
        data = self.db.run_select(opTreeview)

        # Evalúa si el contenido de la tabla en la app es distinto al de la db
        if(data != self.data):
            # Elimina todos los rows del treeview si hay diferencias
            self.treeview.delete(*self.treeview.get_children())

            # Recorre cada registro (tupla) guardado en var data
            for i in data:
                # Inserta valores en treeview
                self.treeview.insert("", "end", iid = i[0], values = i[0:6])

            self.data = data

    def __insertar_cliente(self):
        # Llamada a la clase que permite realizar la inserción de un cliente
        insertar_cliente(self.db, self)

    def __eliminar_cliente(self):
        texto_msj = "¿Realmente quieres borrar el registro?"

        # Si hay un elemento seleccionado, se confirma eliminación
        if ((self.treeview.focus() != "") and
            (messagebox.askyesno(message = texto_msj, title = "Alerta") == True)):

            # Consulta para realizar la eliminación de un cliente
            opEliminar = "DELETE FROM cliente where rut_clie = %(rut_clie)s"

            # Ejecución de la eliminación en la base de datos
            self.db.run_sql(opEliminar, {"rut_clie": self.treeview.focus()}, "D")

            # Se actualiza el treeview de la ventana de cliente
            self.llenar_treeview_cliente()

    def __modificar_cliente(self):
        texto_msj = "¿Realmente quieres modificar el registro?"
        # Si hay un elemento seleccionado, se confirma modificación
        if ((self.treeview.focus() != "") and
            (messagebox.askyesno(message =  texto_msj, title = "Alerta") == True)):

            # SQL para obtener datos de registro a modificar
            opModificar = """SELECT rut_clie, nom_clie, ape_clie, tel_clie, dir_clie,
            nom_ciudad from cliente join ciudad on cliente.id_ciudad = ciudad.id_ciudad
            WHERE rut_clie = %(rut)s"""

            # Se consulta en la tabla cliente por el rut del registro a modificar
            mod_select = self.db.run_select_filter(opModificar, {"rut": self.treeview.focus()})[0]

            # Se llama a la clase para modificar el cliente con los datos actuales
            modificar_cliente(self.db, self, mod_select)

class insertar_cliente:
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db

        # Ventana emergente
        self.insert_datos = tk.Toplevel()

        # Funcionalidades
        self.__config_button()
        self.__config_window()
        self.__config_label()
        self.__config_entry()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x250')
        self.insert_datos.title("Insertar cliente")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Definición de entradas de texto para la clase cliente
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)
        dir_lab = tk.Label(self.insert_datos, text = "Dirección: ")
        dir_lab.place(x = 10, y = 130, width = 120, height = 20)
        ciu_lab = tk.Label(self.insert_datos, text = "Ciudad: ")
        ciu_lab.place(x = 10, y = 160, width = 120, height = 20)

    def __config_entry(self):
        # Se insertan múltiples entradas de texto
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)
        self.direccion = tk.Entry(self.insert_datos)
        self.direccion.place(x = 110, y = 130, width = 150, height = 20)

        # Se inserta el combobox
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 160, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        # Validación de combobox de ciudades
        if self.ids != []:
            # Si no está vacío, se coloca por defecto el primer ítem
            self.combo.insert(0, self.combo["values"][0])
            self.combo.config(state = "readonly")
        else:
            # Advierte que no hay registros en la tabla ciudad
            texto = "Ingresar registros en CIUDAD"
            messagebox.showerror("Problema de inserción", texto)
            # Destruye ventana
            self.insert_datos.destroy()

    def __llenar_combo(self):
        # Consulta para obtener registros de tabla ciudad
        opLCombo = "SELECT id_ciudad, nom_ciudad FROM ciudad"
        self.data = self.db.run_select(opLCombo)
        # Retorna nombre e id de ciudad
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
                            command = self.__insertar, bg='green', fg='white')
        btn_ok.place(x=100, y =200, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
                                command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x=210, y =200, width = 80, height = 20)

    def __insertar(self):
        # Inserción de cliente
        opInsert = """INSERT cliente (rut_clie, nom_clie, ape_clie, tel_clie, dir_clie, id_ciudad)
                values (%(rut)s, %(nombre)s, %(apellido)s, %(telefono)s, %(direccion)s, %(ciudad)s)"""

        # Se ejecuta consulta en la base de datos
        self.db.run_sql(opInsert, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get(),
            "ciudad": self.ids[self.combo.current()]}, "I")

        # Se cierra la ventana de inserción de clientes
        self.insert_datos.destroy()
        # Se actualiza el treeview de la ventana principal
        self.padre.llenar_treeview_cliente()

class modificar_cliente:
    def __init__(self, db, padre, mod_select):
        # Ventana principal de cliente corresponde a ventana padre
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        self.insert_datos = tk.Toplevel()
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        # Ajustes de ventana
        self.insert_datos.geometry('300x250')
        self.insert_datos.title("Modificar cliente")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        # Etiquetas para señalar el texto que debe ingresarse
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)
        dir_lab = tk.Label(self.insert_datos, text = "Dirección: ")
        dir_lab.place(x = 10, y = 130, width = 120, height = 20)
        ciu_lab = tk.Label(self.insert_datos, text = "Ciudad: ")
        ciu_lab.place(x = 10, y = 160, width = 120, height = 20)

    def __config_entry(self):
        # Se obtiene texto para ingresar clientes (rut, nombre, apellido, teléfono,
        # dirección)
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)
        self.direccion = tk.Entry(self.insert_datos)
        self.direccion.place(x = 110, y = 130, width = 150, height = 20)

        # Se crea un combobox para que el cliente pueda seleccionar la ciudad
        self.combo = ttk.Combobox(self.insert_datos)
        self.combo.place(x = 110, y = 160, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

        # Se guarda el valor del rut actual del registro a modificar
        self.rut_viejo = self.mod_select[0]

        # Se insertan valores actuales en las entradas de texto
        self.rut.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])
        self.apellido.insert(0, self.mod_select[2])
        self.telefono.insert(0, self.mod_select[3])
        self.direccion.insert(0, self.mod_select[4])

        # Se inserta ciudad actual en el combobox
        self.combo.insert(0, self.mod_select[5])
        self.combo.config(state = "readonly")

    def __llenar_combo(self):
        # Consulta para obtener id y nombre de ciudad
        opLlenar = "SELECT id_ciudad, nom_ciudad FROM ciudad"

        # Ejecución de la consulta en la base de datos
        self.data = self.db.run_select(opLlenar)

        # Se retorna nombre e id
        return [i[1] for i in self.data], [i[0] for i in self.data]

    def __config_button(self):
        # Crea botón aceptar y se enlaza a evento para modificar cliente
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 200, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x = 210, y = 200, width = 80, height = 20)

    def __modificar(self):
        # Consulta para modificar el registro de acuerdo a un rut específico
        opEdicion = """UPDATE cliente set rut_clie = %(rut)s, nom_clie = %(nombre)s,
            ape_clie = %(apellido)s, tel_clie = %(telefono)s, dir_clie = %(direccion)s,
            id_ciudad = %(ciudad)s WHERE rut_clie = %(rut_viejo)s"""

        # Se ejecuta la consulta
        self.db.run_sql(opEdicion, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get(),
            "ciudad": self.ids[self.combo.current()], "rut_viejo": self.rut_viejo}, "U")

        # Destrucción de la ventana de modificación
        self.insert_datos.destroy()

        # Se actualiza el treeview de la ventana principal de cliente
        self.padre.llenar_treeview_cliente()
