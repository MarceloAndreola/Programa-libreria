import mysql.connector

#Creo una funcion para la conexion y no una variable para poder reutilizar la funcion y si tengo que modificar algo solamente lo modifico desde esta funcion
def ubicacion_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="andreola2279",
        database="Libreria",
        port="3306"
    )

'''
#PRUEBA PARA VER SI SE REALIZO CORRECTAMENTE LA CONEXION
conector=ubicacion_conexion()
print(conector)
'''

#En esta parte del codigo voy a importar de la base de datos algunos datos que despues voy a necesitar en la funcion biblioteca
from libreria import ubicacion_conexion
from libros import Libro
from usuarios import Usuario
from datetime import datetime

#En biblioteca voy a usar conn para establecer la conexion con la base de datos y cursor lo voy a usar para poder selecionar,insertar,subir y eliminar datos
class Biblioteca:
    def __init__(self):
        self.conn=ubicacion_conexion()
        self.cursor=self.conn.cursor()

#En la funcion AGREGAR_LIBRO lo que hago es decirle que datos voy a insertar y en que posicion y despues decirle que valores son lo que voy a insertar y en values pongo (%s) para que no pueda haber inyeccion de datos

    def agregar_libro(self,titulo,autor,anio_publicacion):
        #self es de la instancia de la clase y cursor es para poder acceder desde python a la base de datos e interactuar y execute es el que le permite a cursor poder hacer las consultar a la base de datos
        self.cursor.execute(
            "INSERT INTO libros (titulo,autor,anio_publicacion) Values (%s,%s,%s)",
            (titulo,autor,anio_publicacion)
        )

#el self.conn es una conexion a la base de datos para poder ejecutar los comandos SQL y commit es para guardar los datos de forma permanente
    def eliminar_libro(self,libro_id):
        self.cursor.execute("DELETE FROM libros WHERE id=%s", (libro_id,))
        self.conn.commit()
        

    def listar_libros(self):
        #Le pedimos toda la informacion de libros
        self.cursor.execute("SELECT *FROM libros")
        #Tiene todos los resultados de la consulta 
        libros=self.cursor.fetchall()

        #Creo una lista para poder guardar los datos del libro y si esta disponible
        lista_libros=[]

        #Con el FOR voy a recorrer libros y le doy una posicion especifica a cada dato de libros
        for libro in libros:
            id=libro[0]
            titulo=libro[1]
            autor=libro[2]
            anio_publicacion=libro[3]
            disponible=libro[4]

            libro_objeto=(id,titulo,autor,anio_publicacion,disponible)

            lista_libros.append(libro_objeto)

            return lista_libros

    def agregar_usuario(self,nombre,correo,contrasena):
        self.cursor.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)",
            (nombre, correo, contrasena)
        )
        self.conn.commit()

    def eliminar_usuario(self,usuario_id):
        self.cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        self.conn.commit()

    def registrar_prestamo(self,libro_id,usuario_id):
        self.cursor.execute("SELECT disponible FROM libros WHERE id = %s", (libro_id,))
        #Lo que hago en la variable disponible es ingresar a la base de datos con self.cursor y con fetchone()[0] lo que hago es ir a buscar a la tupla un unico valor de disponible que seria True o False.
        disponible = self.cursor.fetchone()[0]
        #Creo un if por que si el libro esta prestado con el rise exception lo que hago es corta la funcion y mandar un mensaje de que esta prestado
        if not disponible:
            raise Exception("El libro ya está prestado")
        #Si la condicion if no se cumple lo que se hace es seguir con la ejecucion de la funcion en la cual guardamos en una variable la fecha actual en la que prestamos el libro
        fecha_prestamo = datetime.now().date()
        #Lo que hacemos aca es ingresar mediante el cursor a la base de datos y con el execute poder realizar la accion en la base de datos y con el VALUES(%s) lo que hacemos es asegurarnos de que no pueda haber inyeccion de datos
        self.cursor.execute(
            "INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo) VALUES (%s, %s, %s)",
            (libro_id, usuario_id, fecha_prestamo)
        )
        #Lo que hacemos es volver a ingresar a la base de datos pero esta vez para modificar un valor que seria DISPONIBLE que pasa de True a False (libro no disponible) y en commit lo guarda de forma definitiva
        self.cursor.execute("UPDATE libros SET disponible = FALSE WHERE id = %s", (libro_id,))
        self.conn.commit()

    def devolver_libro(self,libro_id):
        #Lo que hago aca es ingresar a la base de datos para realizar una busqueda con (libro_id=%s) buscando la posicion del libro y con fecha_devolucion is NULL es saber si es libro no esta prestado
        self.cursor.execute("SELECT * FROM prestamos WHERE libro_id = %s AND fecha_devolucion IS NULL", (libro_id,))
        #Lo que hago aca es buscar todos los datos de la persona a la cual se le presto el libro
        prestamo = self.cursor.fetchone()
        #Este if lo que hace es que si no esta prestado cortar la ejecucion de la funcion y mandar un mensaje
        if not prestamo:
            raise Exception("El libro no está prestado")
        #Lo que hacemos aca es guardar en prestamo_id guardar la posicion y el dato de prestamo
        prestamo_id = prestamo[0]
        #Lo que hace esto es ingresar a la base de datos para ingresar la fecha de devolucion y guardar la fecha actual y ademas ingresar que libro es el que se guardo y cambiar el valor de disponible a True
        self.cursor.execute("UPDATE prestamos SET fecha_devolucion = %s WHERE id = %s", (datetime.now().date(), prestamo_id))
        self.cursor.execute("UPDATE libros SET disponible = TRUE WHERE id = %s", (libro_id,))
        self.conn.commit()
        

    def informacion_libro(self,libro_id):
        #Con el cursor execute lo que hacemos es ingresar a la base de datos y con el SELECT *FROM lo que hacemos es seleccionar todo lo de libros y con WHERE ID=%s libro_id lo que hacemos es filtrar en donde esta la informacion que buscamos
        self.cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
        #Con fetchone lo que hacemos es verificar si existe algun valor y si no existe devolver un none
        libro = self.cursor.fetchone()
        #Con el if lo que hacemos es si es TRUE retornamos toda la informacion de libro y si es FALSE retorna NONE
        if libro:
            return Libro(*libro)
        return None

    def informacion_usuario(self,usuario_id):
        #Lo que hacemos aca es hacer lo mismo que en la funcion informacion_libro pero con usuario_id
        self.cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = self.cursor.fetchone()
        if usuario:
            return Usuario(*usuario)
        return None

    #Lo que hacemos es cerrar el cursor con el que se hacian las consultar a la base de datos y con el metodo conn cerramos la conexion con la base de datos esto hace que el sistema no quede con datos ocupados que no son necesarios y que sea mas eficiente el programa
    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()


