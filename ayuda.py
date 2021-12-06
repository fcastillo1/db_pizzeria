#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Message
from tkinter import filedialog

# Se define la clase de ayuda que mostrara un texto que puede ser utili para el usuario
class ayuda:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Toplevel es una ventana que está un nivel arriba que la principal
        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('500x350')
        # Se define el título de la ventana
        self.root.title("Ayuda")
        # Se añade color al fondo de la ventana
        self.root.config(bg="light cyan")
        # Esta opcion permite cambiar el tamano de la venta segun las necesidades del usuario
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        self.__informacion_botones()
        # Se llama a cada una de las funciones que permiten su funcionamiento
        self.__funcion_boton()
        self.__crear_mensaje()

    # Se crea la funcion que permite el funcionamiento del boton aceptar
    def __funcion_boton(self):
        # se define el nombre del boton, su texto y algunos detalles de su formtato
        boton_aceptar = Button(self.root, text="Aceptar", command=self.root.destroy, bg='green', fg='white')
        # Se establece la ubicacion del boton
        boton_aceptar.place(x=220, y= 300)

    def __informacion_botones(self):
        exit_button = Button(self.root, text="Aceptar", command=self.root.destroy, bg='green', fg='white')
        exit_button.place(x=220, y= 300)
        #self.root.mainloop()

    # Esta funcion sera la encargada de crear el mensaje
    def __crear_mensaje(self):
        mensaje_ayuda = Message(self.root, text = open("ayuda.txt").read(), bg = "light cyan")
        # permitira el posicionamiento del mensaje
        mensaje_ayuda.pack()
        # Empieza a correr la interfaz
        self.root.mainloop()
