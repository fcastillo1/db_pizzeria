#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import PhotoImage
from PIL import Image, ImageTk


# Se importan todos los archivos con sus clases que son necesarios para el funcionamiento de la database
from db_pizzeria import DB_pizzeria
from cliente import cliente
from ciudad import ciudad
from pizza import pizza
from vehiculo import vehiculo
from repartidor import repartidor
from pedido import pedido
from informacion import informacion
from ayuda import ayuda

# Se define la clase que es de la aplicacion y permite su uso
class aplicacion:
    def __init__(self, db):
        # Se actualiza atributo con la database
        self.db = db

        # Creación de ventana principal
        self.root = tk.Tk()
        # Se define el tamano de la ventana
        self.root.geometry("750x550")
        # Se define el título de la ventana
        self.root.title("APP Pizzería l'italiano")
        # Se añade color al fondo de la ventana
        self.root.config(bg = "light cyan")

        # Se llaman cada una de las funciones que son parte de la app
        self.__crearBotones()
        self.__crearMenu()
        self.__agregarImagenInicial()

        # Empieza a correr la interfaz
        self.root.mainloop()

    # Esta funcion permite la creacion de los botones principales de la aplicacion
    def __crearBotones(self):
        # Se sube una Imagen al botón ciudad
        image_ciudad = Image.open("ciudad.jpg")
        image_ciudad = image_ciudad.resize((63, 45), Image.ANTIALIAS)
        self.reset_img1 = ImageTk.PhotoImage(image_ciudad)

        # Se sube una Imagen al botón pedido
        image_pedido = Image.open("pedido.jpg")
        image_pedido = image_pedido.resize((63, 45), Image.ANTIALIAS)
        self.reset_img2 = ImageTk.PhotoImage(image_pedido)

        # Se sube una Imagen al botón cliente
        image_cliente = Image.open("cliente.jpg")
        image_cliente = image_cliente.resize((63, 45), Image.ANTIALIAS)
        self.reset_img3 = ImageTk.PhotoImage(image_cliente)

        # Se sube una Imagen al botón cliente
        image_cliente = Image.open("cliente.jpg")
        image_cliente = image_cliente.resize((63, 45), Image.ANTIALIAS)
        self.reset_img3 = ImageTk.PhotoImage(image_cliente)

        # Se sube una Imagen al botón pizza
        image_pizza = Image.open("pizza.jpg")
        image_pizza = image_pizza.resize((63, 45), Image.ANTIALIAS)
        self.reset_img4 = ImageTk.PhotoImage(image_pizza)

        # Se sube una Imagen al botón repartidor
        image_repartidor = Image.open("repartidor.jpg")
        image_repartidor = image_repartidor.resize((63, 45), Image.ANTIALIAS)
        self.reset_img5 = ImageTk.PhotoImage(image_repartidor)

        # Se sube una Imagen al botón vehículo
        image_vehiculo = Image.open("vehiculo.jpg")
        image_vehiculo = image_vehiculo.resize((63, 45), Image.ANTIALIAS)
        self.reset_img6 = ImageTk.PhotoImage(image_vehiculo)

        # Creación de los botones principales
        # Creacion boton ciudad con su texto e informacion para su funcionamiento
        boton_ciudad = Button(self.root, text = "Ciudades", image = self.reset_img1, compound = 'top',
        command = self.__mostrar_ciudad, width=135, bg='snow', fg='black').place(x=10, y=10)

        # Creacion boton cliente con su texto e informacion para su funcionamiento
        boton_cliente = Button(self.root, text = "Cliente",  image = self.reset_img2, compound = 'top',
        command = self.__mostrar_cliente, width=135 , bg='snow', fg='black').place(x=10, y=95)

        # Creacion boton pedido con su texto e informacion para su funcionamiento
        boton_pedido = Button(self.root, text = "Pedido",  image = self.reset_img3, compound = 'top',
        command = self.__mostrar_pedido,  width=135, bg='snow', fg='black').place(x=10, y=180)

        # Creacion boton pizza con su texto e informacion para su funcionamiento
        boton_pizza = Button(self.root, text = "Pizza", image = self.reset_img4, compound = 'top',
        command = self.__mostrar_pizza, width=135 , bg='snow', fg='black').place(x=10, y=265)

        # Creacion boton repartidor con su texto e informacion para su funcionamiento
        boton_repartidor = Button(self.root, text = "Repartidor",  image = self.reset_img5, compound = 'top',
        command = self.__mostrar_repartidor, width=135 , bg='snow', fg='black').place(x=10, y=350)

        # Creacion boton vehiculo con su texto e informacion para su funcionamiento
        boton_vehiculo = Button(self.root, text = "Vehiculo",  image = self.reset_img6, compound = 'top',
        command = self.__mostrar_vehiculo, width=135 , bg='snow', fg='black').place(x=10, y=435)

        # Creacion boton salir que permitira que se cierre la app
        boton_salir = Button(self.root, text = "Salir", command = self.root.destroy,
        width=20, bg='red', fg='white').place(x=375, y=475)


    # Esta funcion permite crear el menu de opciones
    def __crearMenu(self):
        menu_opciones = Menu(self.root)
        self.root.config(menu = menu_opciones)

        # Se construye el menubar de la información con su color
        info_menu = Menu(menu_opciones, tearoff = 0, bg = "white")
        menu_opciones.add_cascade(label = "Información", menu = info_menu)

        # Dentro del botón de informacion, hay un botón que detalla acerca de la app y desarrolladores
        info_menu.add_command(label = "Acerca de App", command = self.__mostrar_informacion)

        # Se genera un espacio
        info_menu.add_separator()

        # Se genera un boton para destruir la ventana
        info_menu.add_command(label = "Salir", command = self.root.destroy)

        # Se construye el menú de ayuda con su color
        help_menu = Menu(menu_opciones, tearoff = 0, bg = "white")
        menu_opciones.add_cascade(label = "Ayuda", menu = help_menu)

        # Dentro del botón de AYUDA, existirá uno para guiar al usuario
        help_menu.add_command(label = "Ayuda", command = self.__mostrar_ayuda)

    # Esta funcion permite anadir una imagen a la aplicacion
    def __agregarImagenInicial(self):
        frame = LabelFrame(self.root, text = "", relief = tk.FLAT)
        # Se define la ubicación del frame
        frame.place(x = 240, y = 60)

        # Imagen principal de la ventana abierta a partir de un archivo
        image = Image.open("imagenpizza.jpg")

        # Se define el tamaño de la imagen
        photo = ImageTk.PhotoImage(image.resize((450, 350), Image.ANTIALIAS))
        # Se hace un label con el frame e imagen
        label = Label(frame, image = photo)
        label.image = photo
        label.pack()

    # Esta funcion mostrara la informacion de la base de datos y llama a la clase con su nombre a partir de su archivo
    def __mostrar_informacion(self):
        informacion(self.root, self.db)

    # Esta funcion mostrara la informaicon de ayuda y llama a la clase con su nombre a partir de su archivo
    def __mostrar_ayuda(self):
        ayuda(self.root, self.db)

    # Esta funcion mostrara la informacion de la clase cliente a partir de su archivo
    def __mostrar_cliente(self):
        cliente(self.root, self.db)

    # Esta funcion mostrara la informacion de la clase ciudad a partir de su archivo
    def __mostrar_ciudad(self):
        ciudad(self.root, self.db)

    # Esta funcion mostrara la informacion de pedido a partir de su archivo
    def __mostrar_pedido(self):
        pedido(self.root, self.db)

    # Esta funcion mostrara la informacion de pizza a partir de su archivo
    def __mostrar_pizza(self):
        pizza(self.root, self.db)

    # Esta funcion mostrara la informacion de vehiculo a partir de su archivo
    def __mostrar_vehiculo(self):
        vehiculo(self.root, self.db)

    # Esta funcion mostrara la informacion de repartidor a partir de su archivo
    def __mostrar_repartidor(self):
        repartidor(self.root, self.db)

def main():
    # Se conecta a la base de datos
    database = DB_pizzeria()

    # la aplicacion sera parte del parametro de la database
    aplicacion(database)

if __name__ == "__main__":
    main()
