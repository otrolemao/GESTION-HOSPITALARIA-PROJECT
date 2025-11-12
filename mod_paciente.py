import mysql.connector
from mysql.connector import Error

class ModificarPaciente:
    def __init__(self):
        self.conexion = None
        
    def conectar_bd(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_hospital'
            )
            return True
        except Error as e:
            print("Error al conectar a la base de datos:", e)
            return False
    
    def buscar_paciente(self, rut):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_paciente WHERE rut = %s"
            cursor.execute(sql, (rut,))
            paciente = cursor.fetchone()
            cursor.close()
            return paciente
        except Error as e:
            print("Error al buscar paciente:", e)
            return None
    
    def mostrar_datos_paciente(self, paciente):
        if paciente:
            print("\n--- DATOS ACTUALES DEL PACIENTE ---")
            print(f"RUT: {paciente['rut']}")
            print(f"Nombres: {paciente['nombres']}")
            print(f"Apellidos: {paciente['apellidos']}")
            print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
            print(f"Sexo: {paciente['sexo']}")
        else:
            print("Paciente no encontrado")
    
    def modificar_paciente(self, rut):
        paciente = self.buscar_paciente(rut)
        if not paciente:
            print("Paciente no encontrado")
            return
        
        self.mostrar_datos_paciente(paciente)
        
        print("\n--- MODIFICAR DATOS ---")
        print("(Dejar en blanco para mantener el valor actual)")
        
        nuevo_nombre = input(f"Nuevo nombre [{paciente['nombres']}]: ") or paciente['nombres']
        nuevo_apellido = input(f"Nuevo apellido [{paciente['apellidos']}]: ") or paciente['apellidos']
        nueva_fecha = input(f"Nueva fecha nacimiento [{paciente['fecha_nacimiento']}]: ") or paciente['fecha_nacimiento']
        nuevo_sexo = input(f"Nuevo sexo [{paciente['sexo']}]: ") or paciente['sexo']
        
        try:
            cursor = self.conexion.cursor()
            sql = """
                UPDATE tbl_paciente 
                SET nombres = %s, apellidos = %s, fecha_nacimiento = %s, sexo = %s
                WHERE rut = %s
            """
            datos = (nuevo_nombre, nuevo_apellido, nueva_fecha, nuevo_sexo, rut)
            cursor.execute(sql, datos)
            self.conexion.commit()
            cursor.close()
            print("\n Paciente modificado correctamente")
        except Error as e:
            print("Error al modificar paciente:", e)
    
    def cerrar_conexion(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()

def main():
    modificar = ModificarPaciente()
    
    if modificar.conectar_bd():
        print("=== MODIFICAR DATOS DE PACIENTE ===")
        rut = input("Ingrese RUT del paciente a modificar: ")
        modificar.modificar_paciente(rut)
        modificar.cerrar_conexion()

if __name__ == "__main__":
    main()