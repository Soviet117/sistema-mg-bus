"""Lista enlazada simple para guardar los pasajes de un viaje.

Se implementa a mano con la clase Nodo: cada pasaje apunta al siguiente.
No se usan los metodos append ni pop de las listas de Python para
simular la lista enlazada.
"""

from estructuras.nodo import Nodo


class ListaPasajeros:
    """Lista enlazada simple que almacena objetos Pasaje."""

    # Crea una lista vacia (sin nodos) y su contador en cero.
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    # Indica si la lista no tiene ningun nodo.
    def esta_vacia(self):
        return self.cabeza is None

    # Inserta un pasaje al inicio de la lista.
    def insertar_inicio(self, pasaje):
        nuevo = Nodo(pasaje)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio = self.tamanio + 1

    # Inserta un pasaje al final de la lista (orden de llegada).
    def insertar_final(self, pasaje):
        nuevo = Nodo(pasaje)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio = self.tamanio + 1

    # Busca un pasaje por el DNI del pasajero y lo devuelve (o None).
    def buscar_por_dni(self, dni):
        actual = self.cabeza
        while actual is not None:
            if actual.dato.pasajero.dni == dni:
                return actual.dato
            actual = actual.siguiente
        return None

    # Elimina el pasaje que pertenece al DNI indicado y lo devuelve.
    def eliminar_por_dni(self, dni):
        actual = self.cabeza
        anterior = None
        while actual is not None:
            if actual.dato.pasajero.dni == dni:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self.tamanio = self.tamanio - 1
                return actual.dato
            anterior = actual
            actual = actual.siguiente
        return None

    # Devuelve la cantidad de pasajes guardados en la lista.
    def contar(self):
        return self.tamanio

    # Recorre la lista y devuelve sus datos en un arreglo para reportes.
    # Se crea un arreglo del tamanio exacto; no se usa append.
    def recorrer(self):
        datos = [None] * self.tamanio
        posicion = 0
        actual = self.cabeza
        while actual is not None:
            datos[posicion] = actual.dato
            posicion = posicion + 1
            actual = actual.siguiente
        return datos

    # Muestra en pantalla todos los pasajes de la lista, uno por linea.
    def mostrar(self):
        if self.cabeza is None:
            print("  (La lista de pasajeros esta vacia)")
            return
        actual = self.cabeza
        while actual is not None:
            print("  " + str(actual.dato))
            actual = actual.siguiente
