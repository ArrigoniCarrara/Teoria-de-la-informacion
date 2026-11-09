"""
==========================================================================
 TEORIA DE LA INFORMACION - MENU POR TEMAS (VALORES HARDCODEADOS)
==========================================================================

Temas y modulos:

 1) CODIFICACION DE FUENTES DE INFORMACION
    1.1) Huffman.py                -> Codigo de Huffman, H, L, eficiencia, redundancia
    1.2) Shannon-Fano.py           -> Codigo de Shannon-Fano, H, L, eficiencia, redundancia
    1.3) Shannon.py                -> Clasificacion de un codigo, Kraft, compacto y 1er Teorema de Shannon
    1.4) RendimientoRedundancia.py -> Rendimiento y redundancia de un codigo dado
    1.5) Detec_errores.py          -> Bit de paridad par
    1.6) RecuperarMensaje.py       -> Paridad vertical y longitudinal: generar y recuperar mensaje
    1.7) Hamming.py                -> Distancia de Hamming y errores detectables/corregibles

 2) COMPRESION DE DATOS
    2.1) codificar_decodificar.py  -> Codificar/decodificar con Huffman y tasa de compresion
    2.2) RLC.py                    -> Compresion por longitud de corrida (RLC) a bytearray

 3) CANALES PARA LA TRANSMISION DE INFORMACION
    3.1) Matrizdecanal.py         -> Matriz del canal a partir de cadenas entrada/salida
    3.2) MatrizPrioriPost.py      -> P(salida), posteriori, simultaneos y entropias del canal
    3.3) CanalCompuesto.py        -> Matriz del canal compuesto (producto de matrices)
    3.4) ReduccionCanal.py        -> Reduccion suficiente de un canal (fusion de columnas)
    3.5) SinruidoyDet.py          -> Verifica si un canal es sin ruido y/o determinante
    3.6) CapacidadCanal.py        -> Tipo de canal y su capacidad
    3.7) CapacidadCanalPaso.py    -> Capacidad estimada con un paso
    3.8) ProbError.py             -> Regla de decision maxima y probabilidad de error

Para agregar un modulo nuevo: escribir su bloque de datos y su funcion
menu_xxx(), y sumarlo al diccionario OPCIONES_n del tema (ver al final).
==========================================================================
"""

import math
from math import log2


# ==========================================================================
# FUNCIONES COMUNES (usadas por varios modulos)
# ==========================================================================

def listas_paralelas(cadena, listaALF, listaPro):
    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char) / long)

    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0]))  # Ordeno los eventos para mayor comodidad

    listaALF.clear()
    listaPro.clear()

    for char, pro in parejas_ordenadas:
        listaALF.append(char)
        listaPro.append(pro)


def mostrar(nombre, mat):
    print(nombre)
    for fila in mat:
        print([round(x, 4) for x in fila])


# Usadas por Shannon.py y RendimientoRedundancia.py (eran identicas en ambos)
def Listas(cod, listaALF, listaLong):
    for x in cod:
        listaLong.append(len(x))
        for i in range(len(x)):
            if x[i] not in listaALF:
                listaALF.append(x[i])


def Long_media(listaPro, listaLong):
    aux = 0
    for i in range(len(listaPro)):
        aux += listaPro[i] * listaLong[i]
    return aux


def Entropia(lista, listaInfo):
    i = 0
    entropia = 0
    for num in lista:
        entropia += num * listaInfo[i]
        i = i + 1
    return entropia


def Generolista(lista, listaInfo, listaALF):
    r = len(listaALF)
    for num in lista:
        listaInfo.append(math.log(1 / num, r))


# ##########################################################################
# TEMA 1 - CODIFICACION DE FUENTES DE INFORMACION
# ##########################################################################

# ==========================================================================
# 1.1) HUFFMAN.PY - Codigo de Huffman
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
HUFF_USAR_CADENA = True   # True: usa HUFF_CADENA | False: usa HUFF_PROBS
HUFF_CADENA = "AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO"
HUFF_PROBS = [0.4, 0.25, 0.25, 0.1]
# ---------------------------------------------------------------------------


# Huffman es optimo: ningun codigo libre de prefijo tiene menor longitud media L.
# Si hay empates, puede dar codigos distintos segun el orden, pero el mismo L.
def huffman(probs):
    items = [[p, ""] for p in probs]
    codificar_huffman(sorted(items))
    return [code for _, code in items]


def codificar_huffman(items):
    # Caso base: quedan dos nodos, se asigna 0 y 1
    if len(items) == 1:
        items[0][1] = "0"
        return
    if len(items) == 2:
        items[0][1] = "0"
        items[1][1] = "1"
        return

    # Se toman los dos de menor probabilidad y se los combina en un nodo nuevo
    items = sorted(items, key=lambda x: x[0])
    a, b = items[0], items[1]
    nuevo = [a[0] + b[0], ""]

    # Llamada recursiva con la lista reducida
    codificar_huffman(items[2:] + [nuevo])

    # Al volver, el nodo combinado ya tiene su codigo:
    # los dos nodos que lo formaron lo extienden con 0 y 1
    a[1] = nuevo[1] + "0"
    b[1] = nuevo[1] + "1"


def metricas(probs, codigos):
    h = -sum(p * log2(p) for p in probs)                  # entropia
    l = sum(p * len(c) for p, c in zip(probs, codigos))   # longitud media
    n = h / l                                             # eficiencia
    return h, l, n, 1 - n


def menu_huffman():
    print("\n--- CODIGO DE HUFFMAN (Huffman.py) ---")
    if HUFF_USAR_CADENA:
        listaALF = []
        pro = []
        listas_paralelas(HUFF_CADENA, listaALF, pro)
        codigo = huffman(pro)
        print(f"{'Símbolo':<8} {'Prob.':<10} Código")
        for s, p, c in zip(listaALF, pro, codigo):
            print(f"{s:<8} {p:<10.4f} {c}")
    else:
        pro = HUFF_PROBS
        codigo = huffman(pro)
        print(f"{'Prob.':<10} Código")
        for p, c in zip(pro, codigo):
            print(f"{p:<10.4f} {c}")

    h, l, n, r = metricas(pro, codigo)
    print(f"H(S) = {h} bits")
    print(f"L = {l} bits")
    print(f"η = {n}")
    print(f"R = {r}")


# ==========================================================================
# 1.2) SHANNON-FANO.PY - Codigo de Shannon-Fano
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
SF_USAR_CADENA = True   # True: usa SF_CADENA | False: usa SF_PROBS
SF_CADENA = "AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO"
SF_PROBS = [0.4, 0.25, 0.25, 0.1]
# ---------------------------------------------------------------------------


# Es libre de prefijo y muy cercano al optimo, pero no siempre es optimo.
# Como el corte se decide mirando solo la suma de cada mitad, a veces queda una division poco favorable.
def shannon_fano(probs):
    items = [[p, ""] for p in probs]
    if len(items) == 1:
        return ["0"]
    # Se ordena de mayor a menor probabilidad
    codificar_shannon_fano(sorted(items, key=lambda x: x[0], reverse=True))
    return [code for _, code in items]


def codificar_shannon_fano(items):
    # Caso base: un solo simbolo, ya no hay nada que dividir
    if len(items) <= 1:
        return

    # Se busca el corte que deja las dos mitades con sumas lo mas parecidas posible
    total = sum(p for p, _ in items)
    acumulado = 0
    mejor_corte = 1
    mejor_dif = float("inf")
    for i in range(1, len(items)):
        acumulado += items[i - 1][0]
        dif = abs(acumulado - (total - acumulado))
        if dif < mejor_dif:
            mejor_dif = dif
            mejor_corte = i

    arriba = items[:mejor_corte]
    abajo = items[mejor_corte:]

    # Se asigna un bit a cada grupo
    for item in arriba:
        item[1] += "1"
    for item in abajo:
        item[1] += "0"

    # Se repite el proceso dentro de cada grupo
    codificar_shannon_fano(arriba)
    codificar_shannon_fano(abajo)


def menu_shannon_fano():
    print("\n--- CODIGO DE SHANNON-FANO (Shannon-Fano.py) ---")
    if SF_USAR_CADENA:
        listaALF = []
        pro = []
        listas_paralelas(SF_CADENA, listaALF, pro)
        codigo = shannon_fano(pro)
        print(f"{'Símbolo':<8} {'Prob.':<10} Código")
        for s, p, c in zip(listaALF, pro, codigo):
            print(f"{s:<8} {p:<10.4f} {c}")
    else:
        pro = SF_PROBS
        codigo = shannon_fano(pro)
        print(f"{'Prob.':<10} Código")
        for p, c in zip(pro, codigo):
            print(f"{p:<10.4f} {c}")

    h, l, n, r = metricas(pro, codigo)
    print(f"H(S) = {h} bits")
    print(f"L = {l} bits")
    print(f"η = {n}")
    print(f"R = {r}")


# ==========================================================================
# 1.3) SHANNON.PY - Clasificacion de un codigo y Primer Teorema de Shannon
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
SH_COD = ["BA", "CAB", "A", "CBA"]   # palabras del codigo (strings)
SH_PRO = [0.3, 0.1, 0.4, 0.2]        # probabilidad de cada simbolo de la fuente
SH_ORDENES = [1, 2]                  # ordenes de extension a verificar
# ---------------------------------------------------------------------------


def extension_fuente(alfabeto, distribucion, N, nuevoAlfabeto, nuevaDistribucion):
    alf = ['']
    pro = [1]

    for x in range(N):  # cada x++ es un orden
        alfTemp = []
        proTemp = []
        for i in range(len(alfabeto)):
            for j in range(len(alf)):
                alfTemp.append(alfabeto[i] + alf[j])
                proTemp.append(distribucion[i] * pro[j])
        alf = alfTemp
        pro = proTemp

    nuevoAlfabeto.extend(alf)
    nuevaDistribucion.extend(pro)


def InecuacionKraft(cod, listaALF):
    r = len(listaALF)
    aux = 0
    for x in cod:
        aux += r ** -len(x)
    return aux


def nosingular(cod):
    if len(cod) != len(set(cod)):
        return False
    return True


def instantaneo(cod):  # LOS ELEMENTOS DE LA LISTA DEBEN SER STRINGS
    if nosingular(cod):
        for i in range(len(cod)):
            for j in range(len(cod)):
                if i != j:
                    if cod[i].startswith(cod[j]):
                        return False  # prefijo
    else:
        return False
    return True


def univocamente_decodificable(cod):
    if nosingular(cod):

        if instantaneo(cod):
            return True

        C = set(cod)
        S1 = C
        conjuntos_vistos = []
        S_i = S1

        while True:
            S_siguiente = set()

            for x in S1:
                for y in S_i:
                    if x != y:
                        if y.startswith(x):
                            sufijo = y[len(x):]
                            S_siguiente.add(sufijo)
                        elif x.startswith(y):
                            sufijo = x[len(y):]
                            S_siguiente.add(sufijo)

            if not S_siguiente:  # conjunto de sufijos vacio: es UD
                return True

            if S_siguiente & C:  # algun sufijo es palabra del codigo: no es UD
                return False

            if S_siguiente in conjuntos_vistos:  # se repitio un S_i: es UD
                return True

            conjuntos_vistos.append(S_siguiente)
            S_i = S_siguiente
    return False


def Compacto(cod, listaInfo, listaLong):
    bool = True
    if univocamente_decodificable(cod):
        for i in range(len(listaInfo)):
            if math.ceil(listaInfo[i]) < listaLong[i]:
                bool = False
                break
    return bool


def cumple_shannon(pro, cod, N):
    # pro: distribucion de la fuente original
    # cod: palabras del codigo ORIGINAL (orden 1)
    # N:   orden de la extension (si N = 1 es el codigo sin extension)

    if not univocamente_decodificable(cod):
        return False

    listaALF = []
    listaLong = []
    Listas(cod, listaALF, listaLong)

    nuevoCod = []
    nuevoPro = []
    extension_fuente(cod, pro, N, nuevoCod, nuevoPro)

    # Nombres de los simbolos de la extension (solo para mostrar la tabla)
    simbolos = []
    for i in range(len(pro)):
        simbolos.append("s" + str(i + 1))
    nombres = []
    otraPro = []
    extension_fuente(simbolos, pro, N, nombres, otraPro)

    longitudes = []
    for palabra in nuevoCod:
        longitudes.append(len(palabra))

    print("  Simbolo  Prob.  Palabra codigo  Li")
    for i in range(len(nombres)):
        print("  ", nombres[i], round(nuevoPro[i], 4), nuevoCod[i], longitudes[i])

    Ln = Long_media(nuevoPro, longitudes)

    listaInfo = []
    Generolista(pro, listaInfo, listaALF)
    h = Entropia(pro, listaInfo)

    promedio = Ln / N
    cota_inferior = h
    cota_superior = h + 1 / N

    print("  N =", N)
    print("  r =", len(listaALF))
    print("  H_r(S) =", round(h, 4))
    print("  L_N =", round(Ln, 4))
    print("  L_N / N =", round(promedio, 4))
    print("  Cota:", round(cota_inferior, 4), "<= L_N/N <", round(cota_superior, 4))

    cumple_inferior = promedio >= cota_inferior - 0.000000001
    cumple_superior = promedio < cota_superior
    return cumple_inferior and cumple_superior


def menu_shannon():
    print("\n--- CLASIFICACION DE UN CODIGO Y 1er TEOREMA DE SHANNON (Shannon.py) ---")

    # ---------- Parte 1: clasificacion de un codigo ----------
    cod = SH_COD
    listaPro = SH_PRO
    print(cod)

    if not nosingular(cod):
        print("Clasificacion: Codigo Bloque (Singular)")
    else:
        if instantaneo(cod):
            print("Clasificacion: Instantaneo")
        else:
            if univocamente_decodificable(cod):
                print("Clasificacion: Univocamente Decodificable")
            else:
                print("Clasificacion: No Singular")

    listaALF = []
    listaLong = []
    Listas(cod, listaALF, listaLong)
    print("Lista alfabeto: ", listaALF)
    print("Lista Li: ", listaLong)

    kraft = InecuacionKraft(cod, listaALF)
    print("Kraft: ", kraft)

    if univocamente_decodificable(cod):
        listaInfo = []
        Generolista(listaPro, listaInfo, listaALF)
        entropia_cod = Entropia(listaPro, listaInfo)
        print("Entropia de la Fuente: ", entropia_cod)

        L_media = Long_media(listaPro, listaLong)
        print("Longitud media: ", L_media)

        if Compacto(cod, listaInfo, listaLong):
            print("Es Compacto")
        else:
            print("No es Compacto")

    # ---------- Parte 2: Primer Teorema de Shannon ----------
    print()
    print("===== Primer Teorema de Shannon =====")

    for N in SH_ORDENES:
        if N == 1:
            print("Codigo original (sin extension)")
        else:
            print("Extension de orden", N)
        print("Cumple Shannon:", cumple_shannon(listaPro, cod, N))
        print()


# ==========================================================================
# 1.4) RENDIMIENTOREDUNDANCIA.PY - Rendimiento y redundancia de un codigo
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
RR_PRO = [0.2, 0.15, 0.1, 0.3, 0.25]
RR_COD = ["01", "111", "110", "101", "100"]
# ---------------------------------------------------------------------------


def rendimiento_redundancia(pro, cod):
    listaALF = []
    listaLong = []
    Listas(cod, listaALF, listaLong)

    # Entropia de la fuente en base r
    listaInfo = []
    Generolista(pro, listaInfo, listaALF)
    h = Entropia(pro, listaInfo)

    # Longitud media del codigo
    L = Long_media(pro, listaLong)

    # Rendimiento y redundancia
    rendimiento = h / L
    redundancia = 1 - rendimiento

    print("  r =", len(listaALF))
    print("  H_r(S) =", round(h, 4))
    print("  L =", round(L, 4))

    return rendimiento, redundancia


def menu_rendimiento_redundancia():
    print("\n--- RENDIMIENTO Y REDUNDANCIA (RendimientoRedundancia.py) ---")
    n, R = rendimiento_redundancia(RR_PRO, RR_COD)

    print("Rendimiento (n) =", round(n, 4))
    print("Redundancia (R) =", round(R, 4))


# ==========================================================================
# 1.5) DETEC_ERRORES.PY - Bit de paridad par
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
PAR_CHAR = 'a'
# ---------------------------------------------------------------------------


def paridad_par(char):
    binario = format(ord(char), '07b')

    cant = 0
    for bit in binario:
        if bit == '1':
            cant += 1

    char_paridad = '1'
    if cant % 2 == 0:
        char_paridad = '0'

    binario = binario + char_paridad
    return binario


def verificar(binario):
    cant = 0
    for i in range(len(binario) - 1):
        if binario[i] == '1':
            cant += 1

    char_paridad = '1'
    if cant % 2 == 0:
        char_paridad = '0'

    return char_paridad == binario[len(binario) - 1]


def menu_paridad():
    print("\n--- BIT DE PARIDAD PAR (Detec_errores.py) ---")
    char = PAR_CHAR
    binario = paridad_par(char)
    print("Binario con ultimo bit de paridad: ", binario)

    if verificar(binario):
        print("Correcto")
    else:
        print("Incorrecto")


# ==========================================================================
# 1.6) RECUPERARMENSAJE.PY - Paridad vertical y longitudinal
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
RM_CADENA = "SOL"   # mensaje ASCII para generar los bytes con paridad
# Matriz dada (un byte por fila) para recuperar el mensaje, p. ej. de un ejercicio
RM_MATRIZ = [0b10100000, 0b10101110, 0b10011111, 0b10011001]
# ---------------------------------------------------------------------------


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


def menu_recuperar_mensaje():
    print("\n--- RECUPERAR MENSAJE CON PARIDAD (RecuperarMensaje.py) ---")
    datos = generar_bytes(RM_CADENA)
    print("Bytes generados:")
    for byte in datos:
        print(" ", byte_a_bits(byte))

    print("Mensaje:", recuperar_mensaje(datos))

    matriz_a = bytearray(RM_MATRIZ)
    print("Matriz dada:", recuperar_mensaje(matriz_a))


# ==========================================================================
# 1.7) HAMMING.PY - Distancia de Hamming
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
HAM_COD = ["0110000", "0000011", "0101101", "0100110"]
# ---------------------------------------------------------------------------


def hamming(cod):
    longitud = len(cod[0])
    dif_min = longitud    # la distancia maxima posible es la longitud

    for i in range(len(cod)):
        cad_actual = cod[i]
        for j in range(i + 1, len(cod)):     # j empieza en i + 1
            dif_j = 0
            for pos_car in range(longitud):
                if cod[j][pos_car] != cad_actual[pos_car]:
                    dif_j += 1

            if dif_j < dif_min:
                dif_min = dif_j
    return dif_min


def cant_errores(dh):
    if dh > 0:
        return dh - 1
    return 0


def cant_correcciones(dh):
    if dh > 0:
        return math.floor((dh - 1) / 2)
    return 0


def menu_hamming():
    print("\n--- DISTANCIA DE HAMMING (Hamming.py) ---")
    cod = HAM_COD
    distancia_hamming = hamming(cod)
    print("Distancia de Hamming: ", distancia_hamming)
    print("Se pueden detectar ", cant_errores(distancia_hamming), " errores")
    print("Se pueden corregir ", cant_correcciones(distancia_hamming), " errores")


# ##########################################################################
# TEMA 2 - COMPRESION DE DATOS
# ##########################################################################

# ==========================================================================
# 2.1) CODIFICAR_DECODIFICAR.PY - Codificar / decodificar con Huffman
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
CD_CADENA = "LAS PROBE CON TU ALFABETO ORIGINAL, DE TANTOS."
CD_ALFABETO = " ,.:;ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
# Una probabilidad por cada simbolo de CD_ALFABETO, en el mismo orden
CD_PRO = [
    0.175990, 0.014093, 0.015034, 0.000542, 0.002109, 0.111066, 0.015368, 0.030176,
    0.038747, 0.101604, 0.004873, 0.008762, 0.007953, 0.049740, 0.003706, 0.000034,
    0.048149, 0.021041, 0.050490, 0.002018, 0.073793, 0.019583, 0.010246, 0.051446,
    0.058406, 0.031093, 0.033240, 0.008930, 0.000012, 0.000706, 0.007851, 0.003199]
# ---------------------------------------------------------------------------


def codifico(cad, alfabeto, codigo):
    cod = ""
    for car in cad:
        cod += codigo[alfabeto.find(car)]
    return cod


def decodifico(cad_codificada, alfabeto, codigo):
    decod = ""
    aux = ""     # Acumulador temporal de bits

    for bit in cad_codificada:
        aux += bit

        if aux in codigo:
            # Busco en que posicion esta ese codigo
            indice = codigo.index(aux)
            # Concateno la letra directamente al string final
            decod += alfabeto[indice]
            aux = ""

    return decod


def tasa_compresion(cadena_original, cadena_codificada):
    bits_originales = len(cadena_original) * 8

    bits_comprimidos = len(cadena_codificada)

    if bits_comprimidos == 0:
        return 0.0

    return bits_originales / bits_comprimidos


def menu_codificar_decodificar():
    print("\n--- CODIFICAR / DECODIFICAR CON HUFFMAN (codificar_decodificar.py) ---")
    cad = CD_CADENA
    alfabeto = CD_ALFABETO
    pro = CD_PRO

    codigo = huffman(pro)
    for i in range(len(alfabeto)):
        print(alfabeto[i], pro[i], codigo[i])

    cad_codificada = codifico(cad, alfabeto, codigo)
    print("Cadena codificada: ", cad_codificada)

    cad_decodificada = decodifico(cad_codificada, alfabeto, codigo)
    print("Cadena Decodificada: ", cad_decodificada)
    print(cad == cad_decodificada)

    tasa = tasa_compresion(cad, cad_codificada)
    print(f"Tasa de compresión: {tasa:.2f}")


# ==========================================================================
# 2.2) RLC.PY - Compresion por longitud de corrida (Run Length Coding)
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
RLC_MENSAJE = "UUOOOOAAAIEUUUU"
# ---------------------------------------------------------------------------


def comprimir_rlc(mensaje):
    resultado = bytearray()
    i = 0
    while i < len(mensaje):
        caracter = mensaje[i]
        cantidad = 1
        # Cuento cuantas veces se repite seguido el mismo caracter
        while i + cantidad < len(mensaje) and mensaje[i + cantidad] == caracter and cantidad < 255:
            cantidad += 1
        resultado.append(ord(caracter))
        resultado.append(cantidad)
        i += cantidad
    return resultado


def rlc_a_texto(comprimido):
    texto = ""
    for i in range(0, len(comprimido), 2):
        caracter = chr(comprimido[i])
        cantidad = comprimido[i + 1]
        texto += caracter + str(cantidad)
    return texto


def menu_rlc():
    print("\n--- COMPRESION RLC (RLC.py) ---")
    mensaje = RLC_MENSAJE
    comprimido = comprimir_rlc(mensaje)
    print("Mensaje original:", mensaje)
    print("Cadena RLC:", rlc_a_texto(comprimido))
    print("Bytearray:", list(comprimido))


# ##########################################################################
# TEMA 3 - CANALES PARA LA TRANSMISION DE INFORMACION
# ##########################################################################

# ==========================================================================
# 3.1) MATRIZDECANAL.PY - Matriz del canal a partir de cadenas
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
MC_CADENA_ENTRADA = "110101100110101100110101100111110011"
MC_CADENA_SALIDA = "110021102110022010220121122100112011"
# ---------------------------------------------------------------------------


def proba(cad, sal, car_ent, alfSalida):
    # Cuenta cuantas veces, dado que entro car_ent, salio cada simbolo del alfabeto de salida
    cantidades = [0 for _ in range(len(alfSalida))]
    for i in range(len(cad)):
        if cad[i] == car_ent:
            cantidades[alfSalida.index(sal[i])] += 1
    deno = sum(cantidades)
    return [c / deno for c in cantidades]


def generoMC(mat, n, m, cad, sal, alfEntrada, alfSalida):
    for poscar in range(n):
        fila = proba(cad, sal, alfEntrada[poscar], alfSalida)
        for j in range(m):
            mat[poscar][j] = fila[j]


def menu_matriz_canal():
    print("\n--- MATRIZ DEL CANAL A PARTIR DE CADENAS (Matrizdecanal.py) ---")
    cadenaEntrada = MC_CADENA_ENTRADA
    cadenaSalida = MC_CADENA_SALIDA

    alfEntrada = []
    proEntrada = []
    listas_paralelas(cadenaEntrada, alfEntrada, proEntrada)

    alfSalida = []
    proSalida = []
    listas_paralelas(cadenaSalida, alfSalida, proSalida)

    n = len(alfEntrada)   # cantidad de simbolos de entrada
    m = len(alfSalida)    # cantidad de simbolos de salida

    matriz = [[0 for _ in range(m)] for _ in range(n)]

    generoMC(matriz, n, m, cadenaEntrada, cadenaSalida, alfEntrada, alfSalida)

    print("Alfabeto entrada:", alfEntrada, "Probabilidades a priori:", proEntrada)
    print("Alfabeto salida:", alfSalida, "Probabilidades salida:", proSalida)
    for i in range(n):
        print(alfEntrada[i], matriz[i])


# ==========================================================================
# 3.2) MATRIZPRIORIPOST.PY - Probabilidades y entropias del canal
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
PP_PRIORI = [0.25, 0.25, 0.25, 0.25]
# canal[i][j] = P(b_j | a_i) -> cada FILA suma 1
PP_CANAL = [[1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]]
# ---------------------------------------------------------------------------


def prob_salida(priori, canal):
    # P(b_j) = suma sobre i de P(a_i) * P(b_j | a_i)
    n = len(priori)
    m = len(canal[0])
    salida = [0 for _ in range(m)]
    for j in range(m):
        for i in range(n):
            salida[j] += priori[i] * canal[i][j]
    return salida


def matriz_posteriori(priori, canal, salida):
    # P(a_i | b_j) = P(b_j | a_i) * P(a_i) / P(b_j)
    n = len(priori)
    m = len(salida)
    post = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            post[i][j] = canal[i][j] * priori[i] / salida[j]
    return post


def matriz_simultaneos(priori, canal):
    # P(a_i, b_j) = P(a_i) * P(b_j | a_i)
    n = len(priori)
    m = len(canal[0])
    sim = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            sim[i][j] = priori[i] * canal[i][j]
    return sim


def entropia_apriori(priori):
    # H(A) = suma de P(a) * log2(1 / P(a))
    h = 0
    for p in priori:
        if p > 0:
            h += p * math.log2(1 / p)
    return h


def entropias_aposteriori(post):
    # H(A/b_j) = suma sobre i de P(a_i | b_j) * log2(1 / P(a_i | b_j))
    n = len(post)
    m = len(post[0])
    h = [0 for _ in range(m)]
    for j in range(m):
        for i in range(n):
            p = post[i][j]
            if p > 0:
                h[j] += p * math.log2(1 / p)
    return h


def equivocacion(sim, post):
    # H(A/B) = suma de P(a,b) * log2(1 / P(a/b))
    n = len(sim)
    m = len(sim[0])
    h = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                h += sim[i][j] * math.log2(1 / post[i][j])
    return h


def perdida(sim, canal):
    # H(B/A) = suma de P(a,b) * log2(1 / P(b/a))
    n = len(sim)
    m = len(sim[0])
    h = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                h += sim[i][j] * math.log2(1 / canal[i][j])
    return h


def entropia_afin(sim):
    # H(A,B) = suma de P(a,b) * log2(1 / P(a,b))
    n = len(sim)
    m = len(sim[0])
    h = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                h += sim[i][j] * math.log2(1 / sim[i][j])
    return h


def informacion_mutua_sim(sim, priori, salida):
    # I(A,B) = suma de P(a,b) * log2( P(a,b) / (P(a) * P(b)) )
    n = len(sim)
    m = len(sim[0])
    info = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                info += sim[i][j] * math.log2(sim[i][j] / (priori[i] * salida[j]))
    return info


def entropia_salida(salida):
    # H(B) = suma de P(b) * log2(1 / P(b))
    h = 0
    for p in salida:
        if p > 0:
            h += p * math.log2(1 / p)
    return h


def menu_probas_entropias():
    print("\n--- PROBABILIDADES Y ENTROPIAS DEL CANAL (MatrizPrioriPost.py) ---")
    priori = PP_PRIORI
    canal = PP_CANAL

    assert len(priori) == len(canal), "priori y canal deben tener la misma cantidad de filas"

    salida = prob_salida(priori, canal)
    posteriori = matriz_posteriori(priori, canal, salida)
    simultaneos = matriz_simultaneos(priori, canal)

    print("P(salida):", [round(x, 4) for x in salida])
    mostrar("Posteriori P(A|B):", posteriori)
    mostrar("Simultáneos P(A,B):", simultaneos)

    hA = entropia_apriori(priori)
    hAb = entropias_aposteriori(posteriori)

    print("H(A) =", round(hA, 4), "bits")
    for j in range(len(hAb)):
        print("H(A/b" + str(j + 1) + ") =", round(hAb[j], 4), "bits")

    hB = entropia_salida(salida)
    print("H(B) =", round(hB, 4), "bits")
    print("Equivocación H(A/B) =", round(equivocacion(simultaneos, posteriori), 4), "bits")
    print("Pérdida H(B/A) =", round(perdida(simultaneos, canal), 4), "bits")
    print("Entropía afín H(A,B) =", round(entropia_afin(simultaneos), 4), "bits")
    print("Información mutua I(A,B) =", round(informacion_mutua_sim(simultaneos, priori, salida), 4), "bits")


# ==========================================================================
# 3.3) CANALCOMPUESTO.PY - Canal compuesto (producto de matrices)
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
# Las columnas del canal 1 deben ser iguales a las filas del canal 2
CC_CANAL1 = [[0.7, 0.0, 0.3, 0.0],
             [0.2, 0.6, 0.0, 0.2]]

CC_CANAL2 = [[0.9, 0.0, 0.1],
             [0.0, 1.0, 0.0],
             [0.1, 0.1, 0.8],
             [0.0, 0.5, 0.5]]
# ---------------------------------------------------------------------------


def compuesto(canal1, n1, m1, canal2, n2, m2):
    if m1 != n2:
        print("Las columnas del canal 1 deben ser iguales a las filas del canal 2")

    resultado = [[0.0] * m2 for _ in range(n1)]

    for i in range(n1):
        for j in range(m2):
            for k in range(m1):
                resultado[i][j] += canal1[i][k] * canal2[k][j]

    return resultado


def menu_canal_compuesto():
    print("\n--- CANAL COMPUESTO (CanalCompuesto.py) ---")
    canal1 = CC_CANAL1
    canal2 = CC_CANAL2

    n1 = len(canal1)
    m1 = len(canal1[0])

    n2 = len(canal2)
    m2 = len(canal2[0])

    for fila in compuesto(canal1, n1, m1, canal2, n2, m2):
        print([round(p, 4) for p in fila])


# ==========================================================================
# 3.4) REDUCCIONCANAL.PY - Reduccion suficiente de un canal
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
RC_CANAL = [[0.0, 0.5, 0.0, 0.5],
            [0.8, 0.0, 0.2, 0.0],
            [0.0, 0.5, 0.0, 0.5],
            [0.8, 0.0, 0.2, 0.0]]
# ---------------------------------------------------------------------------


def es_reduccion_suficiente(canal, j, k, tol=1e-9):
    n = len(canal)
    for i in range(n):
        for l in range(i + 1, n):
            if abs(canal[i][j] * canal[l][k] - canal[i][k] * canal[l][j]) > tol:
                return False
    return True


def canal_determinante(s, j, k):
    if j == k or not (0 <= j < s) or not (0 <= k < s):
        print("Los índices deben ser dos columnas distintas y válidas")
    lo, hi = min(j, k), max(j, k)
    det = [[0] * (s - 1) for _ in range(s)]
    for c in range(s):
        if c == hi:
            destino = lo
        elif c > hi:
            destino = c - 1
        else:
            destino = c
        det[c][destino] = 1
    return det


def reducir(canal, j, k):
    n, s = len(canal), len(canal[0])
    det = canal_determinante(s, j, k)
    return compuesto(canal, n, s, det, s, s - 1)


def imprimir(matriz, titulo):
    print(titulo)
    for fila in matriz:
        print("  ", [round(p, 4) for p in fila])


def reducir_todo(canal):
    imprimir(canal, "Canal original:")
    paso = 0

    while True:
        s = len(canal[0])

        # Busca el primer par de columnas que se pueda fusionar
        par = None
        for j in range(s):
            for k in range(j + 1, s):
                if es_reduccion_suficiente(canal, j, k):
                    par = (j, k)
                    break
            if par:
                break

        if par is None:
            break

        paso += 1
        j, k = par
        det = canal_determinante(s, j, k)
        canal = reducir(canal, j, k)

        print(f"\n--- Paso {paso}: fusionar columnas {j} y {k} ---")
        imprimir(det, "Canal determinante:")
        imprimir(canal, "Canal reducido:")

    print(f"\nNo quedan más reducciones. Reducción máxima: {len(canal[0])} columnas.")
    return canal


def menu_reduccion_canal():
    print("\n--- REDUCCION DE UN CANAL (ReduccionCanal.py) ---")
    reducir_todo(RC_CANAL)


# ==========================================================================
# 3.5) SINRUIDOYDET.PY - Canal sin ruido y/o determinante
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
SD_MATRIZ = [[0, 1, 0],
             [0, 0, 1],
             [0, 1, 0],
             [1, 0, 0]]
# ---------------------------------------------------------------------------


def sinruido(matriz, n, m):
    for j in range(m):
        x = 0
        for i in range(n):
            if matriz[i][j] != 0:
                if x != 0:
                    return 0
                else:
                    x += 1
    return 1


def determinante(matriz, n, m):
    for i in range(n):
        x = 0
        for j in range(m):
            if matriz[i][j] != 0:
                if x != 0:
                    return 0
                else:
                    x += 1
    return 1


def menu_sinruido_det():
    print("\n--- CANAL SIN RUIDO Y/O DETERMINANTE (SinruidoyDet.py) ---")
    matriz = SD_MATRIZ
    n = len(matriz)
    m = len(matriz[0])

    if sinruido(matriz, n, m):
        print("Es un canal sin ruido")
    else:
        print("No es un canal sin ruido")

    if determinante(matriz, n, m):
        print("Es un canal determinante")
    else:
        print("No es un canal determinante")


# ==========================================================================
# 3.6) CAPACIDADCANAL.PY - Tipo de canal y capacidad
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
CAP_NOMBRE = "Ejercicio"
CAP_CANAL = [[0.77, 0.23],
             [0.20, 0.80]]
# ---------------------------------------------------------------------------

def entropia(valores):
    h = 0
    for p in valores:
        if p > 0:
            h = h - p * log2(p)
    return h


def es_determinante(canal):
    for fila in canal:
        cantidad_no_nulos = 0
        for p in fila:
            if p > 0:
                cantidad_no_nulos = cantidad_no_nulos + 1
                if abs(p - 1) > 0.000001:
                    return False
        if cantidad_no_nulos != 1:
            return False
    return True


def es_sin_ruido(canal):
    if not es_determinante(canal):
        return False

    n = len(canal)
    m = len(canal[0])
    if n != m:
        return False

    for j in range(m):
        unos_en_columna = 0
        for i in range(n):
            if canal[i][j] > 0:
                unos_en_columna = unos_en_columna + 1
        if unos_en_columna != 1:
            return False
    return True


def capacidad_determinante(canal):
    # C = log2(m_utiles), con m_utiles = columnas que tienen al menos un 1
    n = len(canal)
    m = len(canal[0])
    utiles = 0

    for j in range(m):
        columna_usada = False
        for i in range(n):
            if canal[i][j] > 0:
                columna_usada = True
        if columna_usada:
            utiles = utiles + 1

    return log2(utiles)


def capacidad_sin_ruido(canal):
    # C = log2(n)
    n = len(canal)
    return log2(n)



def tipos_de_canal(canal):
    # Devuelve una lista con TODOS los tipos que cumple el canal
    tipos = []
    if es_sin_ruido(canal):
        tipos.append("sin ruido")
    if es_determinante(canal):
        tipos.append("determinante")
    return tipos


def capacidad_por_tipo(canal, tipo):
    if tipo == "sin ruido":
        return capacidad_sin_ruido(canal)
    if tipo == "determinante":
        return capacidad_determinante(canal)


def informacion_mutua_canal(canal, pa):
    n = len(canal)
    m = len(canal[0])

    pb = []
    for j in range(m):
        suma = 0
        for i in range(n):
            suma = suma + pa[i] * canal[i][j]
        pb.append(suma)

    info = 0
    for i in range(n):
        for j in range(m):
            if pa[i] > 0 and canal[i][j] > 0 and pb[j] > 0:
                termino = pa[i] * canal[i][j] * log2(canal[i][j] / pb[j])
                info = info + termino
    return info


def capacidad_general(canal):
    mejor_p = 0.5
    mejor_info = -1

    desde = 0.1
    hasta = 0.9
    paso = 0.1

    for ronda in range(6):
        print("  Ronda", ronda + 1, ": p de", round(desde, 6), "a", round(hasta, 6),
              "con paso", paso)

        p = desde
        while p <= hasta + 0.0000001:
            pa = [p, 1 - p]
            info = informacion_mutua_canal(canal, pa)
            if info > mejor_info:
                mejor_info = info
                mejor_p = p
            p = p + paso

        print("    Mejor hasta ahora: p =", round(mejor_p, 6),
              " I =", round(mejor_info, 6))

        desde = mejor_p - paso
        hasta = mejor_p + paso
        paso = paso / 10
        if desde < 0:
            desde = 0
        if hasta > 1:
            hasta = 1

    return mejor_p, mejor_info


def menu_capacidad_canal():
    print("\n--- TIPO DE CANAL Y CAPACIDAD (CapacidadCanal.py) ---")
    nombre = CAP_NOMBRE
    canal = CAP_CANAL

    print("Canal:", nombre)

    tipos = tipos_de_canal(canal)

    if len(tipos) > 0:
        print("  Cumple los tipos:", tipos)
        for tipo in tipos:
            c = capacidad_por_tipo(canal, tipo)
            print("  Capacidad como", tipo, ":", round(c, 4), "bits/simbolo")
    else:
        print("  No es sin ruido ni determinante")
        if len(canal) == 2:
            p, c = capacidad_general(canal)
            print("  Capacidad:", round(c, 4), "bits/simbolo, con p(x1) =", round(p, 4))
        else:
            print("  Esta busqueda solo esta hecha para canales de 2 entradas")
    print()


# ==========================================================================
# 3.7) CAPACIDADCANALPASO.PY - Capacidad estimada con un paso
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
PASO_CANAL = [[0.77, 0.23],
              [0.20, 0.80]]       # canal BINARIO (2 entradas)
PASO_PASOS = [0.1, 0.01, 0.001]   # pasos a probar
# ---------------------------------------------------------------------------


def estimar_capacidad(canal, paso):
    # Prueba P(a1) = 0, paso, 2*paso, ... hasta 1 (con P(a2) = 1 - P(a1))
    # y se queda con la que da mayor informacion mutua
    cantidad = int(1 / paso + 0.0000001)
    mejor_p = 0
    mejor_info = -1

    for k in range(cantidad + 1):
        p = k * paso
        if p > 1:
            p = 1
        info = informacion_mutua_canal(canal, [p, 1 - p])
        if info > mejor_info:
            mejor_info = info
            mejor_p = p

    return mejor_info, mejor_p


def menu_capacidad_paso():
    print("\n--- CAPACIDAD ESTIMADA CON PASO (CapacidadCanalPaso.py) ---")
    canal = PASO_CANAL

    for paso in PASO_PASOS:
        capacidad, p = estimar_capacidad(canal, paso)
        print("Paso", paso, "-> C =", round(capacidad, 6),
              "bits/simbolo, con P(a1) =", round(p, 4))


# ==========================================================================
# 3.8) PROBERROR.PY - Regla de decision maxima y probabilidad de error
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
PE_PA = [1/8, 3/8, 4/8]          # probabilidades a priori
PE_CANAL = [[0.6, 0.3, 0.1],        # canal[i][j] = P(b_j | a_i)
            [0.1, 0.8, 0.1],
            [0.3, 0.3, 0.4]]
# ---------------------------------------------------------------------------


def decision_maxima(canal):
    n = len(canal)
    m = len(canal[0])

    decision = []
    for j in range(m):
        mejor_i = 0
        mejor_valor = canal[0][j]

        for i in range(1, n):
            if canal[i][j] > mejor_valor:
                mejor_valor = canal[i][j]
                mejor_i = i

        decision.append(mejor_i)

    return decision


def probabilidad_error(pa, canal):
    m = len(canal[0])
    decision = decision_maxima(canal)

    p_acierto = 0
    for j in range(m):
        i = decision[j]
        p_conjunta = pa[i] * canal[i][j]
        p_acierto = p_acierto + p_conjunta

    return 1 - p_acierto


def menu_prob_error():
    print("\n--- DECISION MAXIMA Y PROBABILIDAD DE ERROR (ProbError.py) ---")
    pa = PE_PA
    canal = PE_CANAL

    decision = decision_maxima(canal)

    print("Regla de decision (salida -> entrada decidida):")
    for j in range(len(decision)):
        print("  b" + str(j + 1), "->", "a" + str(decision[j] + 1))

    pe = probabilidad_error(pa, canal)
    print("Probabilidad de error:", round(pe, 4))


# ==========================================================================
# MENUS
# ==========================================================================
# Cada tema es un diccionario:  clave -> (texto del menu, funcion, descripcion)
# Para agregar un modulo nuevo, sumar una linea al diccionario del tema.

OPCIONES_1 = {
    "1": ("Codigo de Huffman                                [HUFF_USAR_CADENA, HUFF_CADENA, HUFF_PROBS]",
          menu_huffman,
          "Codigo de Huffman: a partir de una cadena (HUFF_CADENA) o de una lista de"
          " probabilidades (HUFF_PROBS, segun HUFF_USAR_CADENA) genera el codigo y"
          " calcula entropia H(S), longitud media L, eficiencia y redundancia."),
    "2": ("Codigo de Shannon-Fano                           [SF_USAR_CADENA, SF_CADENA, SF_PROBS]",
          menu_shannon_fano,
          "Codigo de Shannon-Fano: ordena las probabilidades de mayor a menor y las"
          " divide en dos grupos de suma lo mas parecida posible, repitiendo el proceso."
          " Calcula H(S), L, eficiencia y redundancia. Usa SF_CADENA o SF_PROBS segun"
          " SF_USAR_CADENA."),
    "3": ("Clasificacion de un codigo y 1er Teorema de Shannon  [SH_COD, SH_PRO, SH_ORDENES]",
          menu_shannon,
          "Clasifica el codigo SH_COD (singular, no singular, instantaneo, univocamente"
          " decodificable), calcula Kraft, entropia, longitud media y si es compacto."
          " Despues verifica el Primer Teorema de Shannon para cada orden de extension"
          " de SH_ORDENES."),
    "4": ("Rendimiento y redundancia de un codigo           [RR_PRO, RR_COD]",
          menu_rendimiento_redundancia,
          "Dadas las probabilidades RR_PRO y las palabras del codigo RR_COD, calcula"
          " la entropia en base r, la longitud media, el rendimiento y la redundancia."),
    "5": ("Bit de paridad par                              [PAR_CHAR]",
          menu_paridad,
          "Agrega el bit de paridad par al codigo ASCII de 7 bits del caracter PAR_CHAR"
          " y verifica la paridad."),
    "6": ("Recuperar mensaje con paridad vertical/longitudinal  [RM_CADENA, RM_MATRIZ]",
          menu_recuperar_mensaje,
          "Genera los bytes de RM_CADENA con bit de paridad por caracter y fila de"
          " paridad longitudinal, y recupera el mensaje detectando y corrigiendo un"
          " error. Tambien recupera el mensaje de una matriz dada (RM_MATRIZ)."),
    "7": ("Distancia de Hamming                            [HAM_COD]",
          menu_hamming,
          "Calcula la distancia de Hamming minima del codigo HAM_COD y cuantos errores"
          " se pueden detectar (dh-1) y corregir ((dh-1)/2)."),
}

OPCIONES_2 = {
    "1": ("Codificar / decodificar con Huffman + tasa      [CD_CADENA, CD_ALFABETO, CD_PRO]",
          menu_codificar_decodificar,
          "Arma el codigo de Huffman para CD_ALFABETO con las probabilidades CD_PRO,"
          " codifica CD_CADENA, la decodifica para verificar que coincide con la"
          " original y calcula la tasa de compresion (bits originales a 8 bits por"
          " caracter / bits codificados)."),
    "2": ("Compresion RLC (longitud de corrida)            [RLC_MENSAJE]",
          menu_rlc,
          "Comprime RLC_MENSAJE con RLC: un byte para el codigo ASCII del caracter y"
          " otro para la cantidad de repeticiones seguidas (maximo 255). Muestra la"
          " cadena tipo a3b5 y el bytearray."),
}

OPCIONES_3 = {
    "1": ("Matriz del canal a partir de cadenas            [MC_CADENA_ENTRADA, MC_CADENA_SALIDA]",
          menu_matriz_canal,
          "Dadas una cadena de entrada y su salida, calcula los alfabetos, las"
          " probabilidades a priori y la matriz del canal P(b|a) de n x m."),
    "2": ("Probabilidades y entropias del canal            [PP_PRIORI, PP_CANAL]",
          menu_probas_entropias,
          "Dadas las probabilidades a priori y la matriz del canal, calcula P(salida),"
          " posteriori, simultaneos, H(A), H(A/bj), H(B), equivocacion H(A/B),"
          " perdida H(B/A), entropia afin H(A,B) e informacion mutua I(A,B)."),
    "3": ("Canal compuesto                                 [CC_CANAL1, CC_CANAL2]",
          menu_canal_compuesto,
          "Multiplica la matriz del canal 1 por la del canal 2 para obtener la matriz"
          " del canal compuesto. Las columnas del canal 1 deben ser iguales a las"
          " filas del canal 2."),
    "4": ("Reduccion de un canal                            [RC_CANAL]",
          menu_reduccion_canal,
          "Busca pares de columnas de RC_CANAL que se pueden fusionar (reduccion"
          " suficiente) y las fusiona paso a paso con un canal determinante, hasta"
          " llegar a la reduccion maxima."),
    "5": ("Canal sin ruido y/o determinante                [SD_MATRIZ]",
          menu_sinruido_det,
          "Verifica si SD_MATRIZ es un canal sin ruido (cada columna tiene a lo sumo"
          " un elemento no nulo) y/o determinante (cada fila tiene a lo sumo uno)."),
    "6": ("Tipo de canal y capacidad                       [CAP_NOMBRE, CAP_CANAL]",
          menu_capacidad_canal,
          "Indica si el canal es sin ruido, determinante y calcula la"
          " capacidad de cada tipo. Si no es de ninguno y tiene 2 entradas, busca la"
          " capacidad refinando el valor de p en varias rondas."),
    "7": ("Capacidad estimada con paso (canal binario)     [PASO_CANAL, PASO_PASOS]",
          menu_capacidad_paso,
          "Prueba P(a1) = 0, paso, 2*paso, ..., 1 y se queda con la que da mayor"
          " informacion mutua: esa es la capacidad estimada, junto con su probabilidad."),
    "8": ("Decision maxima y probabilidad de error         [PE_PA, PE_CANAL]",
          menu_prob_error,
          "Para cada salida decide la entrada con mayor P(b|a) (regla de decision"
          " maxima) y calcula la probabilidad de error del canal con las"
          " probabilidades a priori PE_PA."),
}

TEMAS = {
    "1": ("Codificacion de fuentes de informacion", OPCIONES_1),
    "2": ("Compresion de datos", OPCIONES_2),
    "3": ("Canales para la transmision de informacion", OPCIONES_3),
}


def submenu(titulo, opciones):
    while True:
        print("\n==========================================================")
        print(" " + titulo.upper())
        print(" (editar los valores hardcodeados de cada bloque antes de correr)")
        print("==========================================================")
        for clave in opciones:
            print(f" {clave}) {opciones[clave][0]}")
        print(" d) Ver descripcion de una opcion")
        print(" 0) Volver")
        print("==========================================================")
        eleccion = input("Elija una opcion: ").strip().lower()

        if eleccion == "0":
            break
        elif eleccion == "d":
            sub = input("De que opcion quiere ver la descripcion? ").strip()
            if sub in opciones:
                print(opciones[sub][2])
            else:
                print("Opcion invalida.")
        elif eleccion in opciones:
            try:
                opciones[eleccion][1]()
            except Exception as e:
                print("Ocurrio un error:", e)
        else:
            print("Opcion invalida, intente de nuevo.")


def mostrar_menu():
    print("\n==========================================================")
    print(" MENU - TEORIA DE LA INFORMACION")
    print("==========================================================")
    for clave in TEMAS:
        print(f" {clave}) {TEMAS[clave][0]}")
    print(" 0) Salir")
    print("==========================================================")


def main():
    while True:
        mostrar_menu()
        eleccion = input("Elija un tema: ").strip()

        if eleccion == "0":
            print("Saliendo...")
            break
        elif eleccion in TEMAS:
            submenu(TEMAS[eleccion][0], TEMAS[eleccion][1])
        else:
            print("Opcion invalida, intente de nuevo.")


if __name__ == "__main__":
    main()