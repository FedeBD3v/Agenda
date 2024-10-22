import sqlite3

class Connect:
    def __init__(self, db_name = "agenda.db"):
        """Inicializamos la conexión con la base de datos"""
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            print("Conexión establecida correctamente")
            self.crear_tabla()
        except sqlite3.Error as e:
            print(f"Error al concetar a la base de datos: {e}")
        
        

    def crear_tabla(self):
        """Creamos la tabla"""
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contactos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono INTEGER NOT NULL,
                    email VARCHAR(30) NOT NULL
                )
                """
            )
            self.conn.commit()
            print("Tabla creada o ya existente.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def insertar(self,datos):
        """Guardamos los datos en la tabla"""
        try:
            self.cursor.execute("""INSERT INTO contactos (nombre, apellido, telefono, email) 
                VALUES (?, ?, ?, ?)
            """, (datos["Nombre"], datos["Apellido"], datos["Telefono"], datos["Email"]))
            self.conn.commit()
            print("Contacto guardado con exito.")
        except sqlite3.Error as e:
            print(f"Error al guardar el contacto: {e}")

    def contactos_obtenidos(self):
        """Recolectar todos los contactos de la base de datos"""
        self.cursor.execute("SELECT * FROM contactos")
        return self.cursor.fetchall()