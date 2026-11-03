def paridad(bits):
    # Devuelve el bit que hace que la cantidad de unos sea PAR
    cantidad = 0
    for b in bits:
        if b == 1:
            cantidad = cantidad + 1
    return cantidad % 2


def byte_a_bits(numero):
    # Pasa un byte (0 a 255) a una lista de 8 bits, el primero es el mas significativo
    bits = []
    for pos in range(7, -1, -1):
        bits.append((numero >> pos) & 1)
    return bits


def bits_a_byte(bits):
    # Pasa una lista de 8 bits a un numero entero
    numero = 0
    for b in bits:
        numero = numero * 2 + b
    return numero

def generar_bytes(cadena):
    filas = len(cadena) + 1
    matriz = []
    for i in range(filas):
        matriz.append([0] * 8)

    # Filas 1 en adelante: 7 bits del ASCII + bit de paridad vertical
    for i in range(len(cadena)):
        codigo = ord(cadena[i])
        if codigo > 127:
            raise ValueError("Solo se admiten caracteres ASCII")

        bits = byte_a_bits(codigo)       # el primer bit siempre es 0
        siete_bits = bits[1:]            # los 7 bits del caracter
        for j in range(7):
            matriz[i + 1][j] = siete_bits[j]
        matriz[i + 1][7] = paridad(siete_bits)

    # Fila 0: paridad longitudinal de cada columna
    for j in range(8):
        columna = []
        for i in range(1, filas):
            columna.append(matriz[i][j])
        matriz[0][j] = paridad(columna)

    # Paridad cruzada: paridad de los 7 bits de la fila 0
    matriz[0][7] = paridad(matriz[0][0:7])

    
    resultado = bytearray()
    for fila in matriz:
        resultado.append(bits_a_byte(fila))
    return resultado

def recuperar_mensaje(datos):
    matriz = []
    for byte in datos:
        matriz.append(byte_a_bits(byte))

    filas = len(matriz)

    # Filas con paridad incorrecta 
    filas_mal = []
    for i in range(filas):
        if paridad(matriz[i]) != 0:
            filas_mal.append(i)

    # Columnas con paridad incorrecta
    columnas_mal = []
    for j in range(8):
        columna = []
        for i in range(filas):
            columna.append(matriz[i][j])
        if paridad(columna) != 0:
            columnas_mal.append(j)

    if len(filas_mal) == 0 and len(columnas_mal) == 0:
        print("  Sin errores")
    elif len(filas_mal) == 1 and len(columnas_mal) == 1:
        i = filas_mal[0]
        j = columnas_mal[0]
        print("  Error en fila", i, "columna", j, "-> corregido")
        matriz[i][j] = 1 - matriz[i][j]
    else:
        print("  Errores que no se pueden corregir")
        return ""

    texto = ""
    for i in range(1, filas):
        codigo = 0
        for j in range(7):
            codigo = codigo * 2 + matriz[i][j]
        texto = texto + chr(codigo)
    return texto


if __name__ == "__main__":
    
    datos = generar_bytes("Miercoles")
    print("Bytes generados:")
    for byte in datos:
        print(" ", byte_a_bits(byte))

    print("Mensaje:", recuperar_mensaje(datos))

    # Si el ejercicio ya me viene una matriz:
    matriz_a = bytearray([0b00111110, 0b10000111, 0b10010000, 0b10000010, 0b10101010])
    print("Ejercicio 13h:", recuperar_mensaje(matriz_a))