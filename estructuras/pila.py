"""Pila (LIFO) implementada a mano con la clase Nodo.

Se usa para guardar las anulaciones de pasajes. La ultima anulacion
queda en el tope y es la primera que se puede deshacer.
"""

from estructuras.nodo import Nodo


class Pila:
    """Pila enlazada: apilar, desapilar y consultar el tope."""

    # Crea una pila vacia.
    def __init__(self):
        self.tope = None
        self.tamanio = 0

    # Indica si la pila no tiene elementos.
    def esta_vacia(self):
        return self.tope is None

    # Agrega un dato en el tope de la pila.
    def apilar(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamanio = self.tamanio + 1

    # Quita y devuelve el dato que esta en el tope (o None si esta vacia).
    def desapilar(self):
        if self.tope is None:
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamanio = self.tamanio - 1
        return dato

    # Devuelve el dato del tope sin quitarlo de la pila.
    def cima(self):
        if self.tope is None:
            return None
        return self.tope.dato

    # Devuelve cuantos elementos tiene la pila.
    def contar(self):
        return self.tamanio

    # Muestra los elementos desde el tope hasta el fondo.
    def mostrar(self):
        if self.tope is None:
            print("  (La pila esta vacia)")
            return
        actual = self.tope
        primero = True
        while actual is not None:
            if primero:
                print("  TOPE -> " + str(actual.dato))
                primero = False
            else:
                print("          " + str(actual.dato))
            actual = actual.siguiente
