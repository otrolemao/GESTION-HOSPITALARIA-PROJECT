from conexion import conectar

# Función para mostrar pacientes existentes
def listar_pacientes():
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_paciente, rut, nombres, apellidos FROM tbl_paciente ORDER BY nombres")
        pacientes = cursor.fetchall()
        
        if pacientes:
            print("\n=== PACIENTES REGISTRADOS ===")
            for paciente in pacientes:
                print(f"ID: {paciente[0]} | RUT: {paciente[1]} | Nombre: {paciente[2]} {paciente[3]}")
            print("==============================\n")
        else:
            print("No hay pacientes registrados. Registre un paciente primero.")
        
    except Exception as e:
        print("Error al listar pacientes:", e)
    finally:
        cursor.close()
        conexion.close()

# Buscar el id del paciente por su nombre
def obtener_id_paciente(nombre_paciente):
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return None
    try:
        cursor = conexion.cursor()
        # Buscar por nombre o apellido
        cursor.execute("""
            SELECT id_paciente, nombres, apellidos 
            FROM tbl_paciente 
            WHERE nombres LIKE %s OR apellidos LIKE %s
        """, (f'%{nombre_paciente}%', f'%{nombre_paciente}%'))
        
        resultados = cursor.fetchall()
        
        if len(resultados) == 0:
            print("No existe un paciente con ese nombre.")
            return None
        elif len(resultados) == 1:
            return resultados[0][0]  # Retorna el ID del paciente
        else:
            # Múltiples resultados
            print("\nSe encontraron varios pacientes:")
            for i, paciente in enumerate(resultados, 1):
                print(f"{i}. {paciente[1]} {paciente[2]} (ID: {paciente[0]})")
            
            try:
                opcion = int(input("\nSeleccione el número del paciente: ")) - 1
                if 0 <= opcion < len(resultados):
                    return resultados[opcion][0]
                else:
                    print("Opción inválida.")
                    return None
            except ValueError:
                print("Por favor ingrese un número válido.")
                return None
                
    except Exception as e:
        print("Error al buscar paciente:", e)
        return None
    finally:
        cursor.close()
        conexion.close()

# Función para verificar si ya existe una hora en la misma fecha/hora
def verificar_hora_existente(fecha_hora, medico):
    conexion = conectar()
    if conexion is None:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_hora FROM tbl_hora_medica 
            WHERE fecha_hora = %s AND medico = %s AND estado != 'Cancelada'
        """, (fecha_hora, medico))
        
        return cursor.fetchone() is not None
    except Exception as e:
        print("Error al verificar hora:", e)
        return False
    finally:
        cursor.close()
        conexion.close()

# Función principal para agendar hora médica
def agendar_hora():
    print("\n=== AGENDAR HORA MÉDICA ===")
    
    # Mostrar pacientes disponibles
    listar_pacientes()
    
    nombre_paciente = input("Ingrese nombre o apellido del paciente: ").strip()
    
    if not nombre_paciente:
        print("Debe ingresar un nombre.")
        return

    # Buscar el ID automáticamente
    id_paciente = obtener_id_paciente(nombre_paciente)
    if not id_paciente:
        return

    # Pedir datos de la cita
    print("\n--- Datos de la cita ---")
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    hora = input("Hora (HH:MM:SS): ").strip()
    fecha_hora = f"{fecha} {hora}"
    
    especialidad = input("Especialidad: ").strip()
    medico = input("Nombre del médico: ").strip()

    # Validaciones básicas
    if not all([fecha, hora, especialidad, medico]):
        print("Todos los campos son obligatorios.")
        return

    # Verificar si la hora ya está ocupada
    if verificar_hora_existente(fecha_hora, medico):
        print(f"El médico {medico} ya tiene una hora agendada para {fecha_hora}")
        confirmar = input("¿Desea agendar de todas formas? (s/n): ").lower()
        if confirmar != 's':
            return

    # Conectar y guardar
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO tbl_hora_medica (id_paciente, fecha_hora, especialidad, medico, estado)
            VALUES (%s, %s, %s, %s, 'Agendada')
        """
        valores = (id_paciente, fecha_hora, especialidad, medico)
        cursor.execute(query, valores)
        conexion.commit()
        print(f"\n✓ Hora médica agendada correctamente para el paciente (ID: {id_paciente})")
        print(f"  Fecha: {fecha_hora}")
        print(f"  Especialidad: {especialidad}")
        print(f"  Médico: {medico}")
        
    except Exception as e:
        print("Error al agendar hora médica:", e)
    finally:
        cursor.close()
        conexion.close()

# Función para probar el módulo
if __name__ == "__main__":
    agendar_hora()