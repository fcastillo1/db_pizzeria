#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Message

# Se define la clase de ayuda que mostrara un texto que puede ser utili para el usuario
class ayuda:
    def __init__(self, root, db):
        # Se actualiza atributo con la database
        self.db = db
        self.data = []
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

        # Se llama a cada una de las funciones que permiten su funcionamiento
        self.__funcion_boton()
        self.__crear_mensaje()

    # Se crea la funcion que permite el funcionamiento del boton aceptar
    def __funcion_boton(self):
        # se define el nombre del boton, su texto y algunos detalles de su formtato
        boton_aceptar = Button(self.root, text="Aceptar", command=self.root.destroy, bg='green', fg='white')
        # Se establece la ubicacion del boton
        boton_aceptar.place(x=220, y= 300)

    # Esta funcion sera la encargada de crear el mensaje
    def __crear_mensaje(self):
        # se imprime el mensaje que el usuario podra ver en pantalla y lo orientara respecto a ciertas ayuda que requiera
        mensaje_ayuda = Message(self.root, text = "1. Para poder anadir, modificar o eliminar algun dato de interes se tiene que ir directamente a la ventan principal y seleccionar en donde deseas manipular la informacion. \n" + "\n" +
        "2. Cada una de topicos tiene su nombre y una foto relacionada a a informacion. Cabe destacar que a su vez cuando accedes a alguna ventana al momento de ingrear los datos estos tienen que ser de forma manual o por medio de un menu desplegable para relacion los datos. \n" + "\n" +
        "3. Las fechas se sugiere que se ingresen el formato de la fecha en AAAA-MM-DD HH:MM:SS, los datos telefonicos respecto al vehiculo son de tipo Entero (Numeros) y en la mayoria de los casos lso demas datos se pueden ingresar tanto con numeros como letras.  \n", bg="light cyan")
        # permitira el posicionamiento del mensaje
        mensaje_ayuda.pack()
        # Empieza a correr la interfaz
        self.root.mainloop()
