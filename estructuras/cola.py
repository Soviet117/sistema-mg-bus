"""Cola (FIFO) implementada a mano con la clase Nodo.

Se usa para la lista de espera de un viaje lleno. El primer pasajero
que se anota es el primero que sera atendido cuando se libere un asiento.
"""

from estructuras.nodo import Nodo


class Cola:
    """Cola enlazada: encolar, desencolar y consultar el frente."""

    # Crea una cola vacia con punteros al primero y al ultimo.
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    # Indica si la cola no tiene elementos.
    def esta_vacia(self):
        return self.primero is None

    # Agrega un dato al final de la cola.
    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.tamanio = self.tamanio + 1

    # Quita y devuelve el primer dato de la cola (o None si esta vacia).
    def desencolar(self):
        if self.primero is None:
            return None
        dato = self.primero.dato
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        self.tamanio = self.tamanio - 1
        return dato

    # Devuelve el primer dato sin quitarlo de la cola.
    def frente(self):
        if self.primero is None:
            return None
        return self.primero.dato

    # Devuelve cuantos elementos tiene la cola.
    def contar(self):
        return self.tamanio

    # Recorre la cola y devuelve sus datos en un arreglo.
    # Se crea un arreglo del tamanio exacto; no se usa append.
    def recorrer(self):
        datos = [None] * self.tamanio
        posicion = 0
        actual = self.primero
        while actual is not None:
            datos[posicion] = actual.dato
            posicion = posicion + 1
            actual = actual.siguiente
        return datos

    # Muestra los elementos desde el frente hasta el final de la cola.
    def mostrar(self):
        if self.primero is None:
            print("  (La cola esta vacia)")
            return
        actual = self.primero
        primero = True
        while actual is not None:
            if primero:
                print("  FRENTE -> " + str(actual.dato))
                primero = False
            else:
                print("            " + str(actual.dato))
            actual = actual.siguiente
