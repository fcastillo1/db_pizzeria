#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Message

# Se define la clase informacion que mostrara mas detalles acerca de la app al usuario
class informacion:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []
        # Se crea una nueva ventana superior a la principal
        self.root = tk.Toplevel()
        # Se define el tamano de la ventana
        self.root.geometry('300x200')
        # Se define el título de la ventana
        self.root.title("Informacion APP")
        # Se añade color al fondo de la ventana
        self.root.config(bg="light cyan")
        # Esta opcion permite cambiar el tamano de la venta segun las necesidades del usuario
        self.root.resizable(width = 0, height = 0)
        self.root.transient(root)

        # Se llama a cada una de las funciones que permiten su funcionamiento
        self.__funcion_boton()
        self.__crear_mensaje()

    # Se crea la funcion que permite el funcionamiento del boton aceptar
    def __funcion_boton(self):
        # se define el nombre del boton, su texto y algunos detalles de su formtato
        boton_aceptar = Button(self.root, text="Aceptar", command=self.root.destroy, bg='green', fg='white')
        # Se establece la ubicacion del boton
        boton_aceptar.place(x=110, y= 150)

    # Esta funcion sera la encargada de crear el mensaje
    def __crear_mensaje(self):
        # se imprime el mensaje que el usuario podra ver en pantalla
        mensaje_informacion = Message(self.root, text = "VERSIÓN 1.1.1" + "/n" + "Esta aplicación fue desarrollada por Francisca Castillo y Rocío Rodríguez para la creación de la pizzería Il Italiano", bg="light cyan")
        # permitira el posicionamiento del mensaje
        mensaje_informacion.pack()
        # Empieza a correr la interfaz
        self.root.mainloop()
