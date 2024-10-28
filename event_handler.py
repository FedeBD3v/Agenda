from tkinter import messagebox, StringVar, IntVar
import re
import webbrowser
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

    def guardar(self, datos):
        """Guarda un nuevo contacto en la base de datos."""
        try:
            id_db = self.db.insertar(datos)
            messagebox.showinfo(self.GUARDADO_MSG, "El contacto ha sido guardado correctamente.")
            return id_db
        except Exception as e:
            messagebox.showerror(self.ERROR_MSG, f"Ha ocurrido un error inesperado: {e}")

    def validar_datos(self, datos):
        """Valida los datos del contacto ingresados."""
        # 1. Verificar que no haya campos vacíos
        if not datos['Nombre'] and datos['Apellido'] and datos['Telefono'] and datos['Email']:
            messagebox.showerror(self.ERROR_MSG, "Debes completar todos los datos pedidos.")
            return False

        # 2. Validación del teléfono (entre 8-15 dígitos, opcionalmente con '+')
        if not re.match(r"^\+?\d{8,15}$", datos["Telefono"]):
            messagebox.showerror(self.ERROR_MSG, "El teléfono debe ser numérico y tener entre 8 y 15 dígitos.")
            return False

        # 3. Validación del correo electrónico usando una expresión regular
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, datos["Email"]):
            messagebox.showerror(self.ERROR_MSG, "El correo no tiene el formato adecuado.")
            return False

        return True

    def obtener_contactos(self):
        """Obtiene los contactos de la base de datos."""
        return self.db.contactos_obtenidos()
    
    def detalle_contacto(self, contact_id):
        """Obtiene la información de un contacto seleccionado."""
        return self.db.informacion_contacto(contact_id)
    
    def borrar(self, contact_id):
        """Borra un contacto de la base de datos."""
        respuesta = messagebox.askquestion(self.BORRADO_MSG, "¿Desea borrar el contacto?")  #
        if respuesta == 'yes':  
            try:
                self.db.eliminar(contact_id)
                messagebox.showinfo(self.BORRADO_MSG, "El contacto ha sido borrado exitosamente.")
            except Exception as e:
                messagebox.showerror(self.ERROR_MSG, f"Ha ocurrido un error: {e}")
        else:
            print("Acción de borrado cancelada.")

    def editar(self, datos):
        """Modifica el contacto en la base de datos."""
        if datos:
            try:
                self.db.actualizar(datos)
                messagebox.showinfo(self.ACTUALIZADO_MSG, "Los datos se han actualizado correctamente.")
            except Exception as e:
                messagebox.showerror(self.ERROR_MSG, f"Ha ocurrido un error: {e}")

    def whatsapp_msj(self,contact):
        print(contact)
        url = f"https://wa.me/{contact}"
        webbrowser.open(url)

    def gmail_msj(self,contact):
        print(contact)
        url = f"https://mail.google.com/mail/?view=cm&fs=1&to={contact}"
        webbrowser.open(url)