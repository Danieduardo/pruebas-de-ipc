class Cliente:
    def __init__(self, dpi, nombre):
        self.dpi = dpi
        self.nombre = nombre
        self.transacciones = []  # Lista de tuplas (transaccion, cantidad)
        self.tiempo_total_atencion = 0
        self.tiempo_espera = 0
        self.tiempo_inicio_espera = 0
        self.tiempo_fin_espera = 0
        self.tiempo_inicio_atencion = 0
        self.tiempo_fin_atencion = 0
        self.escritorio_asignado = None
    
    def agregar_transaccion(self, transaccion, cantidad=1):
        self.transacciones.append((transaccion, cantidad))
        self.tiempo_total_atencion += transaccion.tiempo_atencion * cantidad
    
    def calcular_tiempo_atencion(self):
        total = 0
        for transaccion, cantidad in self.transacciones:
            total += transaccion.tiempo_atencion * cantidad
        return total
    
    def iniciar_espera(self, tiempo_actual):
        self.tiempo_inicio_espera = tiempo_actual
    
    def terminar_espera(self, tiempo_actual):
        self.tiempo_fin_espera = tiempo_actual
        self.tiempo_espera = self.tiempo_fin_espera - self.tiempo_inicio_espera
    
    def iniciar_atencion(self, tiempo_actual, escritorio):
        self.tiempo_inicio_atencion = tiempo_actual
        self.escritorio_asignado = escritorio
    
    def terminar_atencion(self, tiempo_actual):
        self.tiempo_fin_atencion = tiempo_actual
        tiempo_atencion = self.tiempo_fin_atencion - self.tiempo_inicio_atencion
        return tiempo_atencion
    
    def __str__(self):
        return f"Cliente: {self.nombre} (DPI: {self.dpi}, Tiempo total: {self.tiempo_total_atencion} min)"