#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerías principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Message
from tkinter import filedialog

# Se define la clase de ayuda que mostrará un texto que puede ser útil para el usuario
class ayuda:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []

        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('650x400')
        # Se define el título de la ventana
        self.root.title("Ayuda")
        # Se añade color al fondo de la ventana
        self.root.config(bg="light cyan")
        # Esta opción permite cambiar el tamano de la venta según las necesidades del usuario
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        self.__funcion_boton()
        # Se llama a cada una de las funciones que permiten su funcionamiento

        self.__crear_mensaje()

    # Se crea la función que permite el funcionamiento del botón aceptar
    def __funcion_boton(self):
        # Se define el nombre del botón, su texto y algunos detalles de su formato
        boton_aceptar = Button(self.root, text="Aceptar", command=self.root.destroy, bg='green', fg='white')
        # Se establece la ubicación del botón
        boton_aceptar.place(x =250, y = 350, width = 150)

    # Esta función es la encargada de crear el mensaje
    def __crear_mensaje(self):
        mensaje_ayuda = Message(self.root, text = open("ayuda.txt").read(), bg = "light cyan")
        # Posicionamiento del mensaje
        mensaje_ayuda.pack()
        # Empieza a correr la interfaz
        self.root.mainloop()
