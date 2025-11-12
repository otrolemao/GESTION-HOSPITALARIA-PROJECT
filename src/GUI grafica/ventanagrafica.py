# LO QUE VA AQUI, ES LA INTERFACE DEL TKINTER QUE ESTA CINECTADO CON EL FORMULARIO YA HECHO EN "FormularioPaciente"

from tkinter import *
from registrar_paciente import FormularioPaciente

class InterfazPaciente:
    def __init__(self, ventana):
        self.ventana = ventana
        self.formulario = FormularioPaciente()
        self.crear_widgets()
    
    def crear_widgets(self):
        self.ventana.title("REGISTRO DE PACIENTE")
        self.ventana.geometry("500x400")
        self.ventana.config(bg="#123363")
        
        titulo = Label(self.ventana, text="HOSPITAL REGISTER", font=("Arial", 16, "bold"), bg="#123436", fg="white", width=40, height=2)
        titulo.pack(pady=10)
        
        frame_campos = Frame(self.ventana, bg="#123363")
        frame_campos.pack(pady=20)
        
        self.entries = {}
        
        campos = [
            ("RUT:", "rut"),
            ("Nombre:", "nombre"),
            ("Apellido:", "apellido"), 
            ("Edad:", "edad"),
            ("Género:", "genero"),
            ("Teléfono:", "telefono"),
            ("Email:", "email"),
            ("Dirección:", "direccion")
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
        self.formulario.rut = self.entries["rut"].get()
        self.formulario.nombre = self.entries["nombre"].get()
        self.formulario.apellido = self.entries["apellido"].get()
        self.formulario.edad = int(self.entries["edad"].get()) if self.entries["edad"].get() else 0
        self.formulario.genero = self.entries["genero"].get()
        self.formulario.telefono = self.entries["telefono"].get()
        self.formulario.email = self.entries["email"].get()
        self.formulario.direccion = self.entries["direccion"].get()
        
        self.mostrar_mensaje(f"PACIENTE REGISTRADO 100%\n\nRUT: {self.formulario.rut}\nNombre: {self.formulario.nombre} {self.formulario.apellido}")
        self.limpiar_campos()
    
    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, END)
    
    def mostrar_mensaje(self, mensaje):
        ventana_msg = Toplevel(self.ventana)
        ventana_msg.title("Registro Exitoso")
        ventana_msg.geometry("300x150")
        ventana_msg.config(bg="#123363")
        Label(ventana_msg, text=mensaje, bg="#123363", fg="white", font=("Arial", 11)).pack(expand=True, pady=20)
        Button(ventana_msg, text="OK", command=ventana_msg.destroy, bg="#007bff", fg="white").pack(pady=10)

if __name__ == "__main__":
    ventana = Tk()
    app = InterfazPaciente(ventana)
    ventana.mainloop()