#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importan librerias principales a usar en Tkinter
import tkinter as tk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Se importan todos los archivos con sus clases
from db_pizzeria import DB_pizzeria
from cliente import cliente
from ciudad import ciudad
from pizza import pizza
from tamano import tamano
from vehiculo import vehiculo
from tipo import tipo
from repartidor import repartidor
from detalle import detalle
from pedido import pedido
from informacion import informacion
from ayuda import ayuda
from resumen_pedido import resumen_pedido
from detalle_tipo import detalle_tipo
from filtro_precio_pizza import filtro_precio_pizza
from filtro_nombre_cliente import filtro_nombre_cliente
from histograma import histograma
from filtro_rep_tiempo import filtro_rep_tiempo
from vista_rep_veh import vista_rep_veh
from vista_clie_ciudad import vista_clie_ciudad

# Se define la clase que es de la aplicación y permite su uso
class aplicacion:
    def __init__(self, db):
        # Se actualiza atributo con la database
        self.db = db

        # Creación de ventana principal
        self.root = tk.Tk()
        # Se define el tamaño de la ventana
        self.root.geometry("875x550")
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

    # Esta funcion permite la creación de los botones principales de la app
    def __crearBotones(self):
        # Se sube una Imagen al botón ciudad
        image_ciudad = Image.open("ciudad.jpg")
        image_ciudad = image_ciudad.resize((63, 45), Image.ANTIALIAS)
        self.reset_img1 = ImageTk.PhotoImage(image_ciudad)

        # Se sube una Imagen al botón cliente
        image_cliente = Image.open("cliente.jpg")
        image_cliente = image_cliente.resize((63, 45), Image.ANTIALIAS)
        self.reset_img2 = ImageTk.PhotoImage(image_cliente)

        # Se sube una Imagen al botón tipo
        image_tipo = Image.open("tipo.jpg")
        image_tipo = image_tipo.resize((63, 45), Image.ANTIALIAS)
        self.reset_img3 = ImageTk.PhotoImage(image_tipo)

        # Se sube una Imagen al botón vehículo
        image_vehiculo = Image.open("vehiculo.jpg")
        image_vehiculo = image_vehiculo.resize((63, 45), Image.ANTIALIAS)
        self.reset_img4 = ImageTk.PhotoImage(image_vehiculo)

        # Se sube una Imagen al botón repartidor
        image_repartidor = Image.open("repartidor.jpg")
        image_repartidor = image_repartidor.resize((63, 45), Image.ANTIALIAS)
        self.reset_img5 = ImageTk.PhotoImage(image_repartidor)

        # Se sube una Imagen al botón tamaño
        image_tamano = Image.open("tamano.jpg")
        image_tamano = image_tamano.resize((63, 45), Image.ANTIALIAS)
        self.reset_img6 = ImageTk.PhotoImage(image_tamano)

        # Se sube una Imagen al botón pizza
        image_pizza = Image.open("pizza.jpg")
        image_pizza = image_pizza.resize((63, 45), Image.ANTIALIAS)
        self.reset_img7 = ImageTk.PhotoImage(image_pizza)

        # Se sube una Imagen al botón pedido
        image_pedido = Image.open("pedido.jpg")
        image_pedido = image_pedido.resize((63, 45), Image.ANTIALIAS)
        self.reset_img8 = ImageTk.PhotoImage(image_pedido)

        # Se sube una Imagen al botón detalle
        image_detalle = Image.open("detalle.jpg")
        image_detalle = image_detalle.resize((63, 45), Image.ANTIALIAS)
        self.reset_img9 = ImageTk.PhotoImage(image_detalle)


        # Creación de los botones principales
        # Creación botón ciudad con su texto e información para su funcionamiento
        boton_ciudad = Button(self.root, text = "Ciudad", image = self.reset_img1, compound = 'top',
        command = self.__mostrar_ciudad, width=140, bg='snow', fg='black').place(x=20, y=40)

        # Creación botón cliente con su texto e información para su funcionamiento
        boton_cliente = Button(self.root, text = "Cliente",  image = self.reset_img2, compound = 'top',
        command = self.__mostrar_cliente, width=140 , bg='snow', fg='black').place(x=200, y = 40)

        # Creación botón pedido con su texto e información para su funcionamiento
        boton_pedido = Button(self.root, text = "Tipo Vehículo",  image = self.reset_img3, compound = 'top',
        command = self.__mostrar_tipo,  width=140, bg='snow', fg='black').place(x=20, y = 130)

        # Creación botón detalle con su texto e información para su funcionamiento
        boton_pedido = Button(self.root, text = "Vehículo", image = self.reset_img4, compound = 'top',
        command = self.__mostrar_vehiculo,  width=140, bg='snow', fg='black').place(x=200, y = 130)

        # Creación botón pizza con su texto e información para su funcionamiento
        boton_pizza = Button(self.root, text = "Repartidor", image = self.reset_img5, compound = 'top',
        command = self.__mostrar_repartidor, width=140 , bg='snow', fg='black').place(x=20, y=220)

        # Creación botón tamaño con su texto e información para su funcionamiento
        boton_pizza = Button(self.root, text = "Tamaño Pizza", image = self.reset_img6, compound = 'top',
        command = self.__mostrar_tamano, width=140 , bg='snow', fg='black').place(x=200, y=220)

        # Creación botón cvehículo con su texto e información para su funcionamiento
        boton_vehiculo = Button(self.root, text = "Pizza",  image = self.reset_img7, compound = 'top',
        command = self.__mostrar_pizza, width=140 , bg='snow', fg='black').place(x=20, y=310)

        # Creación botón tipo con su texto e información para su funcionamiento
        boton_vehiculo = Button(self.root, text = "Pedido", image = self.reset_img8, compound = 'top',
        command = self.__mostrar_pedido, width=140 , bg='snow', fg='black').place(x=200, y=310)

        # Creación botón repartidor con su texto e información para su funcionamiento
        boton_repartidor = Button(self.root, text = "Detalle Pedido",  image = self.reset_img9, compound = 'top',
        command = self.__mostrar_detalle, width=140 , bg='snow', fg='black').place(x=115, y=400)

        # Creación botón salir que permite cierre de la app
        boton_salir = Button(self.root, text = "Salir", command = self.root.destroy,
        width=25, bg='red', fg='white').place(x=515, y=475)


    # Método permite crear el menú de opciones
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

        # Se genera un botón para destruir la ventana
        info_menu.add_command(label = "Salir", command = self.root.destroy)

        # Botón de vistas
        vistas_menu = Menu(menu_opciones, tearoff = 0, bg = "white")
        menu_opciones.add_cascade(label = "Vistas", menu = vistas_menu)

        # Despliegue de las vistas
        # vistas_menu.add_command(label = "Resumen pedido", command = self.__mostrar_vista_pedido)
        # vistas_menu.add_command(label = "Resumen tipo", command = self.__mostrar_vista_vehiculo)
        vistas_menu.add_command(label = "Pedido x repartidor x vehículo", command = self.__mostrar_vista_rep_veh)
        vistas_menu.add_command(label = "Pedido x cliente x ciudad", command = self.__mostrar_vista_clie_ciudad)

        # Se genera un menú con las opciones de las gráficas
        graficas_menu = Menu(menu_opciones, tearoff = 0, bg = "white")
        menu_opciones.add_cascade(label = "Gráficas", menu = graficas_menu)

        # Se muestran las opciones del menú con las distintas gráficas (histograma)
        graficas_menu.add_command(label = "Histograma", command = self.__mostrar_histograma)
        graficas_menu.add_command(label = "Pie", command = self.__mostrar_rep_tiempo)

        # Se genera un espacio
        graficas_menu.add_separator()

        graficas_menu.add_command(label = "Graficas Dinamicas 1")
        graficas_menu.add_command(label = "Graficas Dinamicas 2")

        # Opción de consultas dinámicas
        dinamicas_menu = Menu(menu_opciones, tearoff = 0, bg = "white")
        menu_opciones.add_cascade(label = "Dinámicas", menu = dinamicas_menu)

        # Consulta para filtrar pizzas por precio
        dinamicas_menu.add_command(label = "Precio pizza", command = self.__mostrar_precio_pizza)
        dinamicas_menu.add_command(label = "Nombre de cliente", command = self.__mostrar_capacidad_tipo)

        # Se construye el menú de ayuda con su color
        help_menu = Menu(menu_opciones, tearoff = 0, bg = "white")
        menu_opciones.add_cascade(label = "Ayuda", menu = help_menu)

        # Dentro del botón de AYUDA, existirá uno para guiar al usuario
        help_menu.add_command(label = "Ayuda", command = self.__mostrar_ayuda)

    # Esta funcion permite anadir una imagen a la aplicacion
    def __agregarImagenInicial(self):
        frame = LabelFrame(self.root, text = "\t \t APLICACIÓN PIZZERÍA IL ITALIANO \t", relief = tk.FLAT)
        # Se define la ubicación del frame
        frame.place(x = 400, y = 60)

        # Imagen principal de la ventana abierta a partir de un archivo
        image = Image.open("imagenpizza.jpg")

        # Se define el tamaño de la imagen
        photo = ImageTk.PhotoImage(image.resize((450, 350), Image.ANTIALIAS))
        # Se hace un label con el frame e imagen
        label = Label(frame, image = photo)
        label.image = photo
        label.pack()

    # Muestra info de la base de datos y llama a la clase informacion
    def __mostrar_informacion(self):
        informacion(self.root, self.db)

    # Muestra info de ayuda y llama a la clase ayuda a partir de archivo
    def __mostrar_ayuda(self):
        ayuda(self.root, self.db)

    # Muestra info de cliente y llama a la clase cliente a partir de archivo
    def __mostrar_cliente(self):
        cliente(self.root, self.db)

    # Muestra info de ciudad y llama a la clase ciudad a partir de archivo
    def __mostrar_ciudad(self):
        ciudad(self.root, self.db)

    # Muestra info de pedido y llama a la clase pedido a partir de archivo
    def __mostrar_pedido(self):
        pedido(self.root, self.db)

    # Muestra info de detalle y llama a la clase detalle a partir de archivo
    def __mostrar_detalle(self):
        detalle(self.root, self.db)

    # Muestra info de pizza y llama a la clase pizza a partir de archivo
    def __mostrar_pizza(self):
        pizza(self.root, self.db)

    # Muestra info de tamaño y llama a la clase tamano a partir de archivo
    def __mostrar_tamano(self):
        tamano(self.root, self.db)

    # Muestra info de vehículo y llama a la clase vehiculo a partir de archivo
    def __mostrar_vehiculo(self):
        vehiculo(self.root, self.db)

    # Muestra info de tipo y llama a la clase tipo a partir de archivo
    def __mostrar_tipo(self):
        tipo(self.root, self.db)

    # Muestra info de repartidor y llama a la clase repartidor a partir de archivo
    def __mostrar_repartidor(self):
        repartidor(self.root, self.db)

    # Muestra info de resumen_pedido y llama a la clase resumen_pedido a partir de archivo
    # def __mostrar_vista_pedido(self):
    #     resumen_pedido(self.root, self.db)

    # Muestra info de detalle_tipo y llama a la clase detalle_tipo a partir de archivo
    # def __mostrar_vista_vehiculo(self):
    #     detalle_tipo(self.root, self.db)

    # Muestra info de vista_rep_veh
    def __mostrar_vista_rep_veh(self):
        vista_rep_veh(self.root, self.db)

    # Muestra info de vista_clie_ciudad
    def __mostrar_vista_clie_ciudad(self):
        vista_clie_ciudad(self.root, self.db)

    # Muestra info de filtro_precio_pizza y llama a la clase filtro_precio_pizza a partir de archivo
    def __mostrar_precio_pizza(self):
        filtro_precio_pizza(self.root, self.db)

    # Muestra info de filtro_nombre_cliente y llama a la clase filtro_nombre_cliente a partir de archivo
    def __mostrar_capacidad_tipo(self):
        filtro_nombre_cliente(self.root, self.db)

    # Muestra info de histograma y llama a la clase histograma a partir de archivo
    def __mostrar_histograma(self):
        histograma(self.root, self.db)

    # Muestra info de pie plot y llama a la clase filtro_rep_tiempo
    def __mostrar_rep_tiempo(self):
        filtro_rep_tiempo(self.root, self.db)

def main():
    # Se conecta a la base de datos
    database = DB_pizzeria()

    # La db se pasa como parámetro a la clase aplicación
    aplicacion(database)

if __name__ == "__main__":
    main()
