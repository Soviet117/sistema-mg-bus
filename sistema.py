"""Logica principal del sistema de venta de pasajes.

Esta clase hace de controlador y de DAO en memoria: guarda las ciudades,
los viajes y las anulaciones, y ofrece las operaciones que usa el menu.
No imprime nada; las respuestas se muestran desde las vistas.
"""

from estructuras.busquedas import busqueda_binaria, busqueda_secuencial
from estructuras.grafo_rutas import GrafoRutas
from estructuras.pila import Pila
from modelos import Pasajero, Pasaje
from validaciones import (
    es_condicion_valida,
    es_dni_valido,
    es_nombre_valido,
    es_telefono_valido,
    normalizar_codigo,
    normalizar_nombre,
)


class SistemaTransporte:
    """Sistema en memoria para vender, anular y consultar pasajes."""

    # Crea el sistema vacio con su grafo y su pila de anulaciones.
    def __init__(self):
        self.ciudades = []
        self.viajes = []
        self.grafo = GrafoRutas()
        self.anulaciones = Pila()
        self.contador_pasajes = 0
        self.total_anulaciones = 0

    # Agrega una ciudad al arreglo del sistema y al grafo de rutas.
    def agregar_ciudad(self, ciudad):
        self.grafo.agregar_ciudad(ciudad)
        self.ciudades.append(ciudad)

    # Agrega una ruta directa entre dos ciudades al grafo.
    def agregar_ruta(self, origen, destino):
        self.grafo.agregar_ruta(origen, destino)

    # Agrega un viaje programado al arreglo de viajes.
    def agregar_viaje(self, viaje):
        if self.buscar_viaje(viaje.codigo) is not None:
            raise ValueError("Ya existe un viaje con el codigo " + viaje.codigo + ".")
        self.viajes.append(viaje)

    # Busca un viaje por su codigo con busqueda secuencial.
    def buscar_viaje(self, codigo):
        codigo = normalizar_codigo(codigo)
        codigos = [None] * len(self.viajes)
        for posicion in range(len(self.viajes)):
            codigos[posicion] = self.viajes[posicion].codigo
        posicion = busqueda_secuencial(codigos, codigo)
        if posicion == -1:
            return None
        return self.viajes[posicion]

    # Busca una ciudad por su nombre con busqueda binaria.
    def buscar_ciudad_binaria(self, nombre):
        nombre = normalizar_nombre(nombre)
        if nombre == "":
            return None
        nombres = [None] * len(self.grafo.ciudades)
        for posicion in range(len(self.grafo.ciudades)):
            nombres[posicion] = self.grafo.ciudades[posicion].nombre
        nombres.sort()
        posicion = busqueda_binaria(nombres, nombre)
        if posicion == -1:
            return None
        indice = self.grafo.indice_ciudad(nombre)
        if indice == -1:
            return None
        return self.grafo.ciudades[indice]

    # Crea un pasajero despues de validar todos sus datos.
    def _crear_pasajero(self, dni, nombre, edad, telefono, condicion):
        dni = dni.strip()
        nombre = normalizar_nombre(nombre)
        if not es_dni_valido(dni):
            raise ValueError("El DNI debe tener exactamente 8 digitos.")
        if not es_nombre_valido(nombre):
            raise ValueError("El nombre debe tener al menos 3 letras y no llevar numeros.")
        try:
            edad = int(edad)
        except (TypeError, ValueError):
            raise ValueError("La edad debe ser un numero entero.")
        if edad < 0 or edad > 120:
            raise ValueError("La edad debe estar entre 0 y 120 anios.")
        if telefono is None:
            telefono = "No registrado"
        telefono = telefono.strip()
        if telefono == "":
            telefono = "No registrado"
        if telefono != "No registrado" and not es_telefono_valido(telefono):
            raise ValueError("El telefono debe tener entre 6 y 15 digitos.")
        condicion = condicion.strip()
        if not es_condicion_valida(condicion):
            raise ValueError("La condicion del pasajero no es valida.")
        return Pasajero(dni, nombre, edad, telefono, condicion)

    # Vende un pasaje para un viaje y un asiento; si fila y columna son 0,
    # el sistema asigna automaticamente el primer asiento libre.
    def vender_pasaje(self, codigo_viaje, dni, nombre, edad, telefono, condicion, fila=0, columna=0):
        viaje = self.buscar_viaje(codigo_viaje)
        if viaje is None:
            raise ValueError("No existe un viaje con ese codigo.")
        pasajero = self._crear_pasajero(dni, nombre, edad, telefono, condicion)
        if viaje.esta_lleno():
            raise ValueError("El viaje esta lleno. Puede anotar al pasajero en la lista de espera.")
        if viaje.buscar_pasajero_por_dni(pasajero.dni) is not None:
            raise ValueError("Ese pasajero ya tiene un pasaje en este viaje.")

        if fila == 0 and columna == 0:
            asiento = viaje.matriz_asientos.primer_asiento_libre()
            if asiento is None:
                raise ValueError("No hay asientos libres en este viaje.")
            fila = asiento[0]
            columna = asiento[1]
        else:
            if not viaje.matriz_asientos.dentro_de_rango(fila, columna):
                raise ValueError("El asiento indicado no existe en este bus.")
            if not viaje.matriz_asientos.esta_libre(fila, columna):
                raise ValueError("El asiento " + viaje.matriz_asientos.etiqueta_asiento(fila, columna) + " ya esta ocupado.")

        self.contador_pasajes = self.contador_pasajes + 1
        codigo_pasaje = "P" + str(self.contador_pasajes).zfill(3)
        pasaje = Pasaje(codigo_pasaje, pasajero, viaje.codigo, fila, columna, viaje.precio)
        viaje.matriz_asientos.ocupar(fila, columna)
        viaje.agregar_pasajero(pasaje)
        return pasaje

    # Anula el pasaje de un DNI y guarda la anulacion en la pila.
    def anular_pasaje(self, codigo_viaje, dni):
        viaje = self.buscar_viaje(codigo_viaje)
        if viaje is None:
            raise ValueError("No existe un viaje con ese codigo.")
        dni = dni.strip()
        pasaje = viaje.buscar_pasajero_por_dni(dni)
        if pasaje is None:
            raise ValueError("No se encontro un pasaje con ese DNI en el viaje.")
        viaje.quitar_pasajero(dni)
        viaje.matriz_asientos.liberar(pasaje.fila, pasaje.columna)
        pasaje.marcar_anulado()
        self.anulaciones.apilar(pasaje)
        self.total_anulaciones = self.total_anulaciones + 1
        return pasaje

    # Deshace la ultima anulacion guardada en la pila.
    def deshacer_anulacion(self):
        if self.anulaciones.esta_vacia():
            raise ValueError("No hay anulaciones pendientes de deshacer.")
        pasaje = self.anulaciones.cima()
        viaje = self.buscar_viaje(pasaje.viaje_codigo)
        if viaje is None:
            raise ValueError("El viaje de esa anulacion ya no existe.")
        if not viaje.matriz_asientos.esta_libre(pasaje.fila, pasaje.columna):
            raise ValueError("No se puede deshacer: el asiento ya fue ocupado por otra venta.")
        if viaje.buscar_pasajero_por_dni(pasaje.pasajero.dni) is not None:
            raise ValueError("No se puede deshacer: el pasajero ya tiene otro pasaje en este viaje.")
        viaje.matriz_asientos.ocupar(pasaje.fila, pasaje.columna)
        pasaje.marcar_vendido()
        viaje.agregar_pasajero(pasaje)
        self.anulaciones.desapilar()
        return pasaje

    # Devuelve el arreglo de pasajes activos de un viaje.
    def pasajeros_de_viaje(self, codigo_viaje):
        viaje = self.buscar_viaje(codigo_viaje)
        if viaje is None:
            raise ValueError("No existe un viaje con ese codigo.")
        return viaje.pasajeros.recorrer()

    # Anota un pasajero en la cola de espera de un viaje lleno.
    def anotar_en_espera(self, codigo_viaje, dni, nombre, edad, telefono, condicion):
        viaje = self.buscar_viaje(codigo_viaje)
        if viaje is None:
            raise ValueError("No existe un viaje con ese codigo.")
        if not viaje.esta_lleno():
            raise ValueError("Todavia hay asientos libres; puede vender un pasaje normal.")
        pasajero = self._crear_pasajero(dni, nombre, edad, telefono, condicion)
        if viaje.buscar_pasajero_por_dni(pasajero.dni) is not None:
            raise ValueError("Ese pasajero ya tiene un pasaje en este viaje.")
        en_espera = viaje.espera.recorrer()
        for posicion in range(len(en_espera)):
            if en_espera[posicion].dni == pasajero.dni:
                raise ValueError("Ese pasajero ya esta en la lista de espera.")
        viaje.espera.encolar(pasajero)
        return pasajero

    # Atiende al primero de la cola de espera y le vende un asiento libre.
    def atender_siguiente_espera(self, codigo_viaje):
        viaje = self.buscar_viaje(codigo_viaje)
        if viaje is None:
            raise ValueError("No existe un viaje con ese codigo.")
        if viaje.espera.esta_vacia():
            raise ValueError("La lista de espera de ese viaje esta vacia.")
        if viaje.esta_lleno():
            raise ValueError("Todavia no hay asientos libres en ese viaje.")
        pasajero = viaje.espera.frente()
        pasaje = self.vender_pasaje(
            codigo_viaje,
            pasajero.dni,
            pasajero.nombre,
            pasajero.edad,
            pasajero.telefono,
            pasajero.condicion,
        )
        viaje.espera.desencolar()
        return pasaje

    # Consulta si existe ruta entre dos ciudades usando el grafo y Warshall.
    # Devuelve un diccionario con las ciudades, si existe ruta y si es directa.
    def consultar_ruta(self, origen, destino):
        ciudad_origen = self.buscar_ciudad_binaria(origen)
        if ciudad_origen is None:
            raise ValueError("No existe la ciudad de origen: " + origen + ".")
        ciudad_destino = self.buscar_ciudad_binaria(destino)
        if ciudad_destino is None:
            raise ValueError("No existe la ciudad de destino: " + destino + ".")
        existe = self.grafo.existe_ruta(ciudad_origen.nombre, ciudad_destino.nombre)
        directa = self.grafo.es_ruta_directa(ciudad_origen.nombre, ciudad_destino.nombre)
        misma_ciudad = ciudad_origen.nombre == ciudad_destino.nombre
        return {
            "origen": ciudad_origen.nombre,
            "destino": ciudad_destino.nombre,
            "existe": existe,
            "directa": directa,
            "misma_ciudad": misma_ciudad,
        }

    # Devuelve las ciudades a las que se puede llegar desde una ciudad.
    def ciudades_alcanzables(self, origen):
        ciudad = self.buscar_ciudad_binaria(origen)
        if ciudad is None:
            raise ValueError("No existe la ciudad indicada.")
        return self.grafo.alcanzables_desde(ciudad.nombre)

    # Busca todos los pasajes de un DNI recorriendo las listas de cada viaje.
    def buscar_pasajero_por_dni(self, dni):
        dni = dni.strip()
        resultados = []
        for posicion in range(len(self.viajes)):
            pasaje = self.viajes[posicion].buscar_pasajero_por_dni(dni)
            if pasaje is not None:
                resultados.append(pasaje)
        return resultados

    # Calcula los totales que se muestran en el reporte general.
    def generar_reporte(self):
        total_asientos = 0
        asientos_ocupados = 0
        pasajes_activos = 0
        recaudado = 0.0
        en_espera = 0
        for posicion in range(len(self.viajes)):
            viaje = self.viajes[posicion]
            total_asientos = total_asientos + viaje.total_asientos()
            asientos_ocupados = asientos_ocupados + viaje.matriz_asientos.contar_ocupados()
            en_espera = en_espera + viaje.espera.contar()
            pasajes = viaje.pasajeros.recorrer()
            pasajes_activos = pasajes_activos + len(pasajes)
            for numero in range(len(pasajes)):
                recaudado = recaudado + pasajes[numero].precio
        if total_asientos == 0:
            porcentaje = 0.0
        else:
            porcentaje = (asientos_ocupados * 100.0) / total_asientos
        return {
            "ciudades": len(self.ciudades),
            "rutas_directas": self.grafo.total_rutas_directas(),
            "viajes": len(self.viajes),
            "asientos_totales": total_asientos,
            "asientos_ocupados": asientos_ocupados,
            "asientos_libres": total_asientos - asientos_ocupados,
            "pasajes_activos": pasajes_activos,
            "recaudado": recaudado,
            "en_espera": en_espera,
            "anulaciones_pendientes": self.anulaciones.contar(),
            "anulaciones_totales": self.total_anulaciones,
            "porcentaje_ocupacion": porcentaje,
        }
