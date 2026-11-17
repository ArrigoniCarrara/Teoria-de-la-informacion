import math

MATRIZ = [[0, 0, 1.0],
          [0.4, 0.4, 0.2]]
MENSAJE = "000010011111111011010111"


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

    return math.log2(utiles)


def capacidad_sin_ruido(canal):
    n = len(canal)
    return math.log2(n)


def tipos_de_canal(canal):
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
                termino = pa[i] * canal[i][j] * math.log2(canal[i][j] / pb[j])
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
              " 1 - p =", round(1 - mejor_p, 6),
              " I =", round(mejor_info, 6))

        desde = mejor_p - paso
        hasta = mejor_p + paso
        paso = paso / 10
        if desde < 0:
            desde = 0
        if hasta > 1:
            hasta = 1

    return mejor_p, mejor_info


def prob_salida(priori, canal):
    n = len(priori)
    m = len(canal[0])
    salida = [0 for _ in range(m)]
    for j in range(m):
        for i in range(n):
            salida[j] += priori[i] * canal[i][j]
    return salida


def matriz_simultaneos(priori, canal):
    n = len(priori)
    m = len(canal[0])
    sim = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            sim[i][j] = priori[i] * canal[i][j]
    return sim


def matriz_posteriori(priori, canal, salida):
    n = len(priori)
    m = len(salida)
    post = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            post[i][j] = canal[i][j] * priori[i] / salida[j]
    return post


def equivocacion(sim, post):
    n = len(sim)
    m = len(sim[0])
    h = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                h += sim[i][j] * math.log2(1 / post[i][j])
    return h


def perdida(sim, canal):
    n = len(sim)
    m = len(sim[0])
    h = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                h += sim[i][j] * math.log2(1 / canal[i][j])
    return h


def informacion_mutua_sim(sim, priori, salida):
    n = len(sim)
    m = len(sim[0])
    info = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                info += sim[i][j] * math.log2(sim[i][j] / (priori[i] * salida[j]))
    return info


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


def paridad(bits):
    cantidad = 0
    for b in bits:
        if b == 1:
            cantidad = cantidad + 1
    return cantidad % 2


def byte_a_bits(numero):
    bits = []
    for pos in range(7, -1, -1):
        bits.append((numero >> pos) & 1)
    return bits


def recuperar_mensaje(datos):
    matriz = []
    for byte in datos:
        matriz.append(byte_a_bits(byte))

    filas = len(matriz)

    filas_mal = []
    for i in range(filas):
        if paridad(matriz[i]) != 0:
            filas_mal.append(i)

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
        print(f"  Error en fila {i + 1}, columna {j + 1} -> corregido")
        matriz[i][j] = 1 - matriz[i][j]
    else:
        print("  Errores que no se pueden corregir")
        return "", ""

    cadena_corregida = ""
    for fila in matriz:
        for bit in fila:
            cadena_corregida += str(bit)

    texto = ""
    for i in range(1, filas):
        codigo = 0
        for j in range(7):
            codigo = codigo * 2 + matriz[i][j]
        texto = texto + chr(codigo)

    return cadena_corregida, texto


print("\n--- CAPACIDAD DEL CANAL ---")
tipos = tipos_de_canal(MATRIZ)

if len(tipos) > 0:
    print("  Cumple los tipos:", tipos)
    for tipo in tipos:
        c = capacidad_por_tipo(MATRIZ, tipo)
        print("  Capacidad como", tipo, ":", round(c, 4), "bits/simbolo")
else:
    print("  No es sin ruido ni determinante")
    if len(MATRIZ) == 2:
        p, c = capacidad_general(MATRIZ)
        proEntrada = [p, 1 - p]
        print("  Capacidad:", round(c, 4), "bits/simbolo")
        print("  P(0) = p =", round(proEntrada[0], 4))
        print("  P(1) = 1 - p =", round(proEntrada[1], 4))
    else:
        print("  Esta busqueda solo esta hecha para canales de 2 entradas")
print()

print("\n--- EQUIVOCACION, PERDIDA E INFORMACION MUTUA ---")
proSalida = prob_salida(proEntrada, MATRIZ)
matriz_sim = matriz_simultaneos(proEntrada, MATRIZ)
matriz_post = matriz_posteriori(proEntrada, MATRIZ, proSalida)

print("Equivocacion (H(A/B)): ", equivocacion(matriz_sim, matriz_post))
print("Perdida (H(B/A)): ", perdida(matriz_sim, MATRIZ))
print("Informacion mutua (I(A;B)): ", informacion_mutua_sim(matriz_sim, proEntrada, proSalida))

print("\n--- DETECCION Y CORRECCION DE ERRORES ---")
datos = []
for i in range(0, len(MENSAJE), 8):
    datos.append(int(MENSAJE[i:i + 8], 2))

cadena_corregida, texto = recuperar_mensaje(datos)
print("Mensaje recibido:  ", MENSAJE)
print("Mensaje corregido: ", cadena_corregida)
print("Texto recuperado:  ", texto)

print("\n--- ANALISIS DE LA TRANSMISION POR EL CANAL ---")
decision = decision_maxima(MATRIZ)
print("Regla de decision de maxima posibilidad (salida -> entrada decidida):")
for j in range(len(decision)):
    print("  " + chr(ord("A") + j), "->", decision[j])
