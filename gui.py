import tkinter as tk
from tkinter import Tk, Frame, ttk, Button,Entry, IntVar, StringVar, Toplevel, Label
from event_handler import Consultation
import re

class Gui:
    def __init__(self, root):

        # Constantes
        WIDTH = 1500
        HEIGHT = 850
       

        self.root = root
        self.root.title("Agenda")
        self.root.geometry(f"{WIDTH}x{HEIGHT}") # Establecer dimensiones de la ventana
        self.root.resizable(False, False)
        


        # Instanciar la clase Consultation para gestionar contactos
        self.consultation = Consultation()

        # Frame - list
        self.frame_list = Frame(self.root)
        self.frame_list.pack(fill='both', expand=True)  # Agregar espacio alrededor

        self.style = ttk.Style()
        self.style.configure(
            "Treeview",
            background = "#34495E",
            foreground="white",
            rowheight=25,
            fieldbackground="#34495E"
        )
        self.style.map("Treeview",
                       background=[('selected', '#1ABC9C')],
                       foreground=[('selected', 'black')])

        # Crear el Treeview
        self.tree = ttk.Treeview(self.frame_list, columns=("ID", "Nombre", "Apellido", "Teléfono", "E-mail"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("E-mail", text="E-mail")

        # Establecer el ancho de las columnas
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Nombre", width=150, anchor='center')
        self.tree.column("Apellido", width=150, anchor='center')
        self.tree.column("Teléfono", width=100, anchor='center')
        self.tree.column("E-mail", width=150, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_list,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Ubicar Scrollbar
        self.tree.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        self.tree.pack(fill='both', expand=True)  # Expandir el Treeview
        
        

        # Frame para los botones
        self.frame_buttons = Frame(self.root, bg="lightgrey")
        self.frame_buttons.pack(fill='x', padx=10, pady=5)

        # Botones
        btn_add = ttk.Button(self.frame_buttons, text="Agregar", command=self.agregar_nuevo)
        btn_add.pack(side="left", padx=10, pady=5)  # Acomodar el botón

        self.cargar_contactos()
   
    def agregar_nuevo(self):
    # Constante
        NEW_HEIGHT = 200
        NEW_WIDTH = 300
    
    # Variables
        self.id_var = IntVar()
        self.nombre_var = StringVar()
        self.apellido_var = StringVar()
        self.telefono_var = StringVar()
        self.email_var = StringVar()

        new_window = Toplevel(self.root, bg="#34495E")  # Nueva ventana hija
        new_window.title("Agregar nuevo contacto")
        new_window.geometry(F"{NEW_WIDTH}x{NEW_HEIGHT}")
        new_window.resizable(False,False)

        # Definición de campos y creación con un bucle
        campos = [("Nombre", self.nombre_var), 
              ("Apellido", self.apellido_var), 
              ("Teléfono", self.telefono_var), 
              ("E-mail", self.email_var)]

        for i, (texto, variable) in enumerate(campos):
            Label(new_window,bg="#34495E", text=f"{texto}:").grid(row=i, column=0, padx=10, pady=5)
            Entry(new_window, textvariable=variable).grid(row=i, column=1, padx=10, pady=5)


        # Botón Guardar
        Button(new_window, 
                   text="Guardar", 
                   command=self.guardar_contacto,
                   ).grid(
            row=4, column=0, columnspan=2, pady=10
        )

    def guardar_contacto(self):
        nombre = self.nombre_var.get().strip().capitalize()
        apellido = self.apellido_var.get().strip().capitalize()
        telefono = self.telefono_var.get().strip().capitalize()
        email = self.email_var.get().strip().capitalize()

        datos = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Telefono": telefono,
            "Email": email
        }
        self.consultation.guardar(datos)

        for widget in self.root.winfo_children():
            if isinstance(widget, Toplevel):
                self.cargar_contactos()
                widget.destroy()


    def cargar_contactos(self):
        # Recorromos los datos del treeview y los limpiamos
        for dato in self.tree.get_children():
            self.tree.delete(dato)
        
        # Obtener los contactos desde la base de datos a través del event_handler
        contactos = self.consultation.obtener_contactos()

        # Insertamos nuevamente los contactos al treeview
        for contacto in contactos:
            self.tree.insert("",tk.END, values=contacto)
        
        
if __name__ == "__main__":
    root = Tk()
    gui = Gui(root)
    root.mainloop()
