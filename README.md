# APLICACIÓN PIZZERIA IL ITALIANO
### Proyecto Base de Datos Unidad 3

La aplicación desarrollada es un programa que permite visualizar distintas áreas importantes de una pizzería ubicada en Talca. Esta app permite manejar diversos puntos e información relevante de los mismos, tal como:

* Clientes: Cuenta con el rut, nombre, apellido, teléfono, dirección y ciudad. Cada cliente cuenta con una única dirección en la base de datos, con el fin de realizar el reparto.
* Ciudades: Se maneja el nombre de la ciudad.
* Pedidos: Para cada pedido, se cuenta con un código (id), dinero total, cliente que ha efectuado el pedido, repartidor y el vehículo en el que se realiza la entrega.
* Repartidores: Cuenta con el rut, nombre, apellido y teléfono.
* Vehículos: Cuenta con un código (id), patente opcional en caso de que se trabaje con bicicleta y el tipo de vehículo (por ejemplo: moto, bicicleta o auto).
* Pizzas: Contiene información del código de la pizza, nombre de la pizza,tamaño y el precio correspondiente.

## Comenzando
### PROBLEMÁTICA
El desarrollo de la aplicación surge en función de la problemática que posee esta pizzería al momento de organizar el listado de pizzas que pueden vender, los pedidos que recibe, los clientes que realizan esos pedidos, los vehículos posee, el vehículo usado para cada pedido (y sus características), los repartidores que se encargan de transportar cada pedido, entre otros. Asimismo, es relevante mencionar que esta pizzería tiene la posibilidad de realizar repartos a Talca y Maule, por lo que es esencial contar con una forma eficiente de organización.

### DESARROLLO
El desarrollo de este proyecto ha contemplado los siguientes pasos:
1. Realizar un modelo en MySQL Workbench. En MySQL Workbench se ha conseguido identificar las distintas tablas necesarias para solucionar la problemática, las cuales son: CIUDAD, CLIENTE, PEDIDO, PEDIDO_HAS_PIZZA, PIZZA, TAMANO, REPARTIDOR, VEHICHULO y TIPO. 
2. Exportar esquema a MySQL. A partir de este modelo y de la generación de 9 tablas, se procede a exportar el diseño del esquema al servidor MySQL a una base de datos previamente creada en el mismo, la cual recibe el nombre de _db_pizzeria. 
3. Conectar la base de datos con la aplicación. Inicialmente, se ha creado un usuario con una clave específica para que este usuario cuente con todos los privilegios. Luego, se ha iniciado el trabajo de la aplicación como tal en Atom, utilizando Python y Tkinter, y en un archivo específico se ha realizado la conexión. A continuación, se listan los archivos trabajados:
* Relacionado con la conexión a la base de datos: db_pizzeria.py
** Archivo central o main: app_pizeria.py
* Extras: ayuda.py


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
  
2. Si la versión de Ubuntu es superior a 18.04, no debería problemas con las importaciones de librería pymol, necesaria para el desarrollo del programa y la visualización de las proteínas (obtiene el generado de la imagen del archivo PDB). Se puede instalar con el siguiente comando:
  * sudo apt-get install python3-pymol
  * En donde: Se descarga pymol para poder visualizar las estructuras sin problemas, en cuanto a la visualización del objeto indicado por el usuario.

### Lenguaje de programación
1. Corroborar la versión de Python disponible actualmente para poder ejecutar el código sin errores. 
  * Para conocer qué versión se está usando, se debe ingresar el siguiente comando en la terminal: python3
  * En donde: Se obtiene la versión de actual Python disponible. 
  * Si es superior a 3, el programa no presentará errores en su ejecución. Pero si es inferior, se debe:
   * Descargar desde este sitio la última versión de Python https://www.python.org/downloads/
   * Ejecutar el siguiente comando tar xvf python-3.8.5.tgz cd Python-3.8.5 ./configure --prefix= make -j4 make install
 
### Librerías
1. Instalar [algo]: 
* pip install mysql-connector-python
* 
2. Instalar [algo]: 
* pip install matplotlib

sudo apt-get install python3-pil.imagetk

## Ejecutando pruebas
Para implementar la ejecución del código, colocar en terminal: python3 app.py

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

