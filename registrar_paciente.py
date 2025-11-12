class FormularioPaciente:
    def __init__(self, rut="", nombre="", apellido="", edad=0, genero="", telefono="", email="", direccion=""):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    def el_input(self):
        print("=== REGISTRO DE PACIENTE ===")
        self.rut = input("RUT: ")
        self.nombre = input("Nombre: ")
        self.apellido = input("Apellido: ")
        self.edad = int(input("Edad: "))
        self.genero = input("Genero: ")
        self.telefono = input("Telefono: ")
        self.email = input("Email: ")
        self.direccion = input("Direccion: ")
        print("[PACIENTE REGISTRADO 100%]")
        print(f"RUT: {self.rut}")
        print(f"Nombre: {self.nombre} {self.apellido}")

# RUN
if __name__ == "__main__":
    paciente = FormularioPaciente()
    paciente.el_input()