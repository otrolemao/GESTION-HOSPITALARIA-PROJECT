# AQUI ESTA EL menu_principal.py, que es como la interface en si xd, con todas las opciones y su respectiva tarea
from registrar_paciente import FormularioPaciente
from buscar_editar_paciente import buscar_editar_paciente
from agendar_hora import agendar_hora
from vista_reagendamiento import VistaReagendamiento
from gestion_hora import cancelar_hora

def menu_principal():
    while True:
        print("\n" + "="*50)    
        print("       SISTEMA DE GESTIÓN HOSPITALARIA")
        print("="*50)
        print("1. Registrar paciente")
        print("2. Buscar/editar paciente") 
        print("3. Agendar hora médica")
        print("4. Reagendar hora médica")
        print("5. Cancelar hora médica")
        print("6. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n--- REGISTRAR PACIENTE ---")
            paciente = FormularioPaciente()
            paciente.el_input()
            paciente.guardar_en_bd()
            
        elif opcion == "2":
            print("\n--- BUSCAR Y EDITAR PACIENTE ---")
            buscar_editar_paciente()
            
        elif opcion == "3":
            print("\n--- AGENDAR HORA MÉDICA ---")
            agendar_hora()
            
        elif opcion == "4":
            print("\n--- REAGENDAR HORA MÉDICA ---")
            vista_reag = VistaReagendamiento()
            vista_reag.mostrar_menu_reagendamiento()
            
        elif opcion == "5":
            print("\n--- CANCELAR HORA MÉDICA ---")
            cancelar_hora()
            
        elif opcion == "6":
            print("¡Gracias por usar el Sistema Hospitalario!")
            break
            
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()