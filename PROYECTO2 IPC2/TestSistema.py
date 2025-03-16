# test_sistema.py
import unittest
from SistemaAtencionClientes import SistemaAtencionClientes
from Empresa import Empresa
from PuntoAtencion import PuntoAtencion
from Escritorio import Escritorio

class TestSistema(unittest.TestCase):
    def test_crear_empresa(self):
        sistema = SistemaAtencionClientes()
        empresa = sistema.crear_empresa(1, "Empresa 1", "E1")
        self.assertIsNotNone(empresa)
        self.assertEqual(empresa.nombre, "Empresa 1")

    def test_crear_punto_atencion(self):
        sistema = SistemaAtencionClientes()
        sistema.crear_empresa(1, "Empresa 1", "E1")
        resultado = sistema.crear_punto_atencion(1, 1, "Punto 1", "Dirección 1")
        self.assertTrue(resultado)

    def test_crear_escritorio(self):
        sistema = SistemaAtencionClientes()
        sistema.crear_empresa(1, "Empresa 1", "E1")
        sistema.crear_punto_atencion(1, 1, "Punto 1", "Dirección 1")
        resultado = sistema.crear_escritorio(1, 1, 1, "Escritorio 1", "Encargado 1")
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()