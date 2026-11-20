"""Datos de prueba escritos en el codigo.

Al iniciar, el sistema carga 10 ciudades, 15 rutas directas, 5 viajes,
24 pasajes activos, 1 anulacion en la pila y 2 pasajeros en espera.
Asi se puede demostrar el sistema sin usar archivos ni base de datos.
"""

from clases import Bus, Ciudad, Viaje
from sistema import SistemaTransporte


# Crea el sistema y carga todos los datos de prueba.
def cargar_sistema():
    sistema = SistemaTransporte()

    # 1. Ciudades del grafo: (nombre, codigo, departamento).
    ciudades = [
        ("Nueva Cajamarca", "NCJ", "San Martin"),
        ("Moyobamba", "MOY", "San Martin"),
        ("Tarapoto", "TAR", "San Martin"),
        ("Rioja", "RIO", "San Martin"),
        ("Bagua Grande", "BAG", "Amazonas"),
        ("Chiclayo", "CHI", "Lambayeque"),
        ("Trujillo", "TRU", "La Libertad"),
        ("Sullana", "SUL", "Piura"),
        ("Piura", "PIU", "Piura"),
        ("Lima", "LIM", "Lima"),
    ]
    for posicion in range(len(ciudades)):
        datos = ciudades[posicion]
        sistema.agregar_ciudad(Ciudad(datos[0], datos[1], datos[2]))

    # 2. Rutas directas del grafo: (origen, destino).
    rutas = [
        ("Nueva Cajamarca", "Moyobamba"),
        ("Moyobamba", "Nueva Cajamarca"),
        ("Nueva Cajamarca", "Tarapoto"),
        ("Tarapoto", "Nueva Cajamarca"),
        ("Nueva Cajamarca", "Rioja"),
        ("Rioja", "Nueva Cajamarca"),
        ("Rioja", "Moyobamba"),
        ("Moyobamba", "Tarapoto"),
        ("Tarapoto", "Chiclayo"),
        ("Chiclayo", "Trujillo"),
        ("Trujillo", "Sullana"),
        ("Sullana", "Piura"),
        ("Piura", "Lima"),
        ("Nueva Cajamarca", "Bagua Grande"),
        ("Bagua Grande", "Chiclayo"),
    ]
    for posicion in range(len(rutas)):
        sistema.agregar_ruta(rutas[posicion][0], rutas[posicion][1])

    # 3. Viajes: (codigo, origen, destino, fecha, hora, precio, placa,
    #             tipo de bus, filas, columnas).
    viajes = [
        ("V001", "Nueva Cajamarca", "Moyobamba", "2026-12-02", "06:00", 25.0, "MGB-101", "Bus normal", 10, 4),
        ("V002", "Nueva Cajamarca", "Tarapoto", "2026-12-02", "08:30", 35.0, "MGB-102", "Bus normal", 10, 4),
        ("V003", "Nueva Cajamarca", "Rioja", "2026-12-02", "10:00", 12.0, "MGB-103", "Bus normal", 8, 4),
        ("V004", "Tarapoto", "Chiclayo", "2026-12-02", "19:00", 90.0, "MGB-104", "Bus cama", 10, 4),
        ("V005", "Nueva Cajamarca", "Bagua Grande", "2026-12-02", "14:00", 20.0, "MGB-105", "Minibus", 2, 2),
    ]
    for posicion in range(len(viajes)):
        datos = viajes[posicion]
        bus = Bus(datos[6], datos[7], datos[8], datos[9])
        viaje = Viaje(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], bus)
        sistema.agregar_viaje(viaje)

    # 4. Pasajes ya vendidos: (viaje, dni, nombre, edad, telefono,
    #                          condicion, fila, columna).
    ventas = [
        ("V001", "70123456", "Ana Torres Rojas", 28, "987654321", "Normal", 1, 1),
        ("V001", "70123457", "Luis Mendoza Diaz", 35, "987654322", "Normal", 1, 2),
        ("V001", "70123458", "Maria Paredes Ruiz", 67, "987654323", "Adulto mayor", 2, 1),
        ("V001", "70123459", "Jorge Vela Flores", 42, "987654324", "Normal", 2, 2),
        ("V001", "70123460", "Rosa Chavez Silva", 30, "987654325", "Normal", 3, 1),
        ("V001", "70123461", "Pedro Saavedra Lopez", 55, "987654326", "Normal", 3, 2),
        ("V001", "70123462", "Elena Rios Campos", 26, "987654327", "Normal", 4, 1),
        ("V001", "70123463", "Carlos Pinedo Ruiz", 38, "987654328", "Normal", 4, 2),
        ("V002", "70234561", "Sofia Diaz Vela", 24, "986111222", "Normal", 1, 1),
        ("V002", "70234562", "Miguel Angel Rojas", 45, "986111223", "Normal", 1, 2),
        ("V002", "70234563", "Carmen Flores Ruiz", 72, "986111224", "Adulto mayor", 2, 1),
        ("V002", "70234564", "Jose Luis Torres", 33, "986111225", "Normal", 2, 2),
        ("V002", "70234565", "Lucia Pinedo Vega", 29, "986111226", "Normal", 3, 1),
        ("V002", "70234566", "Raul Campos Diaz", 51, "986111227", "Normal", 3, 2),
        ("V003", "70345671", "Patricia Ruiz Rios", 40, "987222333", "Normal", 1, 1),
        ("V003", "70345672", "Fernando Vela Diaz", 19, "987222334", "Normal", 1, 3),
        ("V003", "70345673", "Juana Campos Torres", 69, "987222335", "Adulto mayor", 2, 1),
        ("V003", "70345674", "Diego Mendoza Rios", 27, "987222336", "Normal", 2, 3),
        ("V004", "70456781", "Andrea Silva Paredes", 31, "988333444", "Normal", 1, 1),
        ("V004", "70456782", "Ricardo Torres Vela", 48, "988333445", "Normal", 1, 2),
        ("V004", "70456783", "Milagros Rios Campos", 22, "988333446", "Normal", 2, 1),
        ("V005", "70567891", "Ruth Paredes Diaz", 36, "989444555", "Normal", 1, 1),
        ("V005", "70567892", "Hugo Vela Ruiz", 58, "989444556", "Normal", 1, 2),
        ("V005", "70567893", "Teresa Campos Flores", 64, "989444557", "Normal", 2, 1),
        ("V005", "70567894", "Ivan Mendoza Silva", 25, "989444558", "Normal", 2, 2),
    ]
    for posicion in range(len(ventas)):
        datos = ventas[posicion]
        sistema.vender_pasaje(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7])

    # 5. Una anulacion de prueba para que la pila no empiece vacia.
    sistema.anular_pasaje("V002", "70234566")

    # 6. Dos pasajeros en la cola de espera del viaje V005 (esta lleno).
    sistema.anotar_en_espera("V005", "70678901", "Gladys Rojas Pinedo", 44, "990555666", "Normal")
    sistema.anotar_en_espera("V005", "70678902", "Oscar Torres Campos", 70, "990555667", "Adulto mayor")

    # 7. Se calcula Warshall una vez para dejar listo el grafo.
    sistema.grafo.calcular_warshall()
    return sistema
