import tkinter as tk
from tkinter import ttk

class cliente:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('600x400')
        self.root.title("Clientes")
        self.root.resizable(width=0, height=0)

        # toplevel modal
        self.root.transient(root)

        #
        # self.__config_treeview_cliente()
        self.__crear_botones_cliente()

    # def __config_treeview_jugador(self):
    #     self.treeview = ttk.Treeview(self.root)
    #     self.treeview.configure(columns = ("rut_cli", "nom_clie", "ape_clie",
    #                                         "tel_clie", "dir_clie"))
    #     self.treeview.heading("rut_cli", text = "Rut")
    #     self.treeview.heading("nom_clie", text = "Nombre")
    #     self.treeview.heading("ape_clie", text = "Apellido")
    #     self.treeview.heading("tel_clie", text = "Teléfono")
    #     self.treeview.heading("dir_clie", text = "Dirección")
    #     self.treeview.column("rut_cli", minwidth = 100, width = 100, stretch = False)
    #     self.treeview.column("nom_clie", minwidth = 300, width = 300, stretch = False)
    #     self.treeview.column("ape_clie", minwidth = 300, width = 300, stretch = False)
    #     self.treeview.column("tel_clie", minwidth = 300, width = 300, stretch = False)
    #     self.treeview.column("dir_clie", minwidth = 300, width = 300, stretch = False)
    #     self.treeview.place(x = 0, y = 0, height = 350, width = 700)
    #     self.llenar_treeview_cliente()
    #     self.root.after(0, self.llenar_treeview_cliente)

    def __crear_botones_cliente(self):
        b1 = tk.Button(self.root, text="Insertar cliente", command = self.__insertar_cliente).place(x = 0, y = 350, width = 150, height = 50)
        b2 = tk.Button(self.root, text="Modificar cliente").place(x = 150, y = 350, width = 150, height = 50)
        b3 = tk.Button(self.root, text="Eliminar cliente").place(x = 300, y = 350, width = 150, height = 50)
        b4 = tk.Button(self.root, text="Ver clientes").place(x = 450, y = 350, width = 150, height = 50)

    def llenar_treeview_cliente(self):
        sql = """select rut_cli, nom_clie, ape_clie, tel_clie, dir_clie
        from cliente;"""

        data = self.db.run_select(sql)

        # mycursor = self.db.cursor("select rut_cli, nom_clie, ape_clie, tel_clie, dir_clie from cliente")
        # mycursor.execute("")
        # data = mycursor.fetchall()

        # if(data != self.data):
        #     self.treeview.delete(*self.treeview.get_children())#Elimina todos los rows del treeview
        #     for i in data:
        #         self.treeview.insert("", "end", text = i[0],
        #             values = (i[1]+ " " +i[2], i[3]), iid = i[0],tags = "rojo")
        #     self.data = data

    def __insertar_cliente(self):
        insertar_cliente(self.db, self)
    #
    # def __modificar_jugador(self):
    #     if(self.treeview.focus() != ""):
    #         sql = """select id_jugador, nom_jugador, ape_jugador, equipo.nom_equipo
    #         from jugador join equipo on jugador.id_equipo = equipo.id_equipo
    #         where id_jugador = %(id_jugador)s"""
    #
    #         row_data = self.db.run_select_filter(sql, {"id_jugador": self.treeview.focus()})[0]
    #         modificar_jugador(self.db, self, row_data)

    # def __eliminar_jugador(self):
    #     sql = "delete from jugador where id_jugador = %(id_jugador)s"
    #     self.db.run_sql(sql, {"id_jugador": self.treeview.focus()})
    #     self.llenar_treeview_jugador()

    # def __ver_equipos(self):
    #     equipo(self.db)

class insertar_cliente:
    def __init__(self, db, padre):
        self.padre = padre
        self.db = db
        self.insert_datos = tk.Toplevel()
        self.__config_window()
        self.__config_label()
        self.__config_entry()
        self.__config_button()

    def __config_window(self):
        self.insert_datos.geometry('200x180')
        self.insert_datos.title("Insertar cliente")
        self.insert_datos.resizable(width=0, height=0)

    def __config_label(self):
        tk.Label(self.insert_datos, text = "Rut: ").place(x = 10, y = 10, width = 80, height = 20)
        tk.Label(self.insert_datos, text = "Nombre: ").place(x = 10, y = 40, width = 80, height = 20)
        tk.Label(self.insert_datos, text = "Apellido: ").place(x = 10, y = 70, width = 80, height = 20)
        tk.Label(self.insert_datos, text = "Teléfono: ").place(x = 10, y = 100, width = 80, height = 20)
        tk.Label(self.insert_datos, text = "Dirección: ").place(x = 10, y = 130, width = 80, height = 20)

    def __config_entry(self):
        self.rut = tk.Entry(self.insert_datos)
        self.rut.place(x = 110, y = 10, width = 80, height = 20)
        self.nombre = tk.Entry(self.insert_datos)
        self.nombre.place(x = 110, y = 40, width = 80, height = 20)
        self.apellido = tk.Entry(self.insert_datos)
        self.apellido.place(x = 110, y = 70, width = 80, height = 20)
        self.telefono = tk.Entry(self.insert_datos)
        self.telefono.place(x = 110, y = 100, width = 80, height = 20)
        self.direccion = tk.Entry(self.insert_datos)
        self.direccion.place(x = 110, y = 130, width = 80, height = 20)

        # self.combo = ttk.Combobox(self.insert_datos)
        # self.combo.place(x = 110, y = 70, width = 80, height= 20)
        # self.combo["values"], self.ids = self.__fill_combo()

    def __config_button(self):
        tk.Button(self.insert_datos, text = "Aceptar",
            command = self.__insertar).place(x=10, y =160, width = 80, height = 20)
#
#     def __fill_combo(self):
#         sql = "select id_equipo, nom_equipo from equipo"
#         self.data = self.db.run_select(sql)
#         return [i[1] for i in self.data], [i[0] for i in self.data]
#
    def __insertar(self): #Insercion en la base de datos.
        sql = """insert cliente (rut_cli, nom_clie, ape_clie, tel_clie, dir_clie)
            values (%(rut)s, %(nombre)s, %(apellido)s, %(telefono)s, %(direccion)s)"""
        self.db.run_sql(sql, {"rut": self.rut.get(),"nombre": self.nombre.get(),
        "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get()})

        # consulta = ("""insert cliente (rut_cli, nom_clie,
        # ape_clie, tel_clie, dir_clie) values (%(rut)s, %(nombre)s, %(apellido)s,
        # %(telefono)s, %(direccion)s)""")
        #
        # data = {"rut": self.rut.get(),"nombre": self.nombre.get(),
        # "apellido": self.apellido.get(), "telefono": self.telefono.get(), "direccion": self.direccion.get()}
        #
        # try:
        #     cursor.execute(consulta, data)
        #     self.cursor.comit()
        # except:
        #     self.cursor.rollback()
        #
        # self.cursor.close()

        self.insert_datos.destroy()
        # self.padre.llenar_treeview_jugador()
