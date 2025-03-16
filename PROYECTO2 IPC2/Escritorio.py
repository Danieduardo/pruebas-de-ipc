# Escritorio.py
class Escritorio:
    def __init__(self, id, identificacion, encargado):
        self.id = id
        self.identificacion = identificacion
        self.encargado = encargado
        self.activo = False
        self.cliente_actual = None
        self.tiempo_restante = 0
        
        # Estadísticas
        self.clientes_atendidos = 0
        self.tiempo_total_atencion = 0
        self.tiempo_max_atencion = 0
        self.tiempo_min_atencion = float('inf')
    
    def activar(self):
        self.activo = True
    
    def desactivar(self):
        self.activo = False
    
    def esta_libre(self):
        return self.cliente_actual is None
    
    def asignar_cliente(self, cliente):
        if not self.activo:
            return False
        
        self.cliente_actual = cliente
        self.tiempo_restante = cliente.tiempo_total_atencion
        cliente.tiempo_inicio_atencion = self.obtener_tiempo_actual()
        return True
    
    def avanzar_tiempo(self, tiempo):
        if self.esta_libre():
            return None
        
        self.tiempo_restante -= tiempo
        
        if self.tiempo_restante <= 0:
            cliente_terminado = self.cliente_actual
            cliente_terminado.tiempo_fin_atencion = self.obtener_tiempo_actual()
            
            # Actualizar estadísticas
            tiempo_atencion = cliente_terminado.tiempo_total_atencion
            self.tiempo_total_atencion += tiempo_atencion
            self.tiempo_max_atencion = max(self.tiempo_max_atencion, tiempo_atencion)
            self.tiempo_min_atencion = min(self.tiempo_min_atencion, tiempo_atencion)
            self.clientes_atendidos += 1
            
            # Liberar escritorio
            self.cliente_actual = None
            self.tiempo_restante = 0
            
            return cliente_terminado
        
        return None
    
    def obtener_tiempo_actual(self):
        # En un sistema real, esto sería el tiempo del sistema
        # Para simplificar, simularemos un contador de tiempo
        return 0  # Placeholder
    
    def obtener_estadisticas(self):
        tiempo_promedio_atencion = 0
        if self.clientes_atendidos > 0:
            tiempo_promedio_atencion = self.tiempo_total_atencion / self.clientes_atendidos
        
        tiempo_min_atencion = self.tiempo_min_atencion
        if tiempo_min_atencion == float('inf'):
            tiempo_min_atencion = 0
        
        return {
            "id": self.id,
            "identificacion": self.identificacion,
            "encargado": self.encargado,
            "activo": self.activo,
            "clientes_atendidos": self.clientes_atendidos,
            "tiempo_promedio_atencion": tiempo_promedio_atencion,
            "tiempo_max_atencion": self.tiempo_max_atencion,
            "tiempo_min_atencion": tiempo_min_atencion
        }
    
    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        if self.cliente_actual:
            return f"Escritorio: {self.identificacion} (ID: {self.id}, Encargado: {self.encargado}, Estado: {estado}, Atendiendo a: {self.cliente_actual.nombre})"
        else:
            return f"Escritorio: {self.identificacion} (ID: {self.id}, Encargado: {self.encargado}, Estado: {estado}, Libre)"
        