#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Message
from tkinter import filedialog

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
        exit_button = Button(self.root, text = "Aceptar", command=self.root.destroy, bg='green', fg='white')
        exit_button.place(x=220, y= 300)
        #self.root.mainloop()

    def __crear_mensaje(self):
        msg = Message(self.root, text = open("ayuda.txt").read(), bg = "light cyan")
        msg.pack()
        self.root.mainloop()
