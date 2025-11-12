from conexion import conectar
from datetime import datetime

# Función para listar horas médicas de un paciente
def listar_horas_paciente(id_paciente=None, mostrar_todas=False, solo_activas=True):
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return []
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        if mostrar_todas:
            # Mostrar todas las horas médicas
            query = """
                SELECT h.id_hora, p.nombres, p.apellidos, h.fecha_hora, 
                       h.especialidad, h.medico, h.estado
                FROM tbl_hora_medica h
                JOIN tbl_paciente p ON h.id_paciente = p.id_paciente
            """
            if solo_activas:
                query += " WHERE h.estado = 'Agendada'"
            query += " ORDER BY h.fecha_hora DESC"
            cursor.execute(query)
        elif id_paciente:
            # Mostrar horas de un paciente específico
            query = """
                SELECT id_hora, fecha_hora, especialidad, medico, estado
                FROM tbl_hora_medica 
                WHERE id_paciente = %s
            """
            if solo_activas:
                query += " AND estado = 'Agendada'"
            query += " ORDER BY fecha_hora DESC"
            cursor.execute(query, (id_paciente,))
        else:
            return []
        
        horas = cursor.fetchall()
        return horas
        
    except Exception as e:
        print("Error al listar horas médicas:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Función para buscar paciente por nombre (similar a la de agendar_hora pero devuelve más datos)
def buscar_paciente_por_nombre(nombre_paciente):
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return None
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_paciente, rut, nombres, apellidos 
            FROM tbl_paciente 
            WHERE nombres LIKE %s OR apellidos LIKE %s
        """, (f'%{nombre_paciente}%', f'%{nombre_paciente}%'))
        
        resultados = cursor.fetchall()
        return resultados
        
    except Exception as e:
        print("Error al buscar paciente:", e)
        return None
    finally:
        cursor.close()
        conexion.close()

# Función para cancelar una hora médica
def cancelar_hora():
    print("\n=== CANCELAR HORA MÉDICA ===")
    
    # Mostrar todas las horas activas
    horas = listar_horas_paciente(mostrar_todas=True, solo_activas=True)
    
    if not horas:
        print("No hay horas médicas activas para cancelar.")
        return
    
    print("\n--- Horas médicas activas ---")
    for i, hora in enumerate(horas, 1):
        print(f"{i}. ID: {hora['id_hora']} | Paciente: {hora['nombres']} {hora['apellidos']}")
        print(f"   Fecha: {hora['fecha_hora']} | Médico: {hora['medico']} | Especialidad: {hora['especialidad']}")
        print("   " + "-" * 50)
    
    try:
        opcion = int(input("\nSeleccione el número de la hora a cancelar: ")) - 1
        if 0 <= opcion < len(horas):
            hora_seleccionada = horas[opcion]
            confirmar = input(f"¿Está seguro de cancelar la hora con ID {hora_seleccionada['id_hora']}? (s/n): ").lower()
            
            if confirmar == 's':
                conexion = conectar()
                if conexion is None:
                    print("No se pudo conectar a la base de datos.")
                    return
                
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        UPDATE tbl_hora_medica 
                        SET estado = 'Cancelada' 
                        WHERE id_hora = %s
                    """, (hora_seleccionada['id_hora'],))
                    conexion.commit()
                    print(f"✓ Hora médica ID {hora_seleccionada['id_hora']} cancelada correctamente.")
                    
                except Exception as e:
                    print("Error al cancelar hora médica:", e)
                finally:
                    cursor.close()
                    conexion.close()
            else:
                print("Cancelación abortada.")
        else:
            print("Opción inválida.")
            
    except ValueError:
        print("Por favor ingrese un número válido.")

# Función para reagendar una hora médica
def reagendar_hora():
    print("\n=== REAGENDAR HORA MÉDICA ===")
    
    # Mostrar todas las horas activas
    horas = listar_horas_paciente(mostrar_todas=True, solo_activas=True)
    
    if not horas:
        print("No hay horas médicas activas para reagendar.")
        return
    
    print("\n--- Horas médicas activas ---")
    for i, hora in enumerate(horas, 1):
        print(f"{i}. ID: {hora['id_hora']} | Paciente: {hora['nombres']} {hora['apellidos']}")
        print(f"   Fecha actual: {hora['fecha_hora']} | Médico: {hora['medico']}")
        print("   " + "-" * 50)
    
    try:
        opcion = int(input("\nSeleccione el número de la hora a reagendar: ")) - 1
        if 0 <= opcion < len(horas):
            hora_seleccionada = horas[opcion]
            
            print(f"\nReagendando hora para: {hora_seleccionada['nombres']} {hora_seleccionada['apellidos']}")
            print(f"Médico: {hora_seleccionada['medico']} | Especialidad: {hora_seleccionada['especialidad']}")
            
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ").strip()
            nueva_hora = input("Nueva hora (HH:MM:SS): ").strip()
            nueva_fecha_hora = f"{nueva_fecha} {nueva_hora}"
            
            if not nueva_fecha or not nueva_hora:
                print("Fecha y hora son obligatorios.")
                return
            
            confirmar = input(f"¿Reagendar para {nueva_fecha_hora}? (s/n): ").lower()
            
            if confirmar == 's':
                conexion = conectar()
                if conexion is None:
                    print("No se pudo conectar a la base de datos.")
                    return
                
                try:
                    cursor = conexion.cursor()
                    # Actualizar la fecha/hora y cambiar estado a Reagendada
                    cursor.execute("""
                        UPDATE tbl_hora_medica 
                        SET fecha_hora = %s, estado = 'Reagendada' 
                        WHERE id_hora = %s
                    """, (nueva_fecha_hora, hora_seleccionada['id_hora']))
                    conexion.commit()
                    print(f"✓ Hora médica ID {hora_seleccionada['id_hora']} reagendada correctamente.")
                    
                except Exception as e:
                    print("Error al reagendar hora médica:", e)
                finally:
                    cursor.close()
                    conexion.close()
            else:
                print("Reagendamiento abortado.")
        else:
            print("Opción inválida.")
            
    except ValueError:
        print("Por favor ingrese un número válido.")

# Función para buscar horas por paciente
def buscar_horas_por_paciente():
    print("\n=== BUSCAR HORAS POR PACIENTE ===")
    
    nombre_paciente = input("Ingrese nombre o apellido del paciente: ").strip()
    
    if not nombre_paciente:
        print("Debe ingresar un nombre.")
        return
    
    pacientes = buscar_paciente_por_nombre(nombre_paciente)
    
    if not pacientes:
        print("No se encontraron pacientes con ese nombre.")
        return
    
    if len(pacientes) == 1:
        id_paciente = pacientes[0]['id_paciente']
        nombre_completo = f"{pacientes[0]['nombres']} {pacientes[0]['apellidos']}"
    else:
        print("\nSe encontraron varios pacientes:")
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}. {paciente['nombres']} {paciente['apellidos']} (RUT: {paciente['rut']})")
        
        try:
            opcion = int(input("\nSeleccione el número del paciente: ")) - 1
            if 0 <= opcion < len(pacientes):
                id_paciente = pacientes[opcion]['id_paciente']
                nombre_completo = f"{pacientes[opcion]['nombres']} {pacientes[opcion]['apellidos']}"
            else:
                print("Opción inválida.")
                return
        except ValueError:
            print("Por favor ingrese un número válido.")
            return
    
    # Listar horas del paciente seleccionado
    horas = listar_horas_paciente(id_paciente=id_paciente, solo_activas=False)
    
    if not horas:
        print(f"\nEl paciente {nombre_completo} no tiene horas médicas registradas.")
        return
    
    print(f"\n--- Horas médicas de {nombre_completo} ---")
    for hora in horas:
        estado = hora['estado']
        estado_icon = "✓" if estado == 'Agendada' else "✗" if estado == 'Cancelada' else "↻"
        print(f"{estado_icon} Fecha: {hora['fecha_hora']} | Médico: {hora['medico']} | Especialidad: {hora['especialidad']} | Estado: {estado}")

# Función para mostrar menú de gestión de horas
def menu_gestion_horas():
    while True:
        print("\n=== GESTIÓN DE HORAS MÉDICAS ===")
        print("1. Cancelar hora médica")
        print("2. Reagendar hora médica")
        print("3. Buscar horas por paciente")
        print("4. Listar todas las horas activas")
        print("5. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            cancelar_hora()
        elif opcion == '2':
            reagendar_hora()
        elif opcion == '3':
            buscar_horas_por_paciente()
        elif opcion == '4':
            horas = listar_horas_paciente(mostrar_todas=True, solo_activas=True)
            if horas:
                print("\n--- Todas las horas médicas activas ---")
                for hora in horas:
                    print(f"ID: {hora['id_hora']} | Paciente: {hora['nombres']} {hora['apellidos']}")
                    print(f"   Fecha: {hora['fecha_hora']} | Médico: {hora['medico']} | Especialidad: {hora['especialidad']}")
                    print("   " + "-" * 50)
            else:
                print("No hay horas médicas activas.")
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Por favor seleccione 1-5.")

# Ejecutar si se llama directamente
if __name__ == "__main__":
    menu_gestion_horas()