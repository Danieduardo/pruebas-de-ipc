# PuntoAtencion.py
from Cola import Cola
from Pila import Pila
from ListaSimple import ListaSimple
import time

class PuntoAtencion:
    def __init__(self, id, nombre, direccion):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.escritorios = ListaSimple()  # Lista de escritorios
        self.clientes_espera = Cola()     # Cola de clientes en espera
        self.escritorios_activos = Pila() # Pila de escritorios activos (LIFO)
                
        # Estadísticas
        self.clientes_atendidos = 0
        self.tiempo_total_espera = 0
        self.tiempo_max_espera = 0
        self.tiempo_min_espera = float('inf')
        self.tiempo_total_atencion = 0
        self.tiempo_max_atencion = 0
        self.tiempo_min_atencion = float('inf')
        self.tiempo_actual = 0  # Simulación de tiempo
    
    def agregar_escritorio(self, escritorio):
        self.escritorios.insertar(escritorio)
    
    def buscar_escritorio(self, id_escritorio):
        actual = self.escritorios.primero
        while actual:
            if actual.dato.id == id_escritorio:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def activar_escritorio(self, id_escritorio):
        escritorio = self.buscar_escritorio(id_escritorio)
        if escritorio and not escritorio.activo:
            escritorio.activar()
            self.escritorios_activos.apilar(escritorio)
            self.asignar_cliente_a_escritorio(escritorio)
            return True
        return False
    
    def desactivar_escritorio(self, id_escritorio):
        escritorio = self.buscar_escritorio(id_escritorio)
        if escritorio and escritorio.activo:
            escritorio.desactivar()
            # Nota: No lo quitamos de la pila, simplemente lo marcamos como inactivo
            return True
        return False
    
    def agregar_cliente(self, cliente):
        # Iniciar tiempo de espera
        cliente.iniciar_espera(self.tiempo_actual)
        
        # Buscar escritorio libre y activo
        escritorio_libre = self.buscar_escritorio_libre()
        
        if escritorio_libre:
            # Asignar cliente directamente al escritorio
            cliente.terminar_espera(self.tiempo_actual)
            self.actualizar_estadisticas_espera(cliente)
            escritorio_libre.asignar_cliente(cliente)
            return cliente.tiempo_total_atencion
        else:
            # Poner cliente en cola de espera
            self.clientes_espera.encolar(cliente)
            # Estimar tiempo de espera
            return self.estimar_tiempo_espera()
    
    def buscar_escritorio_libre(self):
        actual = self.escritorios.primero
        while actual:
            if actual.dato.activo and actual.dato.esta_libre():
                return actual.dato
            actual = actual.siguiente
        return None
    
    def asignar_cliente_a_escritorio(self, escritorio):
        if not escritorio.activo or not escritorio.esta_libre():
            return False
        
        if not self.clientes_espera.esta_vacia():
            cliente = self.clientes_espera.desencolar()
            cliente.terminar_espera(self.tiempo_actual)
            self.actualizar_estadisticas_espera(cliente)
            escritorio.asignar_cliente(cliente)
            return True
        
        return False
    
    def atender_cliente(self):
        # Simular la finalización de la atención del cliente más próximo a terminar
        tiempo_minimo = float('inf')
        escritorio_proximo = None
        
        actual = self.escritorios.primero
        while actual:
            if actual.dato.activo and not actual.dato.esta_libre() and actual.dato.tiempo_restante < tiempo_minimo:
                tiempo_minimo = actual.dato.tiempo_restante
                escritorio_proximo = actual.dato
            actual = actual.siguiente
        
        if escritorio_proximo:
            # Avanzar el tiempo para todos los escritorios
            self.tiempo_actual += tiempo_minimo
            
            # Procesar la atención de los clientes
            escritorios_terminados = []
            
            actual = self.escritorios.primero
            while actual:
                if actual.dato.activo and not actual.dato.esta_libre():
                    cliente_terminado = actual.dato.avanzar_tiempo(tiempo_minimo)
                    if cliente_terminado:
                        escritorios_terminados.append(actual.dato)
                        self.actualizar_estadisticas_atencion(cliente_terminado)
                        self.clientes_atendidos += 1
                actual = actual.siguiente
            
            # Asignar nuevos clientes a los escritorios que terminaron
            for escritorio in escritorios_terminados:
                if escritorio.activo:
                    self.asignar_cliente_a_escritorio(escritorio)
            
            return True
        
        return False
    
    def simular_actividad(self):
        # Simular la atención completa de todos los clientes
        while not self.clientes_espera.esta_vacia() or self.hay_clientes_en_atencion():
            self.atender_cliente()
    
    def hay_clientes_en_atencion(self):
        actual = self.escritorios.primero
        while actual:
            if actual.dato.activo and not actual.dato.esta_libre():
                return True
            actual = actual.siguiente
        return False
    
    def estimar_tiempo_espera(self):
        # Estimación básica: sumar tiempos restantes de escritorios y clientes en cola
        tiempo_total = 0
        
        # Sumar tiempo de los clientes en escritorios
        actual = self.escritorios.primero
        while actual:
            if actual.dato.activo and not actual.dato.esta_libre():
                tiempo_total += actual.dato.tiempo_restante
            actual = actual.siguiente
        
        # Sumar tiempo de los clientes en cola
        actual = self.clientes_espera.primero
        contador = 0
        escritorios_activos_count = self.contar_escritorios_activos()
        
        while actual:
            if escritorios_activos_count > 0:
                tiempo_total += actual.dato.tiempo_total_atencion / escritorios_activos_count
            contador += 1
            actual = actual.siguiente
        
        return tiempo_total / max(1, self.contar_escritorios_activos())
    
    def contar_escritorios_activos(self):
        count = 0
        actual = self.escritorios.primero
        while actual:
            if actual.dato.activo:
                count += 1
            actual = actual.siguiente
        return count
    
    def contar_escritorios_inactivos(self):
        count = 0
        actual = self.escritorios.primero
        while actual:
            if not actual.dato.activo:
                count += 1
            actual = actual.siguiente
        return count
    
    def actualizar_estadisticas_espera(self, cliente):
        tiempo_espera = cliente.tiempo_espera
        self.tiempo_total_espera += tiempo_espera
        self.tiempo_max_espera = max(self.tiempo_max_espera, tiempo_espera)
        self.tiempo_min_espera = min(self.tiempo_min_espera, tiempo_espera) if tiempo_espera > 0 else self.tiempo_min_espera
    
    def actualizar_estadisticas_atencion(self, cliente):
        tiempo_atencion = cliente.tiempo_total_atencion
        self.tiempo_total_atencion += tiempo_atencion
        self.tiempo_max_atencion = max(self.tiempo_max_atencion, tiempo_atencion)
        self.tiempo_min_atencion = min(self.tiempo_min_atencion, tiempo_atencion)
    
    def obtener_estadisticas(self):
        escritorios_activos = self.contar_escritorios_activos()
        escritorios_inactivos = self.contar_escritorios_inactivos()
        clientes_espera = self.clientes_espera.tamanio
        
        tiempo_promedio_espera = 0
        if self.clientes_atendidos > 0:
            tiempo_promedio_espera = self.tiempo_total_espera / self.clientes_atendidos
        
        tiempo_promedio_atencion = 0
        if self.clientes_atendidos > 0:
            tiempo_promedio_atencion = self.tiempo_total_atencion / self.clientes_atendidos
        
        tiempo_min_espera = self.tiempo_min_espera
        if tiempo_min_espera == float('inf'):
            tiempo_min_espera = 0
        
        tiempo_min_atencion = self.tiempo_min_atencion
        if tiempo_min_atencion == float('inf'):
            tiempo_min_atencion = 0
        
        return {
            "id": self.id,
            "nombre": self.nombre,
            "escritorios_activos": escritorios_activos,
            "escritorios_inactivos": escritorios_inactivos,
            "clientes_espera": clientes_espera,
            "clientes_atendidos": self.clientes_atendidos,
            "tiempo_promedio_espera": tiempo_promedio_espera,
            "tiempo_max_espera": self.tiempo_max_espera,
            "tiempo_min_espera": tiempo_min_espera,
            "tiempo_promedio_atencion": tiempo_promedio_atencion,
            "tiempo_max_atencion": self.tiempo_max_atencion,
            "tiempo_min_atencion": tiempo_min_atencion
        }
    
    def __str__(self):
        return f"Punto de Atención: {self.nombre} (ID: {self.id}, Dirección: {self.direccion})"