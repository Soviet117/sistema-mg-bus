"""Vistas de consola: menus, tablas y mensajes del sistema.

Esta capa solo se encarga de mostrar informacion y de dar formato a la
salida. La logica de ventas, anulaciones y rutas esta en sistema.py.
"""


# Muestra el encabezado de la empresa al iniciar el programa.
def mostrar_banner():
    print("=" * 64)
    print("   MG BUS - EMPRESA DE TRANSPORTE INTERPROVINCIAL")
    print("   Sistema de venta de pasajes y rutas - Nueva Cajamarca")
    print("=" * 64)


# Muestra el menu principal con todas las opciones del sistema.
def mostrar_menu():
    print("\n" + "=" * 64)
    print("   MENU PRINCIPAL")
    print("=" * 64)
    print("   1. Ver viajes disponibles")
    print("   2. Ver mapa de asientos de un viaje        [Matriz]")
    print("   3. Vender pasaje")
    print("   4. Anular pasaje")
    print("   5. Deshacer ultima anulacion               [Pila]")
    print("   6. Lista de pasajeros por viaje            [Lista enlazada]")
    print("   7. Consultar ruta entre dos ciudades       [Grafo + Warshall]")
    print("   8. Ver matrices del grafo                  [Adyacencia]")
    print("   9. Lista de espera de un viaje lleno       [Cola]")
    print("  10. Buscar pasajero por DNI                 [Busqueda secuencial]")
    print("  11. Buscar ciudad                           [Busqueda binaria]")
    print("  12. Reporte general")
    print("   0. Salir")
    print("=" * 64)


# Imprime un titulo rodeado de lineas para separar las secciones.
def titulo(texto):
    print("\n" + "-" * 64)
    print("  " + texto)
    print("-" * 64)


# Imprime un subtitulo sencillo.
def subtitulo(texto):
    print("\n" + texto)


# Muestra un mensaje de error con una marca facil de identificar.
def mostrar_error(mensaje):
    print("\n[ERROR] " + mensaje)


# Muestra un mensaje de operacion realizada correctamente.
def mostrar_exito(mensaje):
    print("\n[OK] " + mensaje)


# Muestra un aviso importante para el usuario.
def mostrar_aviso(mensaje):
    print("\n[AVISO] " + mensaje)


# Muestra la tabla de viajes con ruta, fecha, precio y asientos libres.
def listar_viajes(viajes):
    if len(viajes) == 0:
        print("  No hay viajes registrados.")
        return
    print("\n  " + "Codigo".ljust(8) + "Ruta".ljust(32) + "Fecha".ljust(12) + "Hora".ljust(7) + "Precio".rjust(9) + "Libres".rjust(8) + "Total".rjust(7) + "  Bus")
    print("  " + "-" * 91)
    for posicion in range(len(viajes)):
        viaje = viajes[posicion]
        libres = viaje.asientos_libres()
        if viaje.esta_lleno():
            texto_libres = "LLENO"
        else:
            texto_libres = str(libres)
        print(
            "  "
            + viaje.codigo.ljust(8)
            + viaje.descripcion_ruta().ljust(32)
            + viaje.fecha.ljust(12)
            + viaje.hora.ljust(7)
            + ("S/ " + format(viaje.precio, ".2f")).rjust(9)
            + texto_libres.rjust(8)
            + str(viaje.total_asientos()).rjust(7)
            + "  "
            + viaje.bus.placa
        )
    print("  " + "-" * 91)


# Muestra el mapa de asientos del bus de un viaje.
def mostrar_mapa_asientos(viaje):
    titulo("MAPA DE ASIENTOS - " + viaje.codigo)
    print("  Ruta   : " + viaje.descripcion_ruta())
    print("  Fecha  : " + viaje.fecha + "   Hora: " + viaje.hora)
    print("  Bus    : " + str(viaje.bus))
    print("  Precio : S/ " + format(viaje.precio, ".2f"))
    print("\n  Leyenda: [ ] = libre     [X] = ocupado\n")

    encabezado = "        "
    for columna in range(1, viaje.matriz_asientos.columnas + 1):
        encabezado = encabezado + ("C" + str(columna)).ljust(4)
    print(encabezado)

    for fila in range(1, viaje.matriz_asientos.filas + 1):
        linea = "  F" + str(fila).rjust(2) + "   "
        for columna in range(1, viaje.matriz_asientos.columnas + 1):
            if viaje.matriz_asientos.esta_libre(fila, columna):
                linea = linea + "[ ] "
            else:
                linea = linea + "[X] "
        print(linea)

    print("\n  Asientos libres  : " + str(viaje.asientos_libres()))
    print("  Asientos ocupados: " + str(viaje.matriz_asientos.contar_ocupados()))
    print("  Total de asientos: " + str(viaje.total_asientos()))


# Muestra la lista enlazada de pasajeros de un viaje.
def mostrar_pasajeros(viaje):
    titulo("LISTA DE PASAJEROS - " + viaje.codigo)
    print("  Ruta: " + viaje.descripcion_ruta() + "   Fecha: " + viaje.fecha + " " + viaje.hora)
    pasajes = viaje.pasajeros.recorrer()
    if len(pasajes) == 0:
        print("\n  El viaje todavia no tiene pasajeros.")
        return
    print("\n  " + "Codigo".ljust(8) + "DNI".ljust(10) + "Pasajero".ljust(28) + "Asiento".ljust(10) + "Condicion".ljust(16) + "Precio".rjust(9))
    print("  " + "-" * 81)
    recaudado = 0.0
    for posicion in range(len(pasajes)):
        pasaje = pasajes[posicion]
        recaudado = recaudado + pasaje.precio
        print(
            "  "
            + pasaje.codigo.ljust(8)
            + pasaje.pasajero.dni.ljust(10)
            + pasaje.pasajero.nombre.ljust(28)
            + pasaje.asiento_texto().ljust(10)
            + pasaje.pasajero.condicion.ljust(16)
            + ("S/ " + format(pasaje.precio, ".2f")).rjust(9)
        )
    print("  " + "-" * 81)
    print("  Pasajeros: " + str(len(pasajes)) + "     Recaudado: S/ " + format(recaudado, ".2f"))
    print("  Esta lista se recorre desde la cabeza hasta el ultimo nodo.")


# Muestra la tabla de ciudades registradas en el grafo.
def mostrar_ciudades(ciudades):
    print("\n  " + "Nro".ljust(5) + "Codigo".ljust(8) + "Ciudad".ljust(22) + "Departamento")
    print("  " + "-" * 55)
    for posicion in range(len(ciudades)):
        ciudad = ciudades[posicion]
        print("  " + str(posicion + 1).ljust(5) + ciudad.codigo.ljust(8) + ciudad.nombre.ljust(22) + ciudad.departamento)


# Imprime una matriz del grafo con los codigos de las ciudades.
def _imprimir_matriz(grafo, matriz):
    encabezado = "        "
    for posicion in range(len(grafo.ciudades)):
        encabezado = encabezado + grafo.ciudades[posicion].codigo.rjust(5)
    print(encabezado)
    for fila in range(len(grafo.ciudades)):
        linea = "  " + grafo.ciudades[fila].codigo.ljust(5) + " "
        for columna in range(len(grafo.ciudades)):
            linea = linea + str(matriz[fila][columna]).rjust(5)
        print(linea)
    print("\n  Leyenda:")
    for posicion in range(len(grafo.ciudades)):
        print("   " + grafo.ciudades[posicion].codigo + " = " + grafo.ciudades[posicion].nombre)


# Muestra la matriz de adyacencia (rutas directas).
def mostrar_matriz_adyacencia(grafo):
    titulo("MATRIZ DE ADYACENCIA - RUTAS DIRECTAS")
    print("  1 = hay ruta directa    0 = no hay ruta directa")
    _imprimir_matriz(grafo, grafo.matriz_adyacencia)
    print("\n  Total de rutas directas: " + str(grafo.total_rutas_directas()))


# Muestra la matriz de alcanzabilidad calculada con Warshall.
def mostrar_matriz_alcanzabilidad(grafo):
    titulo("MATRIZ DE ALCANZABILIDAD - WARSHALL")
    print("  1 = se puede llegar (con o sin escalas)    0 = no se puede llegar")
    matriz = grafo.obtener_alcanzabilidad()
    _imprimir_matriz(grafo, matriz)
    print("\n  La diagonal vale 1 porque una ciudad siempre se alcanza a si misma.")


# Muestra el resultado de consultar una ruta entre dos ciudades.
def mostrar_resultado_ruta(resultado, alcanzables):
    titulo("CONSULTA DE RUTA")
    print("  Origen : " + resultado["origen"])
    print("  Destino: " + resultado["destino"])
    print("")
    if resultado["misma_ciudad"]:
        print("  Es la misma ciudad: no se necesita una ruta.")
    elif not resultado["existe"]:
        print("  NO existe ruta entre esas dos ciudades en el grafo.")
    elif resultado["directa"]:
        print("  SI existe ruta DIRECTA entre esas dos ciudades.")
    else:
        print("  SI existe ruta, pero se debe hacer al menos una escala.")
    if len(alcanzables) > 0:
        print("\n  Ciudades alcanzables desde " + resultado["origen"] + ":")
        print("  " + ", ".join(alcanzables))
    else:
        print("\n  Desde " + resultado["origen"] + " no se alcanza ninguna otra ciudad.")
    print("\n  Resultado calculado con la matriz de alcanzabilidad de Warshall.")


# Muestra los datos de una ciudad y sus rutas directas.
def mostrar_ciudad(ciudad, destinos):
    titulo("CIUDAD ENCONTRADA")
    print("  Nombre      : " + ciudad.nombre)
    print("  Codigo      : " + ciudad.codigo)
    print("  Departamento: " + ciudad.departamento)
    if len(destinos) == 0:
        print("  Rutas directas: ninguna")
    else:
        print("  Rutas directas: " + ", ".join(destinos))


# Muestra la cola de espera de un viaje.
def mostrar_cola(viaje):
    titulo("LISTA DE ESPERA - " + viaje.codigo)
    print("  Ruta: " + viaje.descripcion_ruta() + "   Asientos libres: " + str(viaje.asientos_libres()))
    viaje.espera.mostrar()
    print("\n  Personas en espera: " + str(viaje.espera.contar()))
    print("  La cola atiende primero al pasajero que llego primero (FIFO).")


# Muestra la pila de anulaciones pendientes de deshacer.
def mostrar_pila(pila):
    titulo("PILA DE ANULACIONES")
    pila.mostrar()
    print("\n  Anulaciones pendientes: " + str(pila.contar()))
    print("  La ultima anulacion queda en el tope de la pila (LIFO).")


# Muestra un pasaje en formato de boleto.
def mostrar_ticket(pasaje, viaje, texto_titulo="PASAJE VENDIDO"):
    print("\n" + "=" * 64)
    print("  " + texto_titulo)
    print("=" * 64)
    print("  Codigo    : " + pasaje.codigo)
    print("  Pasajero  : " + pasaje.pasajero.nombre)
    print("  DNI       : " + pasaje.pasajero.dni)
    print("  Condicion : " + pasaje.pasajero.condicion)
    print("  Viaje     : " + viaje.codigo + "  (" + viaje.descripcion_ruta() + ")")
    print("  Fecha     : " + viaje.fecha + "   Hora: " + viaje.hora)
    print("  Asiento   : " + pasaje.asiento_texto())
    print("  Precio    : S/ " + format(pasaje.precio, ".2f"))
    print("  Estado    : " + pasaje.estado)
    print("=" * 64)


# Muestra todos los pasajes encontrados para un DNI.
def mostrar_resultados_busqueda(pasajes, dni):
    titulo("RESULTADOS DE LA BUSQUEDA")
    print("  DNI buscado: " + dni)
    if len(pasajes) == 0:
        print("\n  No se encontro ningun pasaje activo con ese DNI.")
        return
    print("\n  " + "Codigo".ljust(8) + "Viaje".ljust(9) + "Asiento".ljust(10) + "Pasajero".ljust(28) + "Precio".rjust(9))
    print("  " + "-" * 68)
    for posicion in range(len(pasajes)):
        pasaje = pasajes[posicion]
        print(
            "  "
            + pasaje.codigo.ljust(8)
            + pasaje.viaje_codigo.ljust(9)
            + pasaje.asiento_texto().ljust(10)
            + pasaje.pasajero.nombre.ljust(28)
            + ("S/ " + format(pasaje.precio, ".2f")).rjust(9)
        )
    print("\n  Busqueda secuencial sobre las listas enlazadas de cada viaje.")


# Muestra el reporte general con los totales del sistema.
def mostrar_reporte(reporte):
    titulo("REPORTE GENERAL DEL SISTEMA")
    print("  Ciudades registradas   : " + str(reporte["ciudades"]))
    print("  Rutas directas         : " + str(reporte["rutas_directas"]))
    print("  Viajes programados     : " + str(reporte["viajes"]))
    print("  Asientos totales       : " + str(reporte["asientos_totales"]))
    print("  Asientos ocupados      : " + str(reporte["asientos_ocupados"]))
    print("  Asientos libres        : " + str(reporte["asientos_libres"]))
    print("  Pasajes activos        : " + str(reporte["pasajes_activos"]))
    print("  Recaudado              : S/ " + format(reporte["recaudado"], ".2f"))
    print("  Pasajeros en espera    : " + str(reporte["en_espera"]))
    print("  Anulaciones pendientes : " + str(reporte["anulaciones_pendientes"]))
    print("  Anulaciones historicas : " + str(reporte["anulaciones_totales"]))
    print("  Ocupacion de asientos  : " + format(reporte["porcentaje_ocupacion"], ".1f") + " %")
