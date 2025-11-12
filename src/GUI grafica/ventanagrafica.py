from tkinter import *
#EXPERIMENTANDO CON TKINTER (CODIGO DE VENTANA GRAFICA)
import sys
import os

# Agregar el path para que encuentre los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from consola.registrar_paciente import FormularioPaciente

class InterfazPaciente:
    def __init__(self, ventana):
        self.ventana = ventana
        self.formulario = FormularioPaciente()
        self.crear_widgets()
    
    def crear_widgets(self):
        self.ventana.title("REGISTRO DE PACIENTE")
        self.ventana.geometry("500x500")
        self.ventana.config(bg="#123363")
        
        titulo = Label(self.ventana, text="HOSPITAL REGISTER", font=("Arial", 16, "bold"), bg="#123363", fg="white", width=40, height=2)
        titulo.pack(pady=10)
        
        frame_campos = Frame(self.ventana, bg="#123363")
        frame_campos.pack(pady=20)
        
        self.entries = {}
        
        campos = [
            ("RUT:", "rut"),
            ("Nombres:", "nombres"),
            ("Apellidos:", "apellidos"), 
            ("Fecha Nacimiento:", "fecha_nacimiento"),
            ("Sexo:", "sexo"),
            ("Dirección:", "direccion"),
            ("Teléfono:", "telefono"),
            ("Correo:", "correo")
        ]
        
        for i, (label_text, campo) in enumerate(campos):
            Label(frame_campos, text=label_text, bg="#123363", fg="white", font=("Arial", 10)).grid(row=i, column=0, sticky="w", pady=5, padx=10)
            entry = Entry(frame_campos, width=30, font=("Arial", 10))
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[campo] = entry
        
        frame_botones = Frame(self.ventana, bg="#123363")
        frame_botones.pack(pady=20)
        
        Button(frame_botones, text="REGISTRAR PACIENTE", command=self.registrar_desde_interfaz, bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        Button(frame_botones, text="LIMPIAR", command=self.limpiar_campos, bg="#ffc107", fg="black", font=("Arial", 12)).pack(side=LEFT, padx=10)
    
    def registrar_desde_interfaz(self):
        try:
            self.formulario.rut = self.entries["rut"].get()
            self.formulario.nombres = self.entries["nombres"].get()
            self.formulario.apellidos = self.entries["apellidos"].get()
            self.formulario.fecha_nacimiento = self.entries["fecha_nacimiento"].get()
            self.formulario.sexo = self.entries["sexo"].get()
            self.formulario.direccion = self.entries["direccion"].get()
            self.formulario.telefono = self.entries["telefono"].get()
            self.formulario.correo = self.entries["correo"].get()
            
            self.formulario.guardar_en_bd()
            
            self.mostrar_mensaje(f"PACIENTE REGISTRADO\n\nRUT: {self.formulario.rut}\nNombre: {self.formulario.nombres} {self.formulario.apellidos}")
            self.limpiar_campos()
            
        except Exception as e:
            self.mostrar_mensaje(f"Error al registrar: {str(e)}")
    
    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, END)
    
    def mostrar_mensaje(self, mensaje):
        ventana_msg = Toplevel(self.ventana)
        ventana_msg.title("Mensaje")
        ventana_msg.geometry("300x150")
        ventana_msg.config(bg="#123363")
        Label(ventana_msg, text=mensaje, bg="#123363", fg="white", font=("Arial", 11)).pack(expand=True, pady=20)
        Button(ventana_msg, text="OK", command=ventana_msg.destroy, bg="#007bff", fg="white").pack(pady=10)

if __name__ == "__main__":
    ventana = Tk()
    app = InterfazPaciente(ventana)
    ventana.mainloop()