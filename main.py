"""Programa principal del sistema MG Bus.

Muestra el menu, pide los datos al usuario y llama a las funciones del
sistema. La logica esta en sistema.py y las estructuras en la carpeta
estructuras/. Para ejecutar: python main.py
"""

import validaciones
import vistas
from datos_prueba import cargar_sistema


# Muestra la lista de viajes y pide un codigo; devuelve el viaje o None.
def pedir_viaje(sistema):
    if len(sistema.viajes) == 0:
        vistas.mostrar_error("No hay viajes registrados en el sistema.")
        return None
    vistas.listar_viajes(sistema.viajes)
    codigo = validaciones.pedir_texto("  Codigo del viaje (0 para cancelar): ", 10)
    if codigo == "0":
        vistas.mostrar_aviso("Operacion cancelada.")
        return None
    viaje = sistema.buscar_viaje(codigo)
    if viaje is None:
        vistas.mostrar_error("No existe un viaje con el codigo " + codigo + ".")
    return viaje


# Pide todos los datos personales de un pasajero y los devuelve en una tupla.
def leer_datos_pasajero():
    dni = validaciones.pedir_dni()
    nombre = validaciones.pedir_nombre()
    edad = validaciones.pedir_entero("Edad: ", 0, 120)
    telefono = validaciones.pedir_telefono()
    condicion = validaciones.pedir_condicion()
    return (dni, nombre, edad, telefono, condicion)


# Pide la fila y la columna de un asiento libre; (0, 0) significa automatico.
def elegir_asiento(viaje):
    while True:
        fila = validaciones.pedir_entero("  Fila del asiento (0 = automatico): ", 0, viaje.matriz_asientos.filas)
        if fila == 0:
            return (0, 0)
        columna = validaciones.pedir_entero("  Columna del asiento: ", 1, viaje.matriz_asientos.columnas)
        if viaje.matriz_asientos.esta_libre(fila, columna):
            return (fila, columna)
        vistas.mostrar_error("Ese asiento ya esta ocupado. Elija otro.")


# Opcion 1: muestra todos los viajes con sus asientos disponibles.
def accion_ver_viajes(sistema):
    vistas.titulo("VIAJES DISPONIBLES")
    vistas.listar_viajes(sistema.viajes)
    print("\n  Total de viajes: " + str(len(sistema.viajes)))


# Opcion 2: muestra el mapa de asientos del viaje elegido.
def accion_mapa_asientos(sistema):
    vistas.titulo("MAPA DE ASIENTOS")
    viaje = pedir_viaje(sistema)
    if viaje is None:
        return
    vistas.mostrar_mapa_asientos(viaje)


# Opcion 3: vende un pasaje en el viaje y asiento elegidos.
def accion_vender_pasaje(sistema):
    vistas.titulo("VENTA DE PASAJE")
    viaje = pedir_viaje(sistema)
    if viaje is None:
        return
    vistas.mostrar_mapa_asientos(viaje)
    if viaje.esta_lleno():
        vistas.mostrar_aviso("El viaje esta lleno. Use la opcion 9 para la lista de espera.")
        return
    datos = leer_datos_pasajero()
    asiento = elegir_asiento(viaje)
    try:
        pasaje = sistema.vender_pasaje(
            viaje.codigo,
            datos[0],
            datos[1],
            datos[2],
            datos[3],
            datos[4],
            asiento[0],
            asiento[1],
        )
    except ValueError as error:
        vistas.mostrar_error(str(error))
        return
    vistas.mostrar_exito("Pasaje vendido correctamente.")
    vistas.mostrar_ticket(pasaje, viaje)
    print("  Asientos libres que quedan: " + str(viaje.asientos_libres()))


# Opcion 4: anula el pasaje de un pasajero del viaje elegido.
def accion_anular_pasaje(sistema):
    vistas.titulo("ANULACION DE PASAJE")
    viaje = pedir_viaje(sistema)
    if viaje is None:
        return
    vistas.mostrar_pasajeros(viaje)
    if viaje.cantidad_pasajeros() == 0:
        return
    dni = validaciones.pedir_dni()
    pasaje = viaje.buscar_pasajero_por_dni(dni)
    if pasaje is None:
        vistas.mostrar_error("No se encontro un pasaje con ese DNI en este viaje.")
        return
    print("\n  Se anulara el pasaje " + pasaje.codigo + " del asiento " + pasaje.asiento_texto() + ".")
    if not validaciones.pedir_confirmacion("  Confirma la anulacion?"):
        vistas.mostrar_aviso("Anulacion cancelada.")
        return
    try:
        anulado = sistema.anular_pasaje(viaje.codigo, dni)
    except ValueError as error:
        vistas.mostrar_error(str(error))
        return
    vistas.mostrar_exito("Pasaje anulado. La anulacion quedo en el tope de la pila.")
    vistas.mostrar_ticket(anulado, viaje, "PASAJE ANULADO")
    print("  Puede deshacer esta anulacion en la opcion 5.")


# Opcion 5: deshace la ultima anulacion guardada en la pila.
def accion_deshacer_anulacion(sistema):
    vistas.titulo("DESHACER ULTIMA ANULACION")
    if sistema.anulaciones.esta_vacia():
        vistas.mostrar_aviso("No hay anulaciones pendientes de deshacer.")
        return
    vistas.mostrar_pila(sistema.anulaciones)
    if not validaciones.pedir_confirmacion("  Desea deshacer la anulacion del tope?"):
        vistas.mostrar_aviso("Operacion cancelada.")
        return
    try:
        pasaje = sistema.deshacer_anulacion()
    except ValueError as error:
        vistas.mostrar_error(str(error))
        return
    viaje = sistema.buscar_viaje(pasaje.viaje_codigo)
    vistas.mostrar_exito("Anulacion deshecha. El pasaje vuelve a estar vendido.")
    vistas.mostrar_ticket(pasaje, viaje, "PASAJE RESTAURADO")
    print("  Anulaciones pendientes en la pila: " + str(sistema.anulaciones.contar()))


# Opcion 6: muestra la lista enlazada de pasajeros de un viaje.
def accion_lista_pasajeros(sistema):
    vistas.titulo("LISTA DE PASAJEROS POR VIAJE")
    viaje = pedir_viaje(sistema)
    if viaje is None:
        return
    vistas.mostrar_pasajeros(viaje)


# Opcion 7: consulta si existe ruta entre dos ciudades con Warshall.
def accion_consultar_ruta(sistema):
    vistas.titulo("CONSULTA DE RUTA ENTRE DOS CIUDADES")
    vistas.mostrar_ciudades(sistema.ciudades)
    origen = validaciones.pedir_texto("\n  Ciudad de origen: ", 40)
    destino = validaciones.pedir_texto("  Ciudad de destino: ", 40)
    try:
        resultado = sistema.consultar_ruta(origen, destino)
        alcanzables = sistema.ciudades_alcanzables(resultado["origen"])
    except ValueError as error:
        vistas.mostrar_error(str(error))
        return
    vistas.mostrar_resultado_ruta(resultado, alcanzables)


# Opcion 8: muestra la matriz de adyacencia, la de Warshall o ambas.
def accion_ver_matrices(sistema):
    vistas.titulo("MATRICES DEL GRAFO DE CIUDADES")
    print("  1. Matriz de adyacencia (rutas directas)")
    print("  2. Matriz de alcanzabilidad (Warshall)")
    print("  3. Mostrar ambas")
    opcion = validaciones.pedir_entero("  Elija una opcion: ", 1, 3)
    if opcion == 1 or opcion == 3:
        vistas.mostrar_matriz_adyacencia(sistema.grafo)
    if opcion == 2 or opcion == 3:
        vistas.mostrar_matriz_alcanzabilidad(sistema.grafo)


# Opcion 9: permite anotar, atender o ver la cola de espera de un viaje.
def accion_lista_espera(sistema):
    vistas.titulo("LISTA DE ESPERA DE UN VIAJE")
    print("  1. Anotar un pasajero en la lista de espera")
    print("  2. Atender al siguiente pasajero de la cola")
    print("  3. Ver la lista de espera")
    opcion = validaciones.pedir_entero("  Elija una opcion: ", 1, 3)
    viaje = pedir_viaje(sistema)
    if viaje is None:
        return

    if opcion == 1:
        if not viaje.esta_lleno():
            vistas.mostrar_aviso("Ese viaje aun tiene " + str(viaje.asientos_libres()) + " asientos libres. Venda un pasaje normal.")
            return
        datos = leer_datos_pasajero()
        try:
            sistema.anotar_en_espera(viaje.codigo, datos[0], datos[1], datos[2], datos[3], datos[4])
        except ValueError as error:
            vistas.mostrar_error(str(error))
            return
        vistas.mostrar_exito("Pasajero anotado al final de la cola de espera.")
        vistas.mostrar_cola(viaje)

    elif opcion == 2:
        vistas.mostrar_cola(viaje)
        if viaje.espera.esta_vacia():
            return
        if viaje.esta_lleno():
            vistas.mostrar_aviso("Todavia no hay asientos libres. Anule un pasaje para liberar uno.")
            return
        if not validaciones.pedir_confirmacion("  Vender el asiento libre al primero de la cola?"):
            vistas.mostrar_aviso("Operacion cancelada.")
            return
        try:
            pasaje = sistema.atender_siguiente_espera(viaje.codigo)
        except ValueError as error:
            vistas.mostrar_error(str(error))
            return
        vistas.mostrar_exito("Se atendio al primero de la cola y se vendio su pasaje.")
        vistas.mostrar_ticket(pasaje, viaje)
        vistas.mostrar_cola(viaje)

    else:
        vistas.mostrar_cola(viaje)


# Opcion 10: busca pasajes activos por DNI con busqueda secuencial.
def accion_buscar_pasajero(sistema):
    vistas.titulo("BUSCAR PASAJERO POR DNI")
    dni = validaciones.pedir_dni()
    resultados = sistema.buscar_pasajero_por_dni(dni)
    vistas.mostrar_resultados_busqueda(resultados, dni)


# Opcion 11: busca una ciudad por nombre con busqueda binaria.
def accion_buscar_ciudad(sistema):
    vistas.titulo("BUSCAR CIUDAD - BUSQUEDA BINARIA")
    vistas.mostrar_ciudades(sistema.ciudades)
    nombre = validaciones.pedir_texto("\n  Nombre de la ciudad: ", 40)
    ciudad = sistema.buscar_ciudad_binaria(nombre)
    if ciudad is None:
        vistas.mostrar_error("No se encontro la ciudad " + nombre + ". Revise la lista.")
        return
    destinos = sistema.grafo.destinos_directos(ciudad.nombre)
    vistas.mostrar_ciudad(ciudad, destinos)
    print("\n  La busqueda binaria trabaja sobre las ciudades ordenadas por nombre.")


# Opcion 12: muestra el reporte general del sistema.
def accion_reporte(sistema):
    vistas.mostrar_reporte(sistema.generar_reporte())


# Funcion principal: carga los datos y repite el menu hasta que el usuario salga.
def main():
    sistema = cargar_sistema()
    vistas.mostrar_banner()
    reporte = sistema.generar_reporte()
    print("  Datos de prueba cargados: " + str(reporte["ciudades"]) + " ciudades, " + str(reporte["viajes"]) + " viajes,")
    print("  " + str(reporte["pasajes_activos"]) + " pasajes activos y " + str(reporte["en_espera"]) + " pasajeros en espera.")
    print("  Use la opcion 12 para ver el reporte completo.")

    while True:
        vistas.mostrar_menu()
        opcion = validaciones.pedir_entero("  Seleccione una opcion: ", 0, 12)

        if opcion == 0:
            print("\n  Gracias por usar el sistema de MG Bus. Hasta pronto.")
            break
        elif opcion == 1:
            accion_ver_viajes(sistema)
        elif opcion == 2:
            accion_mapa_asientos(sistema)
        elif opcion == 3:
            accion_vender_pasaje(sistema)
        elif opcion == 4:
            accion_anular_pasaje(sistema)
        elif opcion == 5:
            accion_deshacer_anulacion(sistema)
        elif opcion == 6:
            accion_lista_pasajeros(sistema)
        elif opcion == 7:
            accion_consultar_ruta(sistema)
        elif opcion == 8:
            accion_ver_matrices(sistema)
        elif opcion == 9:
            accion_lista_espera(sistema)
        elif opcion == 10:
            accion_buscar_pasajero(sistema)
        elif opcion == 11:
            accion_buscar_ciudad(sistema)
        elif opcion == 12:
            accion_reporte(sistema)

        validaciones.pausa()


# Punto de entrada del programa.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario. Hasta pronto.")
    except EOFError:
        print("\n\n  Entrada finalizada. Hasta pronto.")
