from tkinter import *

ventana = Tk()

ventana.geometry("650x660")
ventana.title("FORMULARIO DE REGISTRO DE PACIENTE")
ventana.resizable(True, True)
ventana.config(background="#123363")
main_title = Label(text="HOSPITAL REGISTER | form jordiv", font=("Cambria", 13), bg="#123436", fg="white", width="55", height="2")
main_title.pack()

ventana.mainloop()