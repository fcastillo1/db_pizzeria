# Importar Tkinter
import tkinter as tk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from PIL import Image, ImageTk

# Se importa database
from db_pizzeria import DB_pizzeria

class App:
    def __init__(self, db):
        # Se actualiza atributo con la database
        self.db = db

        # Creación de ventana principal
        self.root = tk.Tk()
        self.root.geometry("800x550")

        # Título de la ventana
        self.root.title("APP Pizzería L'italiano")

        boton_pedido = Button(self.root, text="Pedido", width=20).grid(column=0, row=1)
        boton_cliente = Button(self.root, text="Cliente", width=20).grid(column=0, row=2)
        boton_pizza = Button(self.root, text="Pizza", width=20).grid(column=0, row=3)
        boton_repartidor = Button(self.root, text="Repartidor", width=20).grid(column=0, row=4)
        boton_vehiculo = Button(self.root, text="Vehiculo", width=20).grid(column=0, row=5)

        # Se define la funcionalidad para que boton salir funcione
        def cerrar_ventana():
            self.root.destroy()
        # cambiar el grid x pack
        boton_salir = Button(self.root, text="Salir", command=cerrar_ventana).grid(column=10, row=10)

        #def mostrar_informacion():
        #    self.root.destroy()
        #boton_informacion = Button(self.root, text="Informacion", width=20, command=mostrar_informacion).grid(column=15, row=15)

        # Empieza a correr la interfaz.
        self.root.mainloop()

def main():
    # Conecta a la base de datos
    db = DB_pizzeria()

    # App que toma como parámetro la database
    App(db)

if __name__ == "__main__":
    main()
