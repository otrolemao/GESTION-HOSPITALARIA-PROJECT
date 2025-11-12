from src.database.conexion import conectar

def cancelar_hora():
    print("\n--- CANCELAR HORA ---")
    
    conexion = conectar()
    if conexion is None:
        return
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT h.id_hora, p.nombres, p.apellidos, h.fecha_hora, h.medico
            FROM tbl_hora_medica h
            JOIN tbl_paciente p ON h.id_paciente = p.id_paciente
            WHERE h.estado = 'Agendada'
        """)
        horas = cursor.fetchall()
        
        if not horas:
            print("No hay horas activas")
            return
        
        print("\nHoras disponibles:")
        for i, hora in enumerate(horas, 1):
            print(f"{i}. {hora[1]} {hora[2]}")
            print(f"   Fecha: {hora[3]}")
            print(f"   Médico: {hora[4]}")
            print()
        
        opcion = int(input("Seleccione una hora: "))
        
        if 1 <= opcion <= len(horas):
            cursor.execute("UPDATE tbl_hora_medica SET estado = 'Cancelada' WHERE id_hora = %s", 
                          (horas[opcion-1][0],))
            conexion.commit()
            print("Hora cancelada")
        else:
            print("Opción inválida")
            
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conexion.close()

def reagendar_hora():
    print("\n--- REAGENDAR HORA ---")
    
    conexion = conectar()
    if conexion is None:
        return
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT h.id_hora, p.nombres, p.apellidos, h.fecha_hora, h.medico
            FROM tbl_hora_medica h
            JOIN tbl_paciente p ON h.id_paciente = p.id_paciente
            WHERE h.estado = 'Agendada'
        """)
        horas = cursor.fetchall()
        
        if not horas:
            print("No hay horas activas")
            return
        
        print("\nHoras disponibles:")
        for i, hora in enumerate(horas, 1):
            print(f"{i}. {hora[1]} {hora[2]}")
            print(f"   Fecha: {hora[3]}")
            print(f"   Médico: {hora[4]}")
            print()
        
        opcion = int(input("Seleccione una hora: "))
        
        if 1 <= opcion <= len(horas):
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ")
            nueva_hora = input("Nueva hora (HH:MM:SS): ")
            nueva_fecha_completa = f"{nueva_fecha} {nueva_hora}"
            
            cursor.execute("UPDATE tbl_hora_medica SET fecha_hora = %s WHERE id_hora = %s", 
                          (nueva_fecha_completa, horas[opcion-1][0]))
            conexion.commit()
            print("Hora reagendada")
        else:
            print("Opción inválida")
            
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conexion.close()

def menu():
    while True:
        print("\n=== GESTIÓN DE HORAS ===")
        print("1. Cancelar hora")
        print("2. Reagendar hora")
        print("3. Salir")
        
        opcion = input("Opción: ")
        
        if opcion == "1":
            cancelar_hora()
        elif opcion == "2":
            reagendar_hora()
        elif opcion == "3":
            print("Fin del programa")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()