# SistemaAtencionClientes.py
import os
import xml_parser
from Empresa import Empresa
from PuntoAtencion import PuntoAtencion
from Escritorio import Escritorio
from Transaccion import Transaccion
from Cliente import Cliente
from ListaSimple import ListaSimple

class SistemaAtencionClientes:
    def __init__(self):
        self.empresas = ListaSimple()

    def limpiar_sistema(self):
        """Inicializa todas las estructuras de datos para iniciar una prueba desde cero."""
        self.empresas = ListaSimple()
        print("Sistema limpiado correctamente")

    def cargar_configuracion(self, ruta_archivo):
        """Carga el archivo XML de configuración del sistema."""
        if not os.path.exists(ruta_archivo):
            print(f"Error: El archivo {ruta_archivo} no existe.")
            return False

        empresas_parsed = xml_parser.parse_config_file(ruta_archivo)
        for empresa in empresas_parsed:
            self.agregar_empresa(empresa)

        return len(empresas_parsed) > 0

    def cargar_configuracion_inicial(self, ruta_archivo):
        """Carga el archivo XML con configuración inicial para la prueba."""
        if not os.path.exists(ruta_archivo):
            print(f"Error: El archivo {ruta_archivo} no existe.")
            return False

        # Convertir lista enlazada a lista Python para pasar a XMLParser
        empresas_list = []
        actual = self.empresas.primero
        while actual:
            empresas_list.append(actual.dato)
            actual = actual.siguiente

        return xml_parser.parse_initial_state(ruta_archivo, empresas_list)

    def agregar_empresa(self, empresa):
        """Agrega una nueva empresa al sistema."""
        # Verificar si ya existe una empresa con el mismo ID
        actual = self.empresas.primero
        while actual:
            if actual.dato.id == empresa.id:
                print(f"Advertencia: Ya existe una empresa con ID {empresa.id}, no se agregará.")
                return False
            actual = actual.siguiente

        self.empresas.insertar(empresa)
        print(f"Empresa agregada: {empresa.nombre}")  # Mensaje de depuración
        return True

    def crear_empresa(self, id, nombre, abreviatura):
        """Crea una nueva empresa y la agrega al sistema."""
        empresa = Empresa(id, nombre, abreviatura)
        return self.agregar_empresa(empresa)

    def crear_punto_atencion(self, id_empresa, id_punto, nombre, direccion):
        """Crea un punto de atención para una empresa existente."""
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            print(f"Error: Empresa con ID {id_empresa} no encontrada.")
            return False

        # Verificar que no exista un punto con el mismo ID
        actual = empresa.puntos_atencion.primero
        while actual:
            if actual.dato.id == id_punto:
                print(f"Error: Ya existe un punto de atención con el ID {id_punto}")
                return False
            actual = actual.siguiente

        punto = PuntoAtencion(id_punto, nombre, direccion)
        empresa.agregar_punto_atencion(punto)
        return True

    def crear_escritorio(self, id_empresa, id_punto, id_escritorio, identificacion, encargado):
        """Crea un escritorio de servicio en un punto de atención existente."""
        empresa = self.buscar_empresa(id_empresa)
        if not empresa:
            print(f"Error: Empresa con ID {id_empresa} no encontrada.")
            return False

        punto = empresa.buscar_punto_atencion(id_punto)
        if not punto:
            print(f"Error: Punto de atención con ID {id_punto} no encontrado.")
            return False

        # Verificar que no exista un escritorio con el mismo ID
        actual = punto.escritorios.primero
        while actual:
            if actual.dato.id == id_escritorio:
                print(f"Error: Ya existe un escritorio con el ID {id_escritorio}")
                return False
            actual = actual.siguiente

        escritorio = Escritorio(id_escritorio, identificacion, encargado)
        punto.agregar_escritorio(escritorio)
        return True

    def buscar_empresa(self, id_empresa):
        """Busca una empresa por su ID."""
        actual = self.empresas.primero
        while actual:
            if actual.dato.id == id_empresa:
                return actual.dato
            actual = actual.siguiente
        return None

    def simular_actividad(self, tiempo_simulacion):
        """
        Simula la atención de clientes durante un tiempo específico.
        
        Args:
            tiempo_simulacion (int): Tiempo de simulación en minutos.
        """
        if tiempo_simulacion <= 0:
            print("Error: El tiempo de simulación debe ser mayor que 0.")
            return

        # Simular la atención en todos los puntos de atención de todas las empresas
        actual_empresa = self.empresas.primero
        while actual_empresa:
            actual_punto = actual_empresa.dato.puntos_atencion.primero
            while actual_punto:
                actual_punto.dato.simular_actividad()
                actual_punto = actual_punto.siguiente
            actual_empresa = actual_empresa.siguiente

        print(f"Simulación completada durante {tiempo_simulacion} minutos.")