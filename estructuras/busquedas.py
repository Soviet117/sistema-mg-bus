"""Algoritmos de busqueda programados por el equipo.

No se usan las funciones in ni index de Python. La busqueda secuencial
recorre el arreglo desde el inicio; la busqueda binaria divide el
arreglo ordenado por la mitad en cada paso.
"""


# Busca un valor recorriendo el arreglo desde la primera posicion.
# Devuelve la posicion encontrada o -1 si el valor no existe.
def busqueda_secuencial(arreglo, objetivo):
    posicion = 0
    while posicion < len(arreglo):
        if arreglo[posicion] == objetivo:
            return posicion
        posicion = posicion + 1
    return -1


# Busca un valor en un arreglo ordenado dividiendo el rango a la mitad.
# Devuelve la posicion encontrada o -1 si el valor no existe.
def busqueda_binaria(arreglo_ordenado, objetivo):
    inicio = 0
    fin = len(arreglo_ordenado) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        valor_medio = arreglo_ordenado[medio]
        if valor_medio == objetivo:
            return medio
        elif valor_medio < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1
