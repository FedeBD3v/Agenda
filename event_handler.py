from tkinter import *
from tkinter import messagebox
from db_manager import Connect  # Importamos la clase Connect

class Consultation:
    # Constantes de mensajes
    ERROR_MSG = "Error"
    GUARDADO_MSG = "Guardado"
    BORRADO_MSG = "Borrado"
    ACTUALIZADO_MSG = "Actualizado"

    def __init__(self):
        self.db = Connect()  # Instancia para acceder a la base de datos.
        self.ID = IntVar()
        self.nombre = StringVar()
        self.apellido = StringVar()
        self.telefono = StringVar()
        self.email = StringVar()
        self.connect = Connect()

    def guardar(self, datos):
        print(datos)
        print(type(datos))
        if self.validar_datos(datos):
            self.connect.insertar(datos)
        else:
            print("Datos incorretos")

    def validar_datos(self,datos):
        if not datos["Nombre"] or not datos["Apellido"] or not datos["Telefono"] or not datos["Email"]:
            return False
        if not datos["Telefono"].isdigit():
            return False
        if "@" not in datos["Email"] or "." not in datos["Email"]:
            return False
        return True

    def obtener_contactos(self):
        """Obtener los contactos de la base de datos."""
        return self.db.contactos_obtenidos()
    
    def detalle_contacto(self, contact_id):
        """Obtener la información de un contacto selecciónado"""
        print(contact_id)
        return self.db.informacion_contacto(contact_id)
