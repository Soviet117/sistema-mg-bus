"""Clase Nodo compartida por las estructuras enlazadas.

Un nodo guarda un dato y una referencia al siguiente nodo. La lista
enlazada, la pila y la cola usan esta misma clase; lo unico que cambia
es la forma en que conectan sus nodos.
"""


class Nodo:
    """Representa un nodo con un dato y un puntero al siguiente nodo."""

    # Guarda el dato recibido y deja el puntero en None (fin de la estructura).
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
