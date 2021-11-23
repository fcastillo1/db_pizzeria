#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar Tkinter
import tkinter as tk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from PIL import Image, ImageTk

# Se importa database
from db_pizzeria import DB_pizzeria
from cliente import cliente

class App:
    def __init__(self, db):
        # Se actualiza atributo con la database
        self.db = db

        # Creación de ventana principal
        self.root = tk.Tk()
        self.root.geometry("700x500")
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
        # Se construyen algunos de los botones que son parte de la app
        boton_pedido = Button(self.root, text="Pedido", width=20, bg='snow', fg='black').place(x=15, y=20)
        boton_cliente = Button(self.root, text="Cliente", command = self.__mostrar_cliente, width=20 , bg='snow', fg='black').place(x=15, y=80)
        boton_pizza = Button(self.root, text="Pizza", width=20 , bg='snow', fg='black').place(x=15, y=140)
        boton_repartidor = Button(self.root, text="Repartidor", width=20 , bg='snow', fg='black').place(x=15, y=200)
        boton_vehiculo = Button(self.root, text="Vehiculo", width=20 , bg='snow', fg='black').place(x=15, y=260)
        boton_r = Button(self.root, text="Salir", command=self.root.destroy, width=20, bg='red', fg='white').place(x=350, y=400)

    def __crearMenu(self):
        menu_opciones = Menu(self.root)
        self.root.config(menu=menu_opciones)

        # se contruye el menu de la informacion con su color
        information_menu = Menu(menu_opciones, tearoff = 0, bg ="white")
        menu_opciones.add_cascade(label = "Informacion", menu=information_menu)
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

    def __agregarImagenInicial(self):
        frame = LabelFrame(self.root, text="", relief=tk.FLAT)
        # se define la ubicacion del frame
        frame.place(x=215, y=10)
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

def main():
    # Conecta a la base de datos
    db = DB_pizzeria()

    # App que toma como parámetro la database
    App(db)

if __name__ == "__main__":
    main()
