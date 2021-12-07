# APLICACIÓN PIZZERIA IL ITALIANO
### Proyecto Base de Datos Unidad 3

La aplicación desarrollada es un programa que permite visualizar distintas áreas importantes de una pizzería ubicada en Talca. Esta app permite manejar diversos puntos e información relevante de los mismos, tal como:

* Clientes: Cuenta con el rut, nombre, apellido, teléfono, dirección y ciudad. Cada cliente cuenta con una única dirección en la base de datos, con el fin de realizar el reparto.
* Ciudades: Se maneja el nombre de la ciudad.
* Pedidos: Para cada pedido, se cuenta con un código (id), dinero total, cliente que ha efectuado el pedido, repartidor y el vehículo en el que se realiza la entrega.
* Repartidores: Cuenta con el rut, nombre, apellido y teléfono.
* Vehículos: Cuenta con un código (id), patente opcional en caso de que se trabaje con bicicleta y el tipo de vehículo (por ejemplo: moto, bicicleta o auto).
* Pizzas: Contiene información del código de la pizza, nombre de la pizza,tamaño y el precio correspondiente.

Al ejecutar la app, el usuario observa un menú principal en la parte superior, bajo eso se presentan diversas opciones (CIUDAD, CLIENTE, PEDIDO, PIZZA, REPARTIDOR o VEHÍCULO). A continuación, se describe más sobre esto:
* Selección de CIUDAD: Se abre una ventana donde se pueden ingresar, modificar o eliminar ciudades.
* Selección de CLIENTE: Se abre una ventana donde se pueden ingresar, modificar o eliminar clientes. Es necesario que existan ciudades registradas antes de ingresar un cliente.
* Selección de PEDIDO: Se abre una ventana donde se pueden ingresar, modificar o eliminar pedidos. Es necesario que existan clientes, repartidores y vehículos registrados antes de ingresar un pedido.
* Selección de PIZZA: Se abre una ventana donde se pueden ingresar, modificar o eliminar pizzas. En la parte superior, hay un menú que tiene una opción para ingresar tamaños. Es necesario que existan tamaños antes de ingresar una pizza.
* Selección de REPARTIDOR: Se abre una ventana donde se pueden ingresar, modificar o eliminar repartidores.
* Selección de VEHÍCULO: Se abre una ventana donde se pueden ingresar, modificar o eliminar vehículos. En la parte superior, hay un menú que tiene una opción para ingresar tipos de vehículos. Es necesario que existan tipos antes de ingresar un vehículo.


## Comenzando
### PROBLEMÁTICA
El desarrollo de la aplicación surge en función de la problemática que posee esta pizzería al momento de organizar el listado de pizzas que pueden vender, los pedidos que recibe, los clientes que realizan esos pedidos, los vehículos posee, el vehículo usado para cada pedido (y sus características), los repartidores que se encargan de transportar cada pedido, entre otros. Asimismo, es relevante mencionar que esta pizzería tiene la posibilidad de realizar repartos a Talca y Maule, por lo que es esencial contar con una forma eficiente de organización.

### DESARROLLO
El desarrollo de este proyecto ha contemplado los siguientes pasos:
1. Realizar un modelo en MySQL Workbench. En MySQL Workbench se ha conseguido identificar las distintas tablas necesarias para solucionar la problemática, las cuales son: CIUDAD, CLIENTE, PEDIDO, PEDIDO_HAS_PIZZA, PIZZA, TAMANO, REPARTIDOR, VEHICHULO y TIPO. 
2. Exportar esquema a MySQL. A partir de este modelo y de la generación de 9 tablas, se procede a exportar el diseño del esquema al servidor MySQL a una base de datos previamente creada en el mismo, la cual recibe el nombre de _db_pizzeria. 
3. Conectar la base de datos con la aplicación. Inicialmente, se ha creado un usuario con una clave específica para que este cuente con todos los privilegios. Luego, se ha iniciado el trabajo de la aplicación como tal en Atom, utilizando Python y Tkinter, y en un archivo específico (db_pizzeria.py) se ha realizado la conexión. 
4. Diseñar interfaz gráfica. Para esto, se utilizan widgets de Tkinter y se generan diversas ventanas. Al ejecutar la aplicación, se abre una ventana principal en la que se ha puesto diversas opciones: CIUDAD, CLIENTE, PEDIDO, PIZZA, REPARTIDOR o VEHÍCULO. Además, en el menú superior puede acceder a información de la aplicación o a una pequeña ayuda para saber cómo funcionan algunos aspectos de la app. Para esto, se ha creado archivos para manejar las tablas de la base de datos y las otras ayudas, los que corresponden a:

* Relacionado con la conexión a la base de datos:
    * db_pizzeria.py
* Archivo central o main: 
    * app_pizeria.py
* Relacionados con las distintas áreas a manejar:
    * ciudad.py
    * cliente.py
    * pedido.py
    * vehiculo.py
    * tipo.py
    * pizza.py
    * tamano.py
    * repartidor.py
* Extras a los que se accede desde la ventana principal (menú superior):
    * ayuda.py
    * informacion.py

## Prerequisitos
* Sistema operativo Linux versión igual o superior a 18.04
* Editor de texto (Atom o vim)
* Lenguaje de programacion Python
* Librería Tkinter

## Instalación

### Sistema operativo
1. Para ejecutar el programa se debe conocer qué versión de Ubuntu presenta la computadora. 
  * Ejecutar comando: lsb_release -a (versión de Ubuntu)
  * En donde: Se corrobora qué versión se tiene instalada actualmente, debido a que se pueden presentar problemas si esta no es compatible con la aplicación que se está desarrollando. 
  
2. Si la versión de Ubuntu es superior a 18.04 no debería existir complicaciones.

### Lenguaje de programación
1. Corroborar la versión de Python disponible actualmente para poder ejecutar el código sin errores. 
  * Para conocer qué versión se está usando, se debe ingresar el siguiente comando en la terminal: python3
  * En donde: Se obtiene la versión de actual Python disponible. 
  * Si es superior a 3, el programa no presentará errores en su ejecución. Pero si es inferior, se debe:
   * Descargar desde este sitio la última versión de Python https://www.python.org/downloads/
   * Ejecutar el siguiente comando tar xvf python-3.8.5.tgz cd Python-3.8.5 ./configure --prefix= make -j4 make install
 
### Librerías
1. Instalar mysql-connector: 
* pip install mysql-connector-python
* 
2. Instalar matplotlib: 
* pip install matplotlib

sudo apt-get install python3-pil.imagetk

## Ejecutando pruebas

En MySQL se deben ejecutar los siguientes pasos:
1. Crear la base de datos: 
* create database db_pizzeria;
2. Cargar el archivo dump: 
* COMANDO
3. Crear el usuario que permite la conexión a la app:
* create user 'pizza'@'localhost' identified by 'Password123#@!';
* grant all privileges on db_pizzeria.* to 'pizza'@'localhost';
* flush privileges;

Fuera de MySQL, colocar en terminal: 
* python3 db_pizzeria.py

## Construido con:
* Ubuntu: Sistema operativo.
* Python: Lenguaje de programación.
* Atom: Editor de código.
* OTROS

## Versiones
### Versiones de herramientas: 
* Ubuntu 20.04 LTS 
* Atom 1.57.0 

### Versiones del desarrollo del código: 
* https://github.com/fcastillo1/db_pizzeria

## Autores
* Francisca Castillo - Desarrollo del código y proyecto, narración README. 
* Rocío Rodríguez - Desarrollo del código y proyecto, narración README.

## Expresiones de gratitud
A los ejemplos en la plataforma de Educandus de Alejandro Valdes: Tambien al ayudante del modulo por aclaracion de dudas y a la informacion obtenida algunas paginas web que se usaron para guiar el proceso las cuales son:
INGRESAR LINK!

