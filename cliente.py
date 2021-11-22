import tkinter as tk
from tkinter import ttk

class cliente:#Clase de equipo, puede llamar a las clases de insertar y modificar
    def __init__(self, root, db):
        self.db = db
        self.data = []
        self.root = tk.Toplevel()
        self.root.geometry('650x400')
        self.root.title("Clientes")
        self.root.resizable(width=0, height=0)

        # toplevel modal
        self.root.transient(root)

        #
        #self.config_treeview_jugador()
        #self.config_buttons_jugador()
