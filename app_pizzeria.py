#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar Tkinter
import tkinter as tk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import PhotoImage
from PIL import Image, ImageTk


# Se importa database
from db_pizzeria import DB_pizzeria
from cliente import cliente
from ciudad import ciudad
from pizza import pizza

class App:
    def __init__(self, db):
        # Se actualiza atributo con la database
        self.db = db

        # Creación de ventana principal
        self.root = tk.Tk()
        self.root.geometry("750x550")
        # Título de la ventana
        self.root.title("APP Pizzería l'italiano")
        # Se añade color al fondo de la ventana
        self.root.config(bg="light cyan")

        self.__crearBotones()
        # Se crea mediante self._ el menu de opciones utiles para el usuario
        self.__crearMenu()
        self.__agregarImagenInicial()

        # Empieza a correr la interfaz.
        self.root.mainloop()


    def __crearBotones(self):
        #imagen boton ciudad
        image_ciudad = Image.open("/home/francisca/Documentos/db_pizzeria-main/ciudad.jpg")
        image_ciudad = image_ciudad.resize((63, 45), Image.ANTIALIAS)
        self.reset_img1 = ImageTk.PhotoImage(image_ciudad)

        #imagen boton pedido
        image_pedido = Image.open("/home/francisca/Documentos/db_pizzeria-main/pedido.jpg")
        image_pedido = image_pedido.resize((63, 45), Image.ANTIALIAS)
        self.reset_img2 = ImageTk.PhotoImage(image_pedido)

        #imagen boton cliente
        image_cliente = Image.open("/home/francisca/Documentos/db_pizzeria-main/cliente.jpg")
        image_cliente = image_cliente.resize((63, 45), Image.ANTIALIAS)
        self.reset_img3 = ImageTk.PhotoImage(image_cliente)

        #imagen boton pizza
        image_pizza = Image.open("/home/francisca/Documentos/db_pizzeria-main/pizza.jpg")
        image_pizza = image_pizza.resize((63, 45), Image.ANTIALIAS)
        self.reset_img4 = ImageTk.PhotoImage(image_pizza)
        image_cliente = Image.open("/home/francisca/Documentos/db_pizzeria-main/cliente.jpg")
        image_cliente = image_cliente.resize((63, 45), Image.ANTIALIAS)
        self.reset_img3 = ImageTk.PhotoImage(image_cliente)

        #imagen boton pizza
        image_pizza = Image.open("/home/francisca/Documentos/db_pizzeria-main/pizza.jpg")
        image_pizza = image_pizza.resize((63, 45), Image.ANTIALIAS)
        self.reset_img4 = ImageTk.PhotoImage(image_pizza)

        #imagen boton repartidor
        image_repartidor = Image.open("/home/francisca/Documentos/db_pizzeria-main/repartidor.jpg")
        image_repartidor = image_repartidor.resize((63, 45), Image.ANTIALIAS)
        self.reset_img5 = ImageTk.PhotoImage(image_repartidor)

        #imagen boton repartidor
        image_repartidor = Image.open("/home/francisca/Documentos/db_pizzeria-main/repartidor.jpg")
        image_repartidor = image_repartidor.resize((63, 45), Image.ANTIALIAS)
        self.reset_img5 = ImageTk.PhotoImage(image_repartidor)

        #imagen boton vehiculo
        image_vehiculo = Image.open("/home/francisca/Documentos/db_pizzeria-main/vehiculo.jpg")
        image_vehiculo = image_vehiculo.resize((63, 45), Image.ANTIALIAS)
        self.reset_img6 = ImageTk.PhotoImage(image_vehiculo)

        # creacion de los botones
        boton_ciudad = Button(self.root, text = "Ciudades", image = self.reset_img1, compound = 'top', command = self.__mostrar_ciudad, width=135, bg='snow', fg='black').place(x=10, y=10)
        boton_cliente = Button(self.root, text ="Cliente",  image = self.reset_img2, compound = 'top', command = self.__mostrar_cliente, width=135 , bg='snow', fg='black').place(x=10, y=95)
        boton_pedido = Button(self.root, text ="Pedido",  image = self.reset_img3, compound = 'top',width=135, bg='snow', fg='black').place(x=10, y=180)
        boton_pizza = Button(self.root, text ="Pizza", image = self.reset_img4, compound = 'top', width=135 , bg='snow', fg='black', command = self.__mostrar_pizza).place(x=10, y=265)
        boton_repartidor = Button(self.root, text ="Repartidor",  image = self.reset_img5, compound = 'top', width=135 , bg='snow', fg='black').place(x=10, y=350)
        boton_vehiculo = Button(self.root, text ="Vehiculo",  image = self.reset_img6, compound = 'top', width=135 , bg='snow', fg='black').place(x=10, y=435)
        boton_salir = Button(self.root, text ="Salir", command=self.root.destroy, width=20, bg='red', fg='white').place(x=375, y=475)

    def __crearMenu(self):
        menu_opciones = Menu(self.root)
        self.root.config(menu=menu_opciones)

        # se contruye el menu de la informacion con su color
        information_menu = Menu(menu_opciones, tearoff = 0, bg ="white")
        menu_opciones.add_cascade(label = "Información", menu=information_menu)
        # dentro del boton de informacion, existira uno que detalle acerca de la app y desarrolladores
        information_menu.add_command(label = "Acerca de App")
        # se genera un espacio
        information_menu.add_separator()
        # se genera un boton r, que pirmitira destuir la ventana
        information_menu.add_command(label = "Salir", command=self.root.destroy)

        # se contruye el menu de ayuda con su color
        help_menu = Menu(menu_opciones, tearoff = 0, bg="white")
        menu_opciones.add_cascade(label = "Ayuda", menu=help_menu)
        # dentro del boton de AYUDA, existira uno que detalle para guiar al usuario
        help_menu.add_command(label = "Ayuda")

    def __mostrar_informacion(self):
        ventana(self.root, self.db)

    def __agregarImagenInicial(self):
        frame = LabelFrame(self.root, text="", relief=tk.FLAT)
        # se define la ubicacion del frame
        frame.place(x = 240, y=60)
        # se define cual sera la imagen de la pizzeria a partir de un archivo
        imagen_pizzeria = "imagenpizza.jpg"
        # se abirira la imagen obtenida
        image = Image.open(imagen_pizzeria)
        # se define el tamaño de la imagen
        photo = ImageTk.PhotoImage(image.resize((450, 350), Image.ANTIALIAS))
        # se hace un label con el frame e imagen
        label = Label(frame, image=photo)
        label.image = photo
        label.pack()

    def __mostrar_cliente(self):
        cliente(self.root, self.db)

    def __mostrar_ciudad(self):
        ciudad(self.root, self.db)

    def __mostrar_pizza(self):
        pizza(self.root, self.db)

def main():
    # Conecta a la base de datos
    db = DB_pizzeria()

    # App que toma como parámetro la database
    App(db)

if __name__ == "__main__":
    main()

