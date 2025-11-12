from src.database.conexion import conectar

class VistaReagendamiento:
    def __init__(self):
        self.conexion = conectar()
    
    def mostrar_menu_reagendamiento(self):
        while True:
            print("\n" + "="*50)
            print("       VISTA DE REAGENDAMIENTO")
            print("="*50)
            print("1. Ver horas agendadas")
            print("2. Reagendar hora seleccionada")
            print("3. Volver al menú principal")
            print("="*50)
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.mostrar_horas_agendadas()
            elif opcion == "2":
                self.reagendar_hora_interfaz()
            elif opcion == "3":
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
    
    def mostrar_horas_agendadas(self):
        print("\n" + "-"*50)
        print("       HORAS AGENDADAS DISPONIBLES")
        print("-"*50)
        
        if self.conexion is None:
            print("Error: No hay conexión a la base de datos")
            return
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT h.id_hora, p.nombres, p.apellidos, h.fecha_hora, h.medico, h.estado
                FROM tbl_hora_medica h
                JOIN tbl_paciente p ON h.id_paciente = p.id_paciente
                WHERE h.estado = 'Agendada'
                ORDER BY h.fecha_hora
            """)
            horas = cursor.fetchall()
            
            if not horas:
                print("No hay horas agendadas disponibles.")
                return
            
            print(f"{'ID':<4} {'Paciente':<20} {'Fecha/Hora':<20} {'Médico':<15} {'Estado':<10}")
            print("-"*70)
            
            for hora in horas:
                id_hora, nombre, apellido, fecha_hora, medico, estado = hora
                paciente_completo = f"{nombre} {apellido}"
                print(f"{id_hora:<4} {paciente_completo:<20} {str(fecha_hora):<20} {medico:<15} {estado:<10}")
                
        except Exception as e:
            print(f"Error al cargar horas: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def reagendar_hora_interfaz(self):
        print("\n" + "-"*50)
        print("       REAGENDAR HORA MÉDICA")
        print("-"*50)
        
        self.mostrar_horas_agendadas()
        
        if self.conexion is None:
            return
        
        try:
            id_hora = input("\nIngrese el ID de la hora a reagendar: ")
            
            if not id_hora.isdigit():
                print("Error: ID debe ser un número")
                return
            
            cursor = self.conexion.cursor()
            
            cursor.execute("""
                SELECT h.id_hora, p.nombres, p.apellidos, h.fecha_hora, h.medico
                FROM tbl_hora_medica h
                JOIN tbl_paciente p ON h.id_paciente = p.id_paciente
                WHERE h.id_hora = %s AND h.estado = 'Agendada'
            """, (id_hora,))
            
            hora = cursor.fetchone()
            
            if not hora:
                print("Error: Hora no encontrada o no está agendada")
                return
            
            id_hora, nombre, apellido, fecha_actual, medico = hora
            print(f"\nReagendando hora para: {nombre} {apellido}")
            print(f"Médico actual: {medico}")
            print(f"Fecha/hora actual: {fecha_actual}")
            
            print("\nIngrese la nueva fecha y hora:")
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ")
            nueva_hora = input("Nueva hora (HH:MM:SS): ")
            
            nueva_fecha_completa = f"{nueva_fecha} {nueva_hora}"
            
            confirmar = input(f"\n¿Confirmar reagendamiento para {nueva_fecha_completa}? (s/n): ")
            
            if confirmar.lower() == 's':
                cursor.execute("""
                    UPDATE tbl_hora_medica 
                    SET fecha_hora = %s 
                    WHERE id_hora = %s
                """, (nueva_fecha_completa, id_hora))
                
                self.conexion.commit()
                print("¡Hora reagendada exitosamente!")
            else:
                print("Reagendamiento cancelado")
                
        except Exception as e:
            print(f"Error durante el reagendamiento: {e}")
        finally:
            if cursor:
                cursor.close()

def main():
    vista = VistaReagendamiento()
    vista.mostrar_menu_reagendamiento()

if __name__ == "__main__":
    main()