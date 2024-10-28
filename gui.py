import tkinter as tk
import os
from tkinter import Tk, Frame, ttk, Toplevel, Label, Button, Entry, IntVar, StringVar
from PIL import Image, ImageTk
from whatsapp_icon import WhatsappIcon
from event_handler import Consultation

class Gui:
    def __init__(self, root):
        # Constantes
        self.WIDTH = 1500
        self.HEIGHT = 850

        self.root = root
        self.root.title("Agenda")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
      
        # Inicializa el diccionario para almacenar imágenes
        self.image_tk = {}

        # Obtener la ruta de la imagen
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "whatsapp.png")

        # Crear el icono de WhatsApp
        whatsapp_icon = WhatsappIcon(image_path)  # Instancia la clase
        self.whatsapp_icon = whatsapp_icon.get_icon()  # Obtiene el icono

        # Instanciar la clase Consultation para gestionar contactos
        self.consultation = Consultation()

        # Crear elementos de la interfaz
        self.setup_treeview()
        self.setup_buttons()
        self.serch_contact()
        self.cargar_contactos()

    def setup_treeview(self):
        # Frame - list
        self.frame_list = Frame(self.root)
        self.frame_list.pack(fill='both', expand=True)

        # Configurar estilo del Treeview
        self.style = ttk.Style()
        self.style.configure("Treeview", background="#34495E", foreground="white", rowheight=25, fieldbackground="#34495E")
        self.style.map("Treeview", background=[('selected', '#1ABC9C')], foreground=[('selected', 'black')])

        

        # Crear el Treeview
        self.tree = ttk.Treeview(self.frame_list, columns=("ID", "Nombre", "Apellido", "Teléfono", "E-mail"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("E-mail", text="E-mail")

        # Establecer el ancho de las columnas
        for col, width in zip(["ID", "Nombre", "Apellido", "Teléfono", "E-mail"], [5, 200, 200, 200, 200]):
            self.tree.column(col, width=width, anchor='center')

        # Evento doble clic
        self.tree.bind("<Double-1>", self.mostrar_detalles)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Ubicar Scrollbar y Treeview
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_buttons(self):
        # Frame para los botones
        self.frame_buttons = Frame(self.root, bg="lightgrey")
        self.frame_buttons.pack(fill='x', padx=10, pady=5)

        # Botones
        btn_add = ttk.Button(self.frame_buttons, text="Agregar", command=self.agregar_nuevo)
        btn_add.pack(side="left", padx=10, pady=5)
    
    def serch_contact(self):
        """Buscador en tiempo real"""
        etr_serch = ttk.Entry(self.frame_buttons)
        etr_serch.pack(side="right", padx=10, pady=5)
        etr_serch.bind("<KeyRelease>", self.filter) 


    def filter(self, event):
        """Evento para filtrar contactos"""
        query = event.widget.get().lower()  # Obtengo el texto del Entry
        print(f"Texto ingresado: {query}")

        # Limpio el Treeview antes de aplicar el filtro
        self.tree.delete(*self.tree.get_children())  # Limpia todos los elementos

        # Obtengo todos los contactos nuevamente
        contactos = self.consultation.obtener_contactos()
    
        # Filtro y Vuelvo a agregar los elementos que coinciden
        for contacto in sorted(contactos, key=lambda x: x[0]):
            if any(query in str(value).lower() for value in contacto):
                self.tree.insert("", tk.END, iid=contacto[0], values=contacto)

    def mostrar_detalles(self, event):
        # Muestro los detalles desde el treeview
        selected_item = self.tree.selection()
        if not selected_item:
            print("No hay ningún contacto seleccionado.")
            return

        contact_id = int(selected_item[0])
        if contact_id:
            try:
                contact = self.consultation.detalle_contacto(contact_id)
                self.show_contact_details(contact)
                
                
            except ValueError as e:
                print(f"{e}")

    def show_contact_details(self, contact):
        # Crear nueva ventana para mostrar detalles
        detail_window = Toplevel(self.root)
        detail_window.title("Detalles del Contacto")
        # Mostrar información del contacto
        labels = ["ID:", "Nombre:", "Apellido:", "Teléfono:", "Email:"]
        for i, (text, value) in enumerate(zip(labels, contact)):
            Label(detail_window, text=text).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            Label(detail_window, text=value).grid(row=i, column=1, sticky='w', padx=5, pady=5)

        # Botones en ventana de detalles
        Button(detail_window, text="Aceptar", command=detail_window.destroy).grid(row=0, column=2, pady=5)
        Button(detail_window, text="Editar", command=lambda: self.editar_contacto(contact)).grid(row=1, column=2, pady=5)
        Button(detail_window, text="Eliminar", command=self.eliminar_contacto).grid(row=2, column=2, pady=5)

        Button(detail_window, text="Whatsapp",image=self.whatsapp_icon, command=lambda: self.consultation.whatsapp_msj(contact[3])).grid(row=3,column=2)
        

    def eliminar_contacto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            print("No hay ningún contacto seleccionado.")
            return

        contact_id = int(selected_item[0])
        if contact_id:
            try:
                self.consultation.borrar(contact_id)
                self.cargar_contactos()
                self.close_top_level_windows()
            except Exception as e:
                print(e)

    def close_top_level_windows(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()

    def editar_contacto(self, contact):
        NEW_HEIGHT, NEW_WIDTH = 230, 300
    
        # Variables
        self.id_var = IntVar()
        self.nombre_var = StringVar()
        self.apellido_var = StringVar()
        self.telefono_var = StringVar()
        self.email_var = StringVar()

        if contact:
            edit_window = Toplevel(self.root, bg="#34495E")
            edit_window.title("Editar contacto")
            edit_window.geometry(f"{NEW_WIDTH}x{NEW_HEIGHT}")
            edit_window.resizable(False, False)

            # Asignar los valores obtenidos a las variables
            self.id_var.set(contact[0])
            self.nombre_var.set(contact[1])  
            self.apellido_var.set(contact[2])  
            self.telefono_var.set(contact[3])  
            self.email_var.set(contact[4])  

            # Definición de campos y creación
            campos = [
                ("ID", self.id_var),
                ("Nombre", self.nombre_var),
                ("Apellido", self.apellido_var),
                ("Teléfono", self.telefono_var),
                ("E-mail", self.email_var),
            ]

            # Crear los Entry fields
            for i, (texto, variable) in enumerate(campos):
                Label(edit_window, bg="#34495E", text=f"{texto}:").grid(row=i, column=0, padx=10, pady=5)
                Entry(edit_window, textvariable=variable, state='readonly' if texto == "ID" else 'normal').grid(row=i, column=1, padx=10, pady=5)
        
            # Botón actualizar
            Button(edit_window, text="Actualizar", command=lambda: self.actualizar_contactos(contact[0])).grid(row=len(campos), columnspan=2, pady=10)

    def actualizar_contactos(self, contact_id):
        campos_actualizados = {
            'ID': self.id_var.get(),
            'nombre': self.nombre_var.get().strip().capitalize(),
            'apellido': self.apellido_var.get().strip().capitalize(),
            'telefono': str(self.telefono_var.get()).strip(),
            'email': self.email_var.get().strip()
        }
        
        resultado = self.consultation.validar_datos(campos_actualizados)
        if resultado:
        # Aquí podrías llamar a un método en tu clase Consultation para actualizar el contacto
            self.consultation.editar(campos_actualizados)  # Asegúrate de tener un método de edición en tu clase Consultation
            print("Contacto actualizado con éxito.")
            self.close_top_level_windows()
            self.cargar_contactos()  # Recargar los contactos para reflejar el cambio

    def agregar_nuevo(self):
        # Constantes de la ventana
        NEW_HEIGHT, NEW_WIDTH = 200, 300

        # Variables
        self.id_var = IntVar()
        self.nombre_var = StringVar()
        self.apellido_var = StringVar()
        self.telefono_var = StringVar()
        self.email_var = StringVar()

        new_window = Toplevel(self.root, bg="#34495E")
        new_window.title("Agregar nuevo contacto")
        new_window.geometry(f"{NEW_WIDTH}x{NEW_HEIGHT}")
        new_window.resizable(False, False)

        # Definición de campos y creación
        campos = [("Nombre", self.nombre_var), ("Apellido", self.apellido_var), ("Teléfono", self.telefono_var), ("E-mail", self.email_var)]
        for i, (texto, variable) in enumerate(campos):
            Label(new_window, bg="#34495E", text=f"{texto}:").grid(row=i, column=0, padx=10, pady=5)
            Entry(new_window, textvariable=variable).grid(row=i, column=1, padx=10, pady=5)

        # Botón Guardar
        Button(new_window, text="Guardar", command=self.guardar_contacto).grid(row=4, column=0, columnspan=2, pady=10)

    def guardar_contacto(self):
        datos = {
            "Nombre": self.nombre_var.get().strip().capitalize(),
            "Apellido": self.apellido_var.get().strip().capitalize(),
            "Telefono": self.telefono_var.get().strip().capitalize(),
            "Email": self.email_var.get().strip().capitalize(),
        }
        if self.consultation.validar_datos(datos):
            id_db = self.consultation.guardar(datos)
            if id_db:
                self.tree.insert("", tk.END, iid=id_db)
            self.cargar_contactos()
            self.close_top_level_windows()

    def cargar_contactos(self):
        # Limpiar el Treeview
        for dato in self.tree.get_children():
            self.tree.delete(dato)

        # Obtener los contactos desde la base de datos y insertarlos
        contactos = self.consultation.obtener_contactos()
        for contacto in sorted(contactos, key=lambda x: x[0]):
            self.tree.insert("", tk.END, iid=contacto[0], values=contacto)

if __name__ == "__main__":
    root = Tk()
    gui = Gui(root)
    root.mainloop()
