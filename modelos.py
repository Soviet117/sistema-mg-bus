"""Clases del dominio del sistema de transporte.

Aqui estan las entidades del negocio: Ciudad, Bus, Viaje, Pasajero y
Pasaje. Cada clase agrupa sus datos y las operaciones basicas que le
corresponden.
"""

from estructuras.cola import Cola
from estructuras.lista_pasajeros import ListaPasajeros
from estructuras.matriz_asientos import MatrizAsientos

# Condiciones especiales que se registran en la entrevista.
CONDICIONES = ("Normal", "Adulto mayor", "Discapacitado", "Embarazada")


class Ciudad:
    """Ciudad que forma parte del grafo de rutas."""

    # Guarda el nombre, el codigo corto y el departamento de la ciudad.
    def __init__(self, nombre, codigo, departamento):
        self.nombre = nombre
        self.codigo = codigo
        self.departamento = departamento

    # Devuelve el nombre de la ciudad con su codigo.
    def __str__(self):
        return self.nombre + " (" + self.codigo + ")"


class Bus:
    """Bus con su placa, su tipo y su matriz de asientos."""

    # Crea el bus y su matriz de asientos con las filas y columnas indicadas.
    def __init__(self, placa, tipo, filas, columnas):
        self.placa = placa
        self.tipo = tipo
        self.filas = filas
        self.columnas = columnas
        self.matriz_asientos = MatrizAsientos(filas, columnas)

    # Devuelve la cantidad total de asientos del bus.
    def total_asientos(self):
        return self.matriz_asientos.total_asientos()

    # Devuelve una descripcion corta del bus.
    def __str__(self):
        return self.tipo + " " + self.placa + " (" + str(self.filas) + "x" + str(self.columnas) + ")"


class Viaje:
    """Servicio programado entre dos ciudades, con su bus y sus pasajeros."""

    # Guarda los datos del viaje y crea su lista de pasajeros y su cola de espera.
    def __init__(self, codigo, origen, destino, fecha, hora, precio, bus):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.fecha = fecha
        self.hora = hora
        self.precio = precio
        self.bus = bus
        self.matriz_asientos = bus.matriz_asientos
        self.pasajeros = ListaPasajeros()
        self.espera = Cola()

    # Devuelve el texto de la ruta, por ejemplo Nueva Cajamarca -> Tarapoto.
    def descripcion_ruta(self):
        return self.origen + " -> " + self.destino

    # Devuelve cuantos asientos quedan libres en el bus.
    def asientos_libres(self):
        return self.matriz_asientos.contar_libres()

    # Devuelve la cantidad total de asientos del viaje.
    def total_asientos(self):
        return self.matriz_asientos.total_asientos()

    # Indica si el viaje ya no tiene asientos disponibles.
    def esta_lleno(self):
        return self.matriz_asientos.esta_llena()

    # Busca un pasaje del viaje por el DNI del pasajero.
    def buscar_pasajero_por_dni(self, dni):
        return self.pasajeros.buscar_por_dni(dni)

    # Agrega un pasaje a la lista enlazada del viaje.
    def agregar_pasajero(self, pasaje):
        self.pasajeros.insertar_final(pasaje)

    # Quita un pasaje del viaje por el DNI y lo devuelve.
    def quitar_pasajero(self, dni):
        return self.pasajeros.eliminar_por_dni(dni)

    # Devuelve la cantidad de pasajeros que tiene el viaje.
    def cantidad_pasajeros(self):
        return self.pasajeros.contar()

    # Devuelve una descripcion corta del viaje.
    def __str__(self):
        return self.codigo + ": " + self.descripcion_ruta() + " | " + self.fecha + " " + self.hora


class Pasajero:
    """Persona que compra un pasaje."""

    # Guarda los datos personales del pasajero.
    def __init__(self, dni, nombre, edad, telefono, condicion):
        self.dni = dni
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.condicion = condicion

    # Indica si el pasajero debe recibir atencion preferente.
    def es_prioritario(self):
        if self.condicion != "Normal":
            return True
        return self.edad >= 65

    # Devuelve los datos principales del pasajero.
    def __str__(self):
        return self.nombre + " - DNI " + self.dni + " - " + self.condicion


class Pasaje:
    """Pasaje vendido para un asiento de un viaje."""

    # Crea un pasaje en estado Vendido con su codigo y su asiento.
    def __init__(self, codigo, pasajero, viaje_codigo, fila, columna, precio):
        self.codigo = codigo
        self.pasajero = pasajero
        self.viaje_codigo = viaje_codigo
        self.fila = fila
        self.columna = columna
        self.precio = precio
        self.estado = "Vendido"

    # Devuelve el asiento con el formato F3-C2.
    def asiento_texto(self):
        return "F" + str(self.fila) + "-C" + str(self.columna)

    # Cambia el estado del pasaje a Anulado.
    def marcar_anulado(self):
        self.estado = "Anulado"

    # Vuelve a marcar el pasaje como Vendido cuando se deshace una anulacion.
    def marcar_vendido(self):
        self.estado = "Vendido"

    # Devuelve los datos principales del pasaje en una linea.
    def __str__(self):
        return (
            self.codigo
            + " | DNI "
            + self.pasajero.dni
            + " | "
            + self.pasajero.nombre
            + " | Asiento "
            + self.asiento_texto()
            + " | S/ "
            + format(self.precio, ".2f")
            + " | "
            + self.estado
        )
