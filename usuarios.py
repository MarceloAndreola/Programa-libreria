#La clase usuario crea el usuario con una contraseña y correo el cual seran unicos
class Usuario:
    def __init__(self,id,nombre,correo,contraseña):
        self.id=id
        self.nombre=nombre
        self.correo=correo
        self.contraseña=contraseña

#Esta funcion lo que hace es devolver el objeto en forma de caracter con su nombre y correo
    def __str__(self):
        return f"{self.nombre} - {self.correo}"
