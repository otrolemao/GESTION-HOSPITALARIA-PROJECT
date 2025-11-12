from conexion import conectar

# Buscar el id del paciente por su nombre
def obtener_id_paciente(nombre_paciente):
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_paciente FROM tbl_paciente WHERE nombre = %s", (nombre_paciente,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except Exception as e:
        print("Error al buscar paciente:", e)
        return None
    finally:
        cursor.close()
        conexion.close()


# Función principal para agendar hora médica
def agendar_hora():
    print("=== AGENDAR HORA MÉDICA ===")
    nombre_paciente = input("Nombre del paciente: ")

    # Buscar el ID automáticamente
    id_paciente = obtener_id_paciente(nombre_paciente)
    if not id_paciente:
        print("No existe un paciente con ese nombre.")
        return

    # Pedir datos de la cita
    fecha_hora = input("Fecha y hora (formato YYYY-MM-DD HH:MM:SS): ")
    especialidad = input("Especialidad: ")
    medico = input("Nombre del médico: ")

    # Conectar y guardar
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO tbl_hora_medica (id_paciente, fecha_hora, especialidad, medico)
            VALUES (%s, %s, %s, %s)
        """
        valores = (id_paciente, fecha_hora, especialidad, medico)
        cursor.execute(query, valores)
        conexion.commit()
        print("Hora médica agendada correctamente para", nombre_paciente)
    except Exception as e:
        print("Error al agendar hora médica:", e)
    finally:
        cursor.close()
        conexion.close()
