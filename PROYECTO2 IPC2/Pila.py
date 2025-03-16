from nodo import Nodo

class Pila:
    def __init__(self):
        self.cima = None
        self.tamanio = 0
    
    def esta_vacia(self):
        return self.cima is None
    
    def apilar(self, dato):
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.cima = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cima
            self.cima = nuevo_nodo
        
        self.tamanio += 1
    
    def desapilar(self):
        if self.esta_vacia():
            return None
        
        dato = self.cima.dato
        self.cima = self.cima.siguiente
        self.tamanio -= 1
        return dato
    
    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self.cima.dato
    
    def imprimir(self):
        if self.esta_vacia():
            print("Pila vacía")
            return
        
        actual = self.cima
        while actual:
            print(actual.dato)
            actual = actual.siguiente