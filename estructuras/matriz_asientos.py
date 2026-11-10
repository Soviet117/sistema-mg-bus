"""Matriz bidimensional que representa los asientos de un bus.

Las filas y columnas se manejan desde 1 para que el usuario escriba,
por ejemplo, fila 3 y columna 2. Internamente la matriz usa indices
desde 0, como toda lista de Python.
"""


class MatrizAsientos:
    """Matriz fija de asientos con estados Libre u Ocupado."""

    LIBRE = "Libre"
    OCUPADO = "Ocupado"

    # Crea la matriz con la cantidad de filas y columnas indicada.
    def __init__(self, filas, columnas):
        if filas <= 0 or columnas <= 0:
            raise ValueError("La cantidad de filas y columnas debe ser mayor que cero.")
        self.filas = filas
        self.columnas = columnas
        self.asientos = []
        for numero_fila in range(filas):
            # Cada fila es un arreglo de asientos libres.
            fila = [self.LIBRE] * columnas
            self.asientos.append(fila)

    # Devuelve la cantidad total de asientos del bus.
    def total_asientos(self):
        return self.filas * self.columnas

    # Verifica que una fila y una columna existan dentro de la matriz.
    def dentro_de_rango(self, fila, columna):
        if fila < 1 or fila > self.filas:
            return False
        if columna < 1 or columna > self.columnas:
            return False
        return True

    # Devuelve el estado actual de un asiento: Libre u Ocupado.
    def estado(self, fila, columna):
        if not self.dentro_de_rango(fila, columna):
            raise ValueError("El asiento indicado no existe.")
        return self.asientos[fila - 1][columna - 1]

    # Indica si un asiento esta libre.
    def esta_libre(self, fila, columna):
        return self.estado(fila, columna) == self.LIBRE

    # Marca un asiento como ocupado; falla si ya estaba ocupado.
    def ocupar(self, fila, columna):
        if not self.esta_libre(fila, columna):
            raise ValueError("Ese asiento ya esta ocupado.")
        self.asientos[fila - 1][columna - 1] = self.OCUPADO

    # Vuelve a dejar libre un asiento.
    def liberar(self, fila, columna):
        if not self.dentro_de_rango(fila, columna):
            raise ValueError("El asiento indicado no existe.")
        self.asientos[fila - 1][columna - 1] = self.LIBRE

    # Cuenta cuantos asientos estan libres recorriendo la matriz.
    def contar_libres(self):
        libres = 0
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.asientos[fila][columna] == self.LIBRE:
                    libres = libres + 1
        return libres

    # Cuenta cuantos asientos estan ocupados.
    def contar_ocupados(self):
        return self.total_asientos() - self.contar_libres()

    # Indica si ya no queda ningun asiento libre.
    def esta_llena(self):
        return self.contar_libres() == 0

    # Busca el primer asiento libre (de arriba a abajo y de izquierda a derecha).
    def primer_asiento_libre(self):
        for fila in range(1, self.filas + 1):
            for columna in range(1, self.columnas + 1):
                if self.esta_libre(fila, columna):
                    return (fila, columna)
        return None

    # Devuelve el texto corto del asiento, por ejemplo F3-C2.
    def etiqueta_asiento(self, fila, columna):
        return "F" + str(fila) + "-C" + str(columna)
