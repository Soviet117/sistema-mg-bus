"""Validaciones y funciones para pedir datos por teclado.

Las validaciones puras (DNI, nombre, telefono y condicion) tambien se
usan en el sistema, no solo en el menu. Asi los datos de prueba y los
datos escritos por el usuario pasan por las mismas reglas.
"""

from modelos import CONDICIONES


# Quita espacios sobrantes y escribe el nombre con mayuscula inicial.
def normalizar_nombre(texto):
    texto = texto.strip()
    if texto == "":
        return ""
    return " ".join(texto.split()).title()


# Quita espacios y convierte un codigo a mayusculas (por ejemplo v001).
def normalizar_codigo(texto):
    return texto.strip().upper()


# Verifica que el DNI tenga exactamente 8 digitos.
def es_dni_valido(dni):
    if len(dni) != 8:
        return False
    return dni.isdigit()


# Verifica que el nombre tenga al menos 3 letras y no contenga numeros.
def es_nombre_valido(nombre):
    if len(nombre) < 3:
        return False
    sin_espacios = nombre.replace(" ", "")
    if sin_espacios == "":
        return False
    return sin_espacios.isalpha()


# Verifica que el telefono tenga entre 6 y 15 digitos.
def es_telefono_valido(telefono):
    if len(telefono) < 6 or len(telefono) > 15:
        return False
    return telefono.isdigit()


# Verifica que la condicion sea una de las permitidas.
def es_condicion_valida(condicion):
    for permitida in CONDICIONES:
        if condicion == permitida:
            return True
    return False


# Pide un numero entero y lo valida dentro de un rango opcional.
def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("  Error: debe escribir un numero entero.")
            continue
        if minimo is not None and numero < minimo:
            print("  Error: el numero debe ser mayor o igual a " + str(minimo) + ".")
            continue
        if maximo is not None and numero > maximo:
            print("  Error: el numero debe ser menor o igual a " + str(maximo) + ".")
            continue
        return numero


# Pide un texto no vacio y con un largo maximo.
def pedir_texto(mensaje, largo_maximo=80):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("  Error: el texto no puede quedar vacio.")
            continue
        if len(texto) > largo_maximo:
            print("  Error: el texto es demasiado largo.")
            continue
        return texto


# Pide un DNI y repite hasta que tenga 8 digitos.
def pedir_dni():
    while True:
        dni = input("DNI (8 digitos): ").strip()
        if es_dni_valido(dni):
            return dni
        print("  Error: el DNI debe tener exactamente 8 digitos.")


# Pide un nombre y repite hasta que sea valido.
def pedir_nombre():
    while True:
        nombre = normalizar_nombre(input("Nombre completo: "))
        if es_nombre_valido(nombre):
            return nombre
        print("  Error: escriba un nombre de al menos 3 letras, sin numeros.")


# Pide un telefono; si se deja vacio se guarda como No registrado.
def pedir_telefono():
    while True:
        telefono = input("Telefono (Enter para omitir): ").strip()
        if telefono == "":
            return "No registrado"
        if es_telefono_valido(telefono):
            return telefono
        print("  Error: el telefono debe tener entre 6 y 15 digitos.")


# Muestra las condiciones especiales y devuelve la elegida.
def pedir_condicion():
    print("  Condicion del pasajero:")
    for posicion in range(len(CONDICIONES)):
        print("   " + str(posicion + 1) + ". " + CONDICIONES[posicion])
    opcion = pedir_entero("  Elija una opcion: ", 1, len(CONDICIONES))
    return CONDICIONES[opcion - 1]


# Pide una confirmacion s/n y devuelve True para si o False para no.
def pedir_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta == "s" or respuesta == "si" or respuesta == "sí":
            return True
        if respuesta == "n" or respuesta == "no":
            return False
        print("  Error: responda s o n.")


# Hace una pausa para que el usuario pueda leer el resultado.
def pausa():
    input("\nPresione ENTER para continuar...")
