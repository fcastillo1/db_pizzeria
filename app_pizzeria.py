import tkinter as tk
from tkinter import Menu
from tkinter import LabelFrame, Label, Frame
from tkinter import Button
from PIL import Image, ImageTk

#
from db_pizzeria import DB_pizzeria
#from graficos import graficos
from cliente import cliente
#from equipo import equipo
class App:
    def __init__(self, db):
        self.db = db

        # Main window
        self.root = tk.Tk()
        #self.master = master

        # Algunas especificaciones de tamaño y título de la ventana
        self.root.geometry("700x500") # se define tamaño de la ventana
        self.root.title(" APP Pizzeria l'italiano ") # se añade el titulo de la app
        self.root.config(bg="light cyan") # se añade color al fondo de la ventana

        # se crea mediante self._ el menu de opciones utiles para el usuario
        self.__crearMenu()
        self.__crearBotones()
        self.__agregarImagenInicial()

        # Empieza a correr la interfaz.
        self.root.mainloop()

        # Se crea una funcion que nos permitira tener el menu
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
        # se genera un boton salir, que pirmitira destuir la ventana
        information_menu.add_command(label = "Salir", command=self.root.destroy)

        # se contruye el menu de ayuda con su color
        help_menu = Menu(menu_opciones, tearoff = 0, bg="white")
        menu_opciones.add_cascade(label = "Ayuda", menu=help_menu)
        # dentro del boton de AYUDA, existira uno que detalle para guiar al usuario
        help_menu.add_command(label = "Ayuda")


        # esta funcion permite que se carge la imagen de inicio de la app
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

    def __crearBotones(self):
        # se construyen algunos de los botones que son parte de la app
        boton_pedido = Button(self.root, text="Pedido", width=20).place(x=15, y=20)
        boton_cliente = Button(self.root, text="Cliente", width=20, command=self.__mostrar_cliente).place(x=15, y=80)
        boton_pizza = Button(self.root, text="Pizza", width=20).place(x=15, y=140)
        boton_repartidor = Button(self.root, text="Repartidor", width=20).place(x=15, y=200)
        boton_vehiculo = Button(self.root, text="Vehiculo", width=20).place(x=15, y=260)

        # Se define la funcionalidad para que boton salir funcione
        # se genera un boton para salir (cerrar app)
        boton_salir = Button(self.root, text="Salir", command=self.root.destroy, width=20).place(x=350, y=400)

    # muestra ventana equipos.
    def __mostrar_cliente(self):
        cliente(self.root, self.db)

    # muestra ventana jugadores.
    #def __mostrar_jugadores(self, button):
    #    jugador(self.root, self.db)

    #def __graficos(self, button):
    #    graficos(self.root, self.db)

def main():
    # Conecta a la base de datos
    db = DB_pizzeria()

    # La app xD
    App(db)

if __name__ == "__main__":
    main()
