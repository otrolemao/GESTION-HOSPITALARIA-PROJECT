from conexion import conectar

def buscar_editar_paciente():
    print("\n--- BUSCAR Y EDITAR PACIENTE ---")
    
    conexion = conectar()
    if conexion is None:
        return
    
    try:
        cursor = conexion.cursor()
        
        # Mostrar TODOS los pacientes
        cursor.execute("SELECT id_paciente, nombres, apellidos, telefono, direccion, correo FROM tbl_paciente")
        pacientes = cursor.fetchall()
        
        if not pacientes:
            print("No hay pacientes")
            return
        
        print("\nLISTA DE PACIENTES:")
        for i, p in enumerate(pacientes, 1):
            print(f"{i}. {p[1]} {p[2]}")
        
        # Seleccionar
        opcion = int(input("\nSeleccione paciente: ")) - 1
        
        if 0 <= opcion < len(pacientes):
            paciente = pacientes[opcion]
            
            print(f"\nEditando a: {paciente[1]} {paciente[2]}")
            print("¿Qué desea editar?")
            print("1. Nombre")
            print("2. Apellido")
            print("3. Teléfono")
            print("4. Dirección")
            print("5. Correo")
            print("6. Salir")
            
            opcion_editar = input("Opción: ")
            
            if opcion_editar == "1":
                nuevo_nombre = input("Nuevo nombre: ")
                cursor.execute("UPDATE tbl_paciente SET nombres = %s WHERE id_paciente = %s", 
                             (nuevo_nombre, paciente[0]))
                print("Nombre actualizado")
                
            elif opcion_editar == "2":
                nuevo_apellido = input("Nuevo apellido: ")
                cursor.execute("UPDATE tbl_paciente SET apellidos = %s WHERE id_paciente = %s", 
                             (nuevo_apellido, paciente[0]))
                print("Apellido actualizado")
                
            elif opcion_editar == "3":
                nuevo_telefono = input("Nuevo teléfono: ")
                cursor.execute("UPDATE tbl_paciente SET telefono = %s WHERE id_paciente = %s", 
                             (nuevo_telefono, paciente[0]))
                print("Teléfono actualizado")
                
            elif opcion_editar == "4":
                nueva_direccion = input("Nueva dirección: ")
                cursor.execute("UPDATE tbl_paciente SET direccion = %s WHERE id_paciente = %s", 
                             (nueva_direccion, paciente[0]))
                print("Dirección actualizada")
                
            elif opcion_editar == "5":
                nuevo_correo = input("Nuevo correo: ")
                cursor.execute("UPDATE tbl_paciente SET correo = %s WHERE id_paciente = %s", 
                             (nuevo_correo, paciente[0]))
                print("Correo actualizado")

            elif opcion_editar == "6":
                return
            
            else:
                print("Opción inválida")
                return
            
            conexion.commit()
        
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conexion.close()

# Usar
if __name__ == "__main__":
    buscar_editar_paciente()