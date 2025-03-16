from nodo import Nodo

class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0
    
    def esta_vacia(self):
        return self.primero is None
    
    def encolar(self, dato):
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        
        self.tamanio += 1
    
    def desencolar(self):
        if self.esta_vacia():
            return None
        
        dato = self.primero.dato
        self.primero = self.primero.siguiente
        
        if self.primero is None:
            self.ultimo = None
        
        self.tamanio -= 1
        return dato
    
    def frente(self):
        if self.esta_vacia():
            return None
        return self.primero.dato
    
    def imprimir(self):
        if self.esta_vacia():
            print("Cola vacía")
            return
        
        actual = self.primero
        while actual:
            print(actual.dato)
            actual = actual.siguiente