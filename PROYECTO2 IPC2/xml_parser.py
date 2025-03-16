# xml_parser.py
import xml.etree.ElementTree as ET
from Empresa import Empresa
from PuntoAtencion import PuntoAtencion
from Escritorio import Escritorio
from Transaccion import Transaccion
from Cliente import Cliente

class XMLParser:
    @staticmethod
    def parse_config_file(file_path):
        """
        Parsea el archivo XML de configuración y crea las empresas con sus puntos de atención,
        escritorios y transacciones.
        
        Args:
            file_path (str): Ruta al archivo XML de configuración
            
        Returns:
            list: Lista de objetos Empresa creados a partir del XML
        """
        empresas = []
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            print("Archivo XML cargado correctamente.")  # Mensaje de depuración
            
            for empresa_element in root.findall('./empresa'):
                id_empresa = empresa_element.get('id')
                nombre = empresa_element.find('nombre').text.strip() if empresa_element.find('nombre') is not None else ""
                abreviatura = empresa_element.find('abreviatura').text.strip() if empresa_element.find('abreviatura') is not None else ""
                
                print(f"Empresa encontrada: ID={id_empresa}, Nombre={nombre}, Abreviatura={abreviatura}")  # Mensaje de depuración
                
                if not id_empresa:
                    print("Error: ID de empresa no encontrado, saltando empresa")
                    continue
                    
                empresa = Empresa(id_empresa, nombre, abreviatura)
                empresas.append(empresa)
            
            print(f"Configuración cargada exitosamente. {len(empresas)} empresas creadas.")  # Mensaje de depuración
            return empresas
        except Exception as e:
            print(f"Error al parsear el archivo de configuración: {e}")  # Mensaje de depuración
            return []

    @staticmethod
    def parse_initial_state(file_path, empresas):
        """
        Parsea el archivo XML de estado inicial y configura los escritorios activos y clientes en cola.
        
        Args:
            file_path (str): Ruta al archivo XML de estado inicial
            empresas (list): Lista de objetos Empresa disponibles
            
        Returns:
            bool: True si el parseo fue exitoso, False en caso contrario
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            configs_procesadas = 0
            
            for config_element in root.findall('./configInicial'):
                id_config = config_element.get('id')
                id_empresa = config_element.get('idEmpresa')
                id_punto = config_element.get('idPunto')
                
                # Validar que los IDs existan
                if not id_config or not id_empresa or not id_punto:
                    print("Error: Configuración inicial incompleta, falta ID de configuración, empresa o punto")
                    continue
                
                # Buscar la empresa y el punto de atención
                empresa = None
                for emp in empresas:
                    if emp.id == id_empresa:
                        empresa = emp
                        break
                
                if not empresa:
                    print(f"Error: Empresa con ID {id_empresa} no encontrada")
                    continue
                
                punto = empresa.buscar_punto_atencion(id_punto)
                if not punto:
                    print(f"Error: Punto de atención con ID {id_punto} no encontrado en la empresa {empresa.nombre}")
                    continue
                
                # Activar escritorios
                escritorios_activos = config_element.find('escritoriosActivos')
                escritorios_activados = 0
                if escritorios_activos is not None:
                    for escritorio_element in escritorios_activos.findall('./escritorio'):
                        id_escritorio = escritorio_element.get('idEscritorio')
                        if not id_escritorio:
                            print("Error: ID de escritorio no encontrado en la configuración inicial")
                            continue
                        
                        if punto.activar_escritorio(id_escritorio):
                            escritorios_activados += 1
                        else:
                            print(f"Advertencia: No se pudo activar el escritorio con ID {id_escritorio}")
                
                # Agregar clientes
                listado_clientes = config_element.find('listadoClientes')
                clientes_agregados = 0
                if listado_clientes is not None:
                    for cliente_element in listado_clientes.findall('./cliente'):
                        dpi = cliente_element.get('dpi')
                        if not dpi:
                            print("Error: DPI de cliente no encontrado, saltando cliente")
                            continue
                            
                        nombre_element = cliente_element.find('nombre')
                        nombre = nombre_element.text.strip() if nombre_element is not None else f"Cliente {dpi}"
                        
                        cliente = Cliente(dpi, nombre)
                        
                        # Agregar transacciones al cliente
                        transacciones = cliente_element.find('listadoTransacciones')
                        transacciones_agregadas = 0
                        if transacciones is not None:
                            for transaccion_element in transacciones.findall('./transaccion'):
                                id_transaccion = transaccion_element.get('idTransaccion')
                                if not id_transaccion:
                                    print(f"Error: ID de transacción no encontrado para cliente {dpi}, saltando transacción")
                                    continue
                                
                                try:
                                    cantidad = int(transaccion_element.get('cantidad', '1'))
                                    if cantidad <= 0:
                                        print(f"Advertencia: Cantidad inválida ({cantidad}) para transacción {id_transaccion}, usando valor por defecto de 1")
                                        cantidad = 1
                                except ValueError:
                                    print(f"Error al convertir cantidad para transacción {id_transaccion}, usando valor por defecto de 1")
                                    cantidad = 1
                                
                                transaccion = empresa.buscar_transaccion(id_transaccion)
                                if transaccion:
                                    cliente.agregar_transaccion(transaccion, cantidad)
                                    transacciones_agregadas += 1
                                else:
                                    print(f"Advertencia: Transacción con ID {id_transaccion} no encontrada en la empresa {empresa.nombre}")
                        
                        # Solo agregar cliente si tiene al menos una transacción
                        if transacciones_agregadas > 0:
                            punto.agregar_cliente(cliente)
                            clientes_agregados += 1
                        else:
                            print(f"Advertencia: Cliente {dpi} no tiene transacciones válidas, no se agregará")
                
                print(f"Configuración inicial {id_config} procesada exitosamente. Se activaron {escritorios_activados} escritorios y se agregaron {clientes_agregados} clientes.")
                configs_procesadas += 1
            
            return configs_procesadas > 0
        
        except Exception as e:
            print(f"Error al parsear el archivo de estado inicial: {e}")
            return False