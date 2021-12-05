#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Message

class ayuda:
    def __init__(self, root, db):
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        self.root = tk.Toplevel()
        self.root.geometry('500x350')
        self.root.title("Ayuda")
        self.root.config(bg="light cyan")
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        self.__informacion_botones()
        self.__crear_mensaje()


    def __informacion_botones(self):
        exit_button = Button(self.root, text="Aceptar", command=self.root.destroy, bg='green', fg='white')
        exit_button.place(x=220, y= 300)
        #self.root.mainloop()

    def __crear_mensaje(self):
        msg = Message(self.root, text = "1. Para poder anadir, modificar o eliminar algun dato de interes se tiene que ir directamente a la ventan principal y seleccionar en donde deseas manipular la informacion. \n" + "\n" +
        "2. Cada una de topicos tiene su nombre y una foto relacionada a a informacion. Cabe destacar que a su vez cuando accedes a alguna ventana al momento de ingrear los datos estos tienen que ser de forma manual o por medio de un menu desplegable para relacion los datos. \n" + "\n" +
        "3. Las fechas se sugiere que se ingresen el formato de la fecha en AAAA-MM-DD HH:MM:SS, los datos telefonicos respecto al vehiculo son de tipo Entero (Numeros) y en la mayoria de los casos lso demas datos se pueden ingresar tanto con numeros como letras.  \n", bg="light cyan")
        msg.pack()
        self.root.mainloop()
