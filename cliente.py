#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Se define la clase de cliente(tabla)
class cliente:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea un que e sun aventana superior a la principal
        self.root = tk.Toplevel()
        # se define el tamaño de la ventana
        self.root.geometry('600x400')
        # se define el titulo que tendra la ventana
        self.root.title("Cliente")
        # mediante esta opcion de configuracion la ventana tendra un color de fondo
        self.root.config(bg="light cyan")
        # Esta opcion permite cambiar el tamano de la venta segun las necesidades del usuario
        self.root.resizable(width = 0, height = 0)

        # Se permite la creacion de una ventana nueva
        self.root.transient(root)

        # Se llaman a las funciones creadas
        self.__config_treeview_cliente()
        self.__crear_botones_cliente()

    # Esta funcion permitira poder hacer un treeview que solicitara los datos al user
    def __config_treeview_cliente(self):
        # se genera el trevieew 
        self.treeview = ttk.Treeview(self.root)
        # se generan los headin que estan arriba de la ventan y muestran la informacion de cliente
        self.treeview.configure(show = "headings", columns = ("rut_cli", "nom_clie", "ape_clie",
            "tel_clie", "dir_clie", "id_ciudad"))
        # se crean los treeview de la informacion de los clientes y tambien su formato
        self.treeview.heading("rut_cli", text = "Rut")
        self.treeview.heading("nom_clie", text = "Nombre")
        self.treeview.heading("ape_clie", text = "Apellido")
        self.treeview.heading("tel_clie", text = "Teléfono")
        self.treeview.heading("dir_clie", text = "Dirección")
        self.treeview.heading("id_ciudad", text = "Ciudad")
        self.treeview.column("rut_cli", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("nom_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("ape_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("tel_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("dir_clie", minwidth = 150, width = 100, stretch = False)
        self.treeview.column("id_ciudad", minwidth = 150, width = 100, stretch = False)
        self.treeview.place(x = 0, y = 0, height = 350, width = 700)
        # Llenado del treeview
        self.llenar_treeview_cliente()

        self.root.after(0, self.llenar_treeview_cliente)

    # Esta funcion permite la creacion de los botones
    def __crear_botones_ciudad(self):
        # este boton permitira que se pueda insertar la ciudad y el formato de este
        btn_insert = tk.Button(self.root, text = "Insertar ciudad", bg='snow',
            fg='green', command = self.__insertar_ciudad)
        # aqui se describe la posicion del boton
        btn_insert.place(x = 0, y = 350, width = 150, height = 50)
        # este boton permitira que se pueda modificar la ciudad y el formato de este
        btn_modificar = tk.Button(self.root, text = "Modificar ciudad", bg='snow',
            fg='orange', command = self.__modificar_ciudad)
        # aqui se describe la posicion del boton
        btn_modificar.place(x = 150, y = 350, width = 150, height = 50)
        # este boton permitira que se pueda eliminar la ciudad y el formato de este
        btn_delete = tk.Button(self.root, text = "Eliminar ciudad", bg='snow',
            fg='red', command = self.__eliminar_ciudad)
        # aqui se describe la posicion del boton
        btn_delete.place(x = 300, y = 350, width = 150, height = 50)
        # este boton permitira que se pueda salir la ciudad y el formato de este
        btn_exit = tk.Button(self.root, text = "Salir", bg='red', fg='white',
            command=self.root.destroy)
        # aqui se describe la posicion del boton
        btn_exit.place(x = 450, y = 350, width = 150, height = 50)

    # esta funcion permite que el treeview se llene
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
    
    # esta funcion llama a la otra que permite que se inserte el cliente
    def __insertar_cliente(self):
        insertar_cliente(self.db, self)
    
    # esta funcion permite que la cliente se eliminada
    def __eliminar_cliente(self):
        # se imprime el mensaje box para advertir que se borra el registro
        if messagebox.askyesno(message="¿Realmente quieres borrar el registro?", title = "Alerta")== True:
            # se indica cual sera la operacion a realizar
            opEliminar = "DELETE FROM cliente where rut_clie = %(rut_clie)s"
            # se elimina desde la base de datos por el id
            self.db.run_sql(opEliminar, {"rut_clie": self.treeview.focus()})
            self.llenar_treeview_cliente()

    # esta funcion permite que se modifique al cliente
    def __modificar_cliente(self):
         # se imprime el mensaje box para advertir que se modifica el mensaje
        if messagebox.askyesno(message="¿Realmente quieres modificar el registro?", title = "Alerta")== True:
            if(self.treeview.focus() != ""):
                # se indica cual sera la operacion a realizar en este caso modificar
                opModificar = """SELECT rut_clie, nom_clie, ape_clie, tel_clie, dir_clie,
                nom_ciudad from cliente join ciudad on cliente.id_ciudad = ciudad.id_ciudad
                WHERE rut_clie = %(rut)s"""
                
                # Se consulta en la tabla cliente por el rut del registro a modificar
                mod_select = self.db.run_select_filter(opModificar, {"rut": self.treeview.focus()})[0]
                modificar_cliente(self.db, self, mod_select)

# Se genera una clase que permite que al cliente sea insertada
class insertar_cliente:
    def __init__(self, db, padre):
        # se definen los self de la base de datos y del padre
        self.padre = padre
        self.db = db

        # Se genera la ventana emergente
        self.insert_datos = tk.Toplevel()

        # Se procede a llamar a cada una de las funciones necesarias
        self.__configuracion_ventana()
        self.__configuracion_label()
        self.__configuracion_text_entrada()
        self.__configuracion_boton()

    # esta funcion permite la configuracion de la ventana
    def __configuracion_ventana(self):
        # Se define el tamano de la ventana
        self.insert_datos.geometry('300x200')
        # Se define el título de la ventana
        self.insert_datos.title("Insertar cliente")
        self.insert_datos.resizable(width=0, height=0)

    # Se define la clase que vera la configuracion del label
    def __configuracion_label(self):
        # Definición de entradas de texto para la clase cliente
        # Se define la entrada de rut con algunas configuraciones de tamaño y estructura
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        # Se define la entreda de nombre con algunas configuraciones de tamaño y estructura
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        # Se define la entrada de apellido con algunas configuraciones de tamaño y estructura
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        # Se define la entrada de telefono con algunas configuraciones de tamaño y estructura
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)
        # Se define la entrada de direccion con algunas configuraciones de tamaño y estructura
        dir_lab = tk.Label(self.insert_datos, text = "Dirección: ")
        dir_lab.place(x = 10, y = 130, width = 120, height = 20)
        # Se define la entrada de ciudad con algunas configuraciones de tamaño y estructura
        ciu_lab = tk.Label(self.insert_datos, text = "Ciudad: ")
        ciu_lab.place(x = 10, y = 160, width = 120, height = 20)

    # Se define la clase que vera la configuracion del texto que entrada
    def __configuracion_text_entrada(self):
        # Se obtiene texto para ingresar clientes
        self.rut = tk.Entry(self.insert_datos)
        # se obtiene el texto y la posicion donde debe ir para el rut
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        # se obtiene el texto y la posicion donde debe ir para el nombre
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        # se obtiene el texto y la posicion donde debe ir para el apellido
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        # se obtiene el texto y la posicion donde debe ir para el telefono
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)
        self.direccion = tk.Entry(self.insert_datos)
        # se obtiene el texto y la posicion donde debe ir para la direccion
        self.direccion.place(x = 110, y = 130, width = 150, height = 20)
        self.combo = ttk.Combobox(self.insert_datos)
        # se obtiene el texto y la posicion donde debe ir para el lugar
        self.combo.place(x = 110, y = 160, width = 150, height= 20)
        self.combo["values"], self.ids = self.__llenar_combo()

    # esta funcion permite llenar el combobox con la informacion de ciudad
    def __llenar_combo(self):
        # se ingresa el comando de sql que pemrmitira llenar el combobox
        opLCombo = "SELECT id_ciudad, nom_ciudad FROM ciudad"
        # se conecta la informacion de sql con la base de datos para llenar el combobox
        self.data = self.db.run_select(opLCombo)
        # se retorna y se ocupa como matriz llenando los datos de la base de datos
        return [i[1] for i in self.data], [i[0] for i in self.data]

    # Se define la clase que vera la configuracion del boton
    def __configuracion_boton(self):
        # Crea botón aceptar ingreso y se enlaza a evento
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar, bg='green', fg='white')
         # se define la ubicacion del boton
        btn_ok.place(x=100, y =200, width = 80, height = 20)

        # Crea botón para cancelar ingreso y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
         # se define la ubicacion del boton
        btn_cancel.place(x=210, y =200, width = 80, height = 20)

    # se define la funcion que permite la Insercion en la base de datos.
    def __insertar(self): 
        # Inserción de cliente
        opInsert = """INSERT cliente (rut_clie, nom_clie, ape_clie, tel_clie, dir_clie, id_ciudad)
                values (%(rut)s, %(nombre)s, %(apellido)s, %(telefono)s, %(direccion)s, %(ciudad)s)"""
        # Se ejecuta consulta
        self.db.run_sql(opInsert, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get(),
            "ciudad": self.ids[self.combo.current()]})

        self.insert_datos.destroy()
        self.padre.llenar_treeview_cliente()

# se crea la clase que modifica al cliente
class modificar_cliente:
    def __init__(self, db, padre, mod_select):
        # se definen los self de la base de datos y del padre
        self.padre = padre
        self.db = db
        self.mod_select = mod_select
        # Se genera una ventana emergente
        self.insert_datos = tk.Toplevel()
        # Se procede a llamar a cada una de las funciones necesarias
        self.__configuracion_ventana()
        self.__configuracion_label()
        self.__configuracion_text_entrada()
        self.__llenar_combo()
        self.__configuracion_boton()

     # esta funcion permite la configuracion de la ventana
    def __configuracion_ventana(self):
        # Se define el tamano de la ventana
        self.insert_datos.geometry('300x200')
        # Se define el título de la ventana
        self.insert_datos.title(" Modificar cliente")
        self.insert_datos.resizable(width=0, height=0)

    # Se define la clase que vera la configuracion del label
    def __configuracion_label(self):
        # Definición de entradas de texto para la clase cliente para el rut
        rut_lab = tk.Label(self.insert_datos, text = "Rut: ")
        rut_lab.place(x = 10, y = 10, width = 120, height = 20)
        # Definición de entradas de texto para la clase cliente para el nombre
        nom_lab = tk.Label(self.insert_datos, text = "Nombre: ")
        nom_lab.place(x = 10, y = 40, width = 120, height = 20)
        # Definición de entradas de texto para la clase cliente para el apellido
        ape_lab = tk.Label(self.insert_datos, text = "Apellido: ")
        ape_lab.place(x = 10, y = 70, width = 120, height = 20)
        # Definición de entradas de texto para la clase cliente para el telefono
        tel_lab = tk.Label(self.insert_datos, text = "Teléfono: ")
        tel_lab.place(x = 10, y = 100, width = 120, height = 20)
        # Definición de entradas de texto para la clase cliente para la direccion
        dir_lab = tk.Label(self.insert_datos, text = "Dirección: ")
        dir_lab.place(x = 10, y = 130, width = 120, height = 20)
        # Definición de entradas de texto para la clase cliente para la ciudad
        ciu_lab = tk.Label(self.insert_datos, text = "Ciudad: ")
        ciu_lab.place(x = 10, y = 160, width = 120, height = 20)

    # Se define la clase que vera la configuracion del texto que entrada
    def __configuracion_text_entrada(self):
        # Se obtiene texto para ingresar clientes desde el rut
        self.rut = tk.Entry(self.insert_datos)
        # Se obtiene la ubicacion donde se dejara el rut
        self.rut.place(x = 110, y = 10, width = 150, height = 20)
        # Se obtiene texto para ingresar clientes desde el nombre
        self.nombre = tk.Entry(self.insert_datos)
        # Se obtiene la ubicacion donde se dejara el nombre
        self.nombre.place(x = 110, y = 40, width = 150, height = 20)
        # Se obtiene texto para ingresar clientes desde el apellido
        self.apellido = tk.Entry(self.insert_datos)
        # Se obtiene texto para ingresar clientes desde el apellido
        self.apellido.place(x = 110, y = 70, width = 150, height = 20)
        # Se obtiene texto para ingresar clientes desde el telefono
        self.telefono = tk.Entry(self.insert_datos)
        # Se obtiene texto para ingresar clientes desde el telefono
        self.telefono.place(x = 110, y = 100, width = 150, height = 20)
        # Se obtiene texto para ingresar clientes desde la direccion
        self.direccion = tk.Entry(self.insert_datos)
        # Se obtiene texto para ingresar clientes desde la direccion
        self.direccion.place(x = 110, y = 130, width = 150, height = 20)
        # Se define el combobox desde el insert al datos
        self.combo = ttk.Combobox(self.insert_datos)
        # se define la ubicacion del combobox
        self.combo.place(x = 110, y = 160, width = 150, height= 20)
        # se llenan los valores de llenar el combobox
        self.combo["values"], self.ids = self.__llenar_combo()
        self.rut.insert(0, self.mod_select[0])
        self.nombre.insert(0, self.mod_select[1])
        self.apellido.insert(0, self.mod_select[2])
        self.telefono.insert(0, self.mod_select[3])
        self.direccion.insert(0, self.mod_select[4])
        self.combo.insert(0, self.mod_select[5])

    # esta funcion permite llenar el combobox con la informacion
    def __llenar_combo(self):
        # este es el comando que permite llenar la informacion
        opLlenar = "SELECT id_ciudad, nom_ciudad FROM ciudad"
        # se conecta la informacion de llenar el combobox con la base de datos
        self.data = self.db.run_select(opLlenar)
        return [i[1] for i in self.data], [i[0] for i in self.data]

    # Se define la clase que vera la configuracion del boton
    def __configuracion_boton(self):
        # Crea botón aceptar y se enlaza a evento para modificar cliente
        btn_ok = tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__modificar, bg = 'green', fg = 'white')
        btn_ok.place(x = 100, y = 200, width = 80, height = 20)

        # Crea botón para cancelar modificación y se destruye ventana
        btn_cancel = tk.Button(self.insert_datos, text = "Cancelar",
            command = self.insert_datos.destroy, bg='red', fg='white')
        btn_cancel.place(x = 210, y = 200, width = 80, height = 20)

    # Se define la clase de modificar para confirmar el registro 
    def __modificar(self): 
         # Modificar registro con los comandos de mysql
        opEdicion = """UPDATE cliente set rut_clie = %(rut)s, nom_clie = %(nombre)s,
            ape_clie = %(apellido)s, tel_clie = %(telefono)s, dir_clie = %(direccion)s,
            id_ciudad = %(ciudad)s WHERE rut_clie = %(rut)s"""
         # Empieza a correr la informacion para poder editar la informacion desde la db
        self.db.run_sql(opEdicion, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get(),
            "ciudad": self.ids[self.combo.current()]})

        self.insert_datos.destroy()
        # Se actualizan registros en la ventana principal (padre)
        self.padre.llenar_treeview_cliente()

