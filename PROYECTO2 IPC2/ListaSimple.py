# ListaSimple.py
from nodo import Nodo

class ListaSimple:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def esta_vacia(self):
        return self.primero is None
    
    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        
        self.tamanio += 1
    
    def insertar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero = nuevo_nodo
        
        self.tamanio += 1
    
    def eliminar(self, dato):
        if self.esta_vacia():
            return False
        
        actual = self.primero
        anterior = None
        
        while actual and actual.dato != dato:
            anterior = actual
            actual = actual.siguiente
        
        if actual is None:
            return False
        
        if anterior is None:
            self.primero = actual.siguiente
            if self.primero is None:
                self.ultimo = None
        else:
            anterior.siguiente = actual.siguiente
            if anterior.siguiente is None:
                self.ultimo = anterior
        
        self.tamanio -= 1
        return True
    
    def buscar(self, dato):
        actual = self.primero
        
        while actual:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        
        return None
    
    def obtener_por_indice(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        
        actual = self.primero
        contador = 0
        
        while contador < indice:
            actual = actual.siguiente
            contador += 1
        
        return actual.dato
    
    def imprimir(self):
        if self.esta_vacia():
            print("Lista vacía")
            return
        
        actual = self.primero
        while actual:
            print(actual.dato)
            actual = actual.siguiente