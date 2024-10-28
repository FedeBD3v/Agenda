import os
from PIL import Image, ImageTk

class WhatsappIcon:
    def __init__(self, image_path, size=(32, 32)):
        self.image_path = image_path
        self.size = size
        self.whatsapp_icon = None
        self.load_image()

    def load_image(self):
        """Carga y redimensiona la imagen de WhatsApp."""
        try:
            img = Image.open(self.image_path)
            img = img.resize(self.size, Image.LANCZOS)  # Cambiado de ANTIALIAS a LANCZOS
            self.whatsapp_icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.whatsapp_icon = ImageTk.PhotoImage()  # Imagen vacía o predeterminada

    def get_icon(self):
        """Retorna el icono cargado."""
        return self.whatsapp_icon
