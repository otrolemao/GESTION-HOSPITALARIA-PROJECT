import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",             # tu usuario de MySQL
            password="", # cambia esto por tu contraseña real
            database="db_hospital"    # nombre exacto de tu base de datos
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion

    except mysql.connector.Error as error:
        print("Error al conectar a MySQL:", error)
        return None
