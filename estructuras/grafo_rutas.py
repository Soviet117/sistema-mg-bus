"""Grafo dirigido de ciudades y algoritmo de Warshall.

La matriz de adyacencia guarda 1 cuando existe una ruta directa entre
dos ciudades y 0 cuando no existe. Warshall calcula la matriz de
alcanzabilidad: 1 si se puede llegar a la ciudad destino aunque sea
pasando por otras ciudades.
"""


class GrafoRutas:
    """Grafo dirigido representado con una matriz de adyacencia."""

    # Crea un grafo vacio, sin ciudades ni rutas.
    def __init__(self):
        self.ciudades = []
        self.matriz_adyacencia = []
        self.matriz_alcanzabilidad = None

    # Agrega una ciudad al grafo y amplia las matrices con una fila y columna.
    def agregar_ciudad(self, ciudad):
        for posicion in range(len(self.ciudades)):
            if self.ciudades[posicion].nombre == ciudad.nombre:
                raise ValueError("La ciudad ya esta registrada en el grafo.")
        self.ciudades.append(ciudad)
        for fila in self.matriz_adyacencia:
            fila.append(0)
        nueva_fila = [0] * len(self.ciudades)
        self.matriz_adyacencia.append(nueva_fila)
        self.matriz_alcanzabilidad = None

    # Devuelve la cantidad de ciudades del grafo.
    def cantidad_ciudades(self):
        return len(self.ciudades)

    # Busca la posicion de una ciudad por su nombre con busqueda secuencial.
    def indice_ciudad(self, nombre):
        for posicion in range(len(self.ciudades)):
            if self.ciudades[posicion].nombre == nombre:
                return posicion
        return -1

    # Registra una ruta directa desde la ciudad origen hacia la ciudad destino.
    def agregar_ruta(self, origen, destino):
        posicion_origen = self.indice_ciudad(origen)
        posicion_destino = self.indice_ciudad(destino)
        if posicion_origen == -1:
            raise ValueError("La ciudad de origen no existe en el grafo.")
        if posicion_destino == -1:
            raise ValueError("La ciudad de destino no existe en el grafo.")
        if posicion_origen == posicion_destino:
            raise ValueError("Una ruta debe unir dos ciudades diferentes.")
        self.matriz_adyacencia[posicion_origen][posicion_destino] = 1
        self.matriz_alcanzabilidad = None

    # Indica si existe una ruta directa de origen a destino.
    def es_ruta_directa(self, origen, destino):
        posicion_origen = self.indice_ciudad(origen)
        posicion_destino = self.indice_ciudad(destino)
        if posicion_origen == -1 or posicion_destino == -1:
            return False
        return self.matriz_adyacencia[posicion_origen][posicion_destino] == 1

    # Aplica el algoritmo de Warshall para calcular todas las rutas posibles.
    # Se copia la matriz de adyacencia y se van agregando los caminos con escalas.
    def calcular_warshall(self):
        cantidad = len(self.ciudades)
        alcanzable = []
        for fila in range(cantidad):
            nueva_fila = []
            for columna in range(cantidad):
                # La diagonal es 1 porque una ciudad siempre se alcanza a si misma.
                if fila == columna or self.matriz_adyacencia[fila][columna] == 1:
                    nueva_fila.append(1)
                else:
                    nueva_fila.append(0)
            alcanzable.append(nueva_fila)

        # k es la ciudad intermedia; i es el origen y j es el destino.
        for k in range(cantidad):
            for i in range(cantidad):
                for j in range(cantidad):
                    if alcanzable[i][k] == 1 and alcanzable[k][j] == 1:
                        alcanzable[i][j] = 1

        self.matriz_alcanzabilidad = alcanzable
        return alcanzable

    # Devuelve la matriz de alcanzabilidad, calculandola si aun no existe.
    def obtener_alcanzabilidad(self):
        if self.matriz_alcanzabilidad is None:
            return self.calcular_warshall()
        return self.matriz_alcanzabilidad

    # Indica si se puede viajar de origen a destino, con o sin escalas.
    def existe_ruta(self, origen, destino):
        posicion_origen = self.indice_ciudad(origen)
        posicion_destino = self.indice_ciudad(destino)
        if posicion_origen == -1 or posicion_destino == -1:
            return False
        alcanzable = self.obtener_alcanzabilidad()
        return alcanzable[posicion_origen][posicion_destino] == 1

    # Devuelve los nombres de las ciudades alcanzables desde una ciudad.
    def alcanzables_desde(self, origen):
        posicion_origen = self.indice_ciudad(origen)
        if posicion_origen == -1:
            return []
        alcanzable = self.obtener_alcanzabilidad()
        resultado = []
        for posicion in range(len(self.ciudades)):
            if posicion != posicion_origen and alcanzable[posicion_origen][posicion] == 1:
                resultado.append(self.ciudades[posicion].nombre)
        return resultado

    # Devuelve los nombres de las ciudades con ruta directa desde el origen.
    def destinos_directos(self, origen):
        posicion_origen = self.indice_ciudad(origen)
        if posicion_origen == -1:
            return []
        resultado = []
        for posicion in range(len(self.ciudades)):
            if self.matriz_adyacencia[posicion_origen][posicion] == 1:
                resultado.append(self.ciudades[posicion].nombre)
        return resultado

    # Cuenta cuantas rutas directas tiene registradas el grafo.
    def total_rutas_directas(self):
        total = 0
        for fila in range(len(self.matriz_adyacencia)):
            for columna in range(len(self.matriz_adyacencia)):
                if self.matriz_adyacencia[fila][columna] == 1:
                    total = total + 1
        return total
