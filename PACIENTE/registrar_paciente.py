import mysql.connector
from mysql.connector import Error
from datetime import datetime

class FormularioPaciente:
    def __init__(self):
        self.rut = ""
        self.nombres = ""
        self.apellidos = ""
        self.fecha_nacimiento = ""
        self.sexo = ""
        self.direccion = ""
        self.telefono = ""
        self.correo = ""

    def el_input(self):
        print("=== REGISTRO DE PACIENTE ===")
        self.rut = input("RUT: ")
        self.nombres = input("Nombres: ")
        self.apellidos = input("Apellidos: ")
        self.fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
        self.sexo = input("Sexo (Masculino/Femenino/Otro): ")
        self.direccion = input("Dirección: ")
        self.telefono = input("Teléfono: ")
        self.correo = input("Correo: ")

    def guardar_en_bd(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',          # cambia si usas otro usuario
                password='',           # tu contraseña si tienes
                database='db_hospital' # usa el nombre de tu base de datos
            )

            if conexion.is_connected():
                cursor = conexion.cursor()
                sql = """
                    INSERT INTO tbl_paciente
                    (rut, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, correo, fecha_registro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                datos = (
                    self.rut,
                    self.nombres,
                    self.apellidos,
                    self.fecha_nacimiento,
                    self.sexo,
                    self.direccion,
                    self.telefono,
                    self.correo,
                    datetime.now()
                )
                cursor.execute(sql, datos)
                conexion.commit()
                print("\n Paciente registrado correctamente en la base de datos.")

        except Error as e:
            print("Error al conectar o guardar en MySQL:", e)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

# RUN
if __name__ == "__main__":
    paciente = FormularioPaciente()
    paciente.el_input()
    paciente.guardar_en_bd()
