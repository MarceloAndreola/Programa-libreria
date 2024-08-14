#La clase libro lo que hace es guardar un id(identificador unico), el titulo, autor, anio de publicacion y si esta disponible
class Libro:
    def __init__(self,id,titulo,autor,anio_publicacion,disponible):
        self.id=id
        self.titulo=titulo
        self.autor=autor
        self.anio_publicacion=anio_publicacion
        self.disponible=disponible
    
#En esta funcion tenemos un if para saber si el libro esta disponible y un str para ese objeto pasarlo a una cadena de texto
    def __str__(self):
        if self.disponible:
            estado = "Disponible" 
        else: 
            estado="No disponible"
        return f"{self.titulo} por el autor {self.autor} en el {self.anio_publicacion} - estado: {estado}"
        
