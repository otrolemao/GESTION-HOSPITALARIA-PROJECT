from conexion import conectar

def agendar_hora():
    print("\n--- AGENDAR HORA ---")
    
    conexion = conectar()
    if conexion is None:
        return
    
    try:
        cursor = conexion.cursor()
        
        # Aquí muestra a los pacientes
        cursor.execute("SELECT id_paciente, nombres, apellidos FROM tbl_paciente")
        pacientes = cursor.fetchall()
        
        if not pacientes:
            print("No hay pacientes registrados")
            return
        
        print("\nPacientes disponibles:")
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}. {paciente[1]} {paciente[2]}")
        
        
        opcion = int(input("\nSeleccione un paciente: "))
        
        if 1 <= opcion <= len(pacientes):
            id_paciente = pacientes[opcion-1][0]
            
            
            fecha = input("Fecha (YYYY-MM-DD): ")
            hora = input("Hora (HH:MM:SS): ")
            especialidad = input("Especialidad: ")
            medico = input("Médico: ")
            
            fecha_hora = f"{fecha} {hora}"
            
            
            cursor.execute("""
                INSERT INTO tbl_hora_medica (id_paciente, fecha_hora, especialidad, medico, estado)
                VALUES (%s, %s, %s, %s, 'Agendada')
            """, (id_paciente, fecha_hora, especialidad, medico))
            
            conexion.commit()
            print("Hora agendada correctamente")
            
        else:
            print("Opción inválida")
            
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    agendar_hora()