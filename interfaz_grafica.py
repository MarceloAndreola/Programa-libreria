#Lo que hacemos es llamar a la libreria tkinter y renombrarla tk por si la tenemos que llamar
import tkinter as tk
#Lo que hacemos al importar messagebox es importar mensajes que se nos van a mostrar en pantalla
from tkinter import messagebox
#Lo que hacemos aca es conectar esta carpeta con la base de datos
from libreria import ubicacion_conexion
from libreria import Biblioteca
from libros import Libro
from usuarios import Usuario


# Código de la interfaz gráfica usando Tkinter

#Clase de la interfaz principal
class libreriaApp:
    #En esta funcion con el constructor init lo que hacemos es crear una interfaz en la que vamos a trabajar y con title lo que hacemos es ponerle un titulo al interfaz
    def __init__(self,root):
        self.root=root
        self.root.title("Biblioteca")

        #Lo que hacemos aca es con el LABEL va a mostrar algo por pantalla que no se puede modificar, root lo que va hacer es decirle la ubicacion del label que va hacer en la interfaz principal, text el texto y lo que esta dentro de grid la posicion
        tk.Label(root, text="Título:").grid(row=0, column=0, padx=10, pady=10)
        #Lo que hacemos aca es con el entry poder ingresar datos por pantalla con el root decirle que es en la interfaz grafica y con el grid lo que hacemos es darle la posicion al entry
        self.titulo_entry = tk.Entry(root)
        self.titulo_entry.grid(row=0, column=1, padx=10, pady=10)

        #En este label hacemos lo mismo que en el de titulo pero con autor
        tk.Label(root, text="Autor:").grid(row=1, column=0, padx=10, pady=10)
        self.autor_entry = tk.Entry(root)
        self.autor_entry.grid(row=1, column=1, padx=10, pady=10)

        #En este label hacemos lo mismo en el de titulo pero con Año de publicacion
        tk.Label(root, text="Año de Publicación:").grid(row=2, column=0, padx=10, pady=10)
        self.anio_entry = tk.Entry(root)
        self.anio_entry.grid(row=2, column=1, padx=10, pady=10)

        #Esto lo que hace es crear un boton en la interfaz principal y con el command lo que hace es ir a libreria y buscar la funcion agregar_libro y con esa funcion ingresa a la base de datos para agregar el libro y con el grid le damos la posicion
        agregar_btn = tk.Button(root, text="Agregar Libro", command=self.agregar_libro)
        agregar_btn.grid(row=3, columnspan=2, padx=10, pady=10)


    #Lo que hacemos en esta funcion es tener los datos que ingresaron y guardarlo en titulo,autor,anio_publicacion
    def agregar_libro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        anio_publicacion = self.anio_entry.get()

        #En este if lo que hacemos es verificar si titulo, autor, anio_publicacion no estan vacios y insertar los datos en la base de datos sin que quede ningun valor vacio
        if titulo and autor and anio_publicacion:
            conn = ubicacion_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO libros (titulo, autor, anio_publicacion) VALUES (%s, %s, %s)",
                (titulo, autor, anio_publicacion)
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.limpiar_campos()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    #Lo que hacemos con esta funcion es ingresar con entry en donde se ingresa el texto y con 0 borrar el valor inicial y con tk.end borrar hasta el ultimo caracter
    def limpiar_campos(self):
            self.titulo_entry.delete(0, tk.END)
            self.autor_entry.delete(0, tk.END)
            self.anio_entry.delete(0, tk.END)

#Lo que hacemos es crear la interfaz grafica
root = tk.Tk()
app = libreriaApp(root)
root.mainloop()

