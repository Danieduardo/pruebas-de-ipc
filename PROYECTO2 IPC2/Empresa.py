class Empresa:
    def __init__(self, id, nombre, abreviatura):
        self.id = id
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.puntos_atencion = ListaSimple()
        self.transacciones = ListaSimple()
    
    def agregar_punto_atencion(self, punto_atencion):
        self.puntos_atencion.insertar(punto_atencion)
    
    def agregar_transaccion(self, transaccion):
        self.transacciones.insertar(transaccion)
    
    def buscar_punto_atencion(self, id_punto):
        actual = self.puntos_atencion.primero
        while actual:
            if actual.dato.id == id_punto:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def buscar_transaccion(self, id_transaccion):
        actual = self.transacciones.primero
        while actual:
            if actual.dato.id == id_transaccion:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def __str__(self):
        return f"Empresa: {self.nombre} (ID: {self.id}, Abreviatura: {self.abreviatura})"