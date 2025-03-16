# Transaccion.py
class Transaccion:
    def __init__(self, id, nombre, tiempo_atencion):
        self.id = id
        self.nombre = nombre
        self.tiempo_atencion = tiempo_atencion
    
    def __str__(self):
        return f"Transacción: {self.nombre} (ID: {self.id}, Tiempo: {self.tiempo_atencion} min)"