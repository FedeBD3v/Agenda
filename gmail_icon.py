import os
from PIL import Image, ImageTk

class GmailIcon:
    def __init__(self, image_path, size=(32, 32)):
        self.image_path = image_path
        self.size = size
        self.gmail_icon = None
        self.load_image()

    def load_image(self):
        """Carga y redimensiona la imagen de Gmail."""
        try:
            img = Image.open(self.image_path)
            img = img.resize(self.size, Image.LANCZOS)  
            self.gmail_icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            self.gmail_icon = ImageTk.PhotoImage()  
            
    def get_icon(self):
        """Retorna el ícono de Gmail."""
        return self.gmail_icon
