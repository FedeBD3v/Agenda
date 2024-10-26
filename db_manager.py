import sqlite3
from cryptography.fernet import Fernet # Para encriptar la base de datos

class Connect:
    def __init__(self, db_name="agenda.db"):
        """Inicializamos la conexión con la base de datos"""
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(db_name, check_same_thread=False)  # Permitir múltiples hilos
            self.cursor = self.conn.cursor()
            print("Conexión establecida correctamente")
            self.crear_tabla()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def crear_tabla(self):
        """Creamos la tabla si no existe"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS contactos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email VARCHAR(30) NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def insertar(self, datos):
        """Insertar un nuevo contacto en la base de datos y retornar su ID"""
        try:
            self.cursor.execute("""
                INSERT INTO contactos (nombre, apellido, telefono, email)
                VALUES (?, ?, ?, ?)
            """, (datos["Nombre"], datos["Apellido"], datos["Telefono"], datos["Email"]))
            self.conn.commit()
            print("Contacto guardado exitosamente.")
            return self.cursor.lastrowid  # Retorna el ID del contacto insertado
        except sqlite3.Error as e:
            print(f"Error al guardar el contacto: {e}")
            return None  # Retorna None en caso de error


    def contactos_obtenidos(self):
        """Obtener todos los contactos en orden ascendente por ID"""
        try:
            self.cursor.execute("SELECT * FROM contactos ORDER BY id ASC")
            contactos = self.cursor.fetchall()
            return contactos
        except sqlite3.Error as e:
            print(f"Error al obtener contactos: {e}")
            return []


    def informacion_contacto(self, contact_id):
        """Obtener un contacto específico por ID"""
        try:
            self.cursor.execute("SELECT * FROM contactos WHERE id = ?", (contact_id,))
            resultado = self.cursor.fetchone()
            return resultado
        except sqlite3.Error as e:
            print(f"Error en la consulta del contacto: {e}")
            return None

    def eliminar(self, contact_id):
        """Eliminar un contacto por ID"""
        try:
            self.cursor.execute("DELETE FROM contactos WHERE id = ?", (contact_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("Contacto eliminado exitosamente.")
            else:
                print("No se encontró el contacto para eliminar.")
        except sqlite3.Error as e:
            print(f"Error al eliminar el contacto: {e}")

    def actualizar(self, datos):
        """Actualizamos contacto"""
        if datos:
            try:
                print(datos)  # Verifica qué valores estás recibiendo
            
                # Asegúrate de que datos contenga los 4 valores necesarios: id, nombre, telefono, email
                self.cursor.execute("""
                UPDATE contactos
                SET nombre = ?, apellido = ? , telefono = ?, email = ?
                WHERE id = ?;
                """, (datos['nombre'],datos['apellido'], datos['telefono'], datos['email'], datos['ID']))  # Aquí pasamos los parámetros correctamente
            
                self.conn.commit()
            except Exception as e:
                print(f"Error {e}")


    def cerrar_conexion(self):
        """Cerrar la conexión con la base de datos"""
        if self.conn:
            self.conn.close()
            print("Conexión cerrada correctamente.")
