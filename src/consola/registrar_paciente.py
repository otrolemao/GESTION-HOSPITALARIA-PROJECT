import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

# FUNCIONES DE VALIDACIÓN
def validar_rut(rut):
    patron = r'^\d{7,8}-[\dkK]$'
    return re.match(patron, rut) is not None

def validar_nombre(nombre):
    return nombre.replace(' ', '').isalpha() and len(nombre) >= 2

def validar_fecha_nacimiento(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validar_sexo(sexo):
    opciones_validas = ['Masculino', 'Femenino', 'Otro']
    return sexo in opciones_validas

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9

def validar_email(email):
    if not email:
        return True
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

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
        
        while True:
            self.rut = input("RUT (formato: 12345678-9): ").strip()
            if validar_rut(self.rut):
                break
            print("RUT invalido. Use formato: 12345678-9")
        
        while True:
            self.nombres = input("Nombres: ").strip()
            if validar_nombre(self.nombres):
                break
            print("Solo letras y espacios, minimo 2 caracteres")
        
        while True:
            self.apellidos = input("Apellidos: ").strip()
            if validar_nombre(self.apellidos):
                break
            print("Solo letras y espacios, minimo 2 caracteres")
        
        while True:
            self.fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            if validar_fecha_nacimiento(self.fecha_nacimiento):
                break
            print("Formato invalido. Use: YYYY-MM-DD")
        
        while True:
            print("Opciones: Masculino, Femenino, Otro")
            self.sexo = input("Sexo: ").strip().capitalize()
            if validar_sexo(self.sexo):
                break
            print("Opcion invalida. Elija entre: Masculino, Femenino, Otro")
        
        self.direccion = input("Direccion: ").strip()
        
        while True:
            self.telefono = input("Telefono (9 digitos): ").strip()
            if validar_telefono(self.telefono):
                break
            print("Telefono debe tener 9 digitos")
        
        while True:
            self.correo = input("Correo (opcional): ").strip()
            if not self.correo or validar_email(self.correo):
                break
            print("Formato de email invalido")

    def guardar_en_bd(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_hospital'
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
                print("Paciente registrado correctamente.")

        except Error as e:
            print("Error al conectar o guardar en MySQL:", e)
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

if __name__ == "__main__":
    paciente = FormularioPaciente()
    paciente.el_input()
    paciente.guardar_en_bd()