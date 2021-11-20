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

        # Empieza a correr la interfaz.
        self.root.mainloop()

def main():
    # Conecta a la base de datos
    db = DB_pizzeria()

    # App que toma como parámetro la database
    App(db)

if __name__ == "__main__":
    main()
