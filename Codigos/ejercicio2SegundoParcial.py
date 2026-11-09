import math
# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
MC_CADENA_ENTRADA = "10100000101011101001111110011001"
MC_CADENA_SALIDA = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"
# ---------------------------------------------------------------------------

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

def matriz_simultaneos(priori, canal):
    # P(a_i, b_j) = P(a_i) * P(b_j | a_i)
    n = len(priori)
    m = len(canal[0])
    sim = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            sim[i][j] = priori[i] * canal[i][j]
    return sim

def matriz_posteriori(priori, canal, salida):
    # P(a_i | b_j) = P(b_j | a_i) * P(a_i) / P(b_j)
    n = len(priori)
    m = len(salida)
    post = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            post[i][j] = canal[i][j] * priori[i] / salida[j]
    return post

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

def compuesto(canal1, n1, m1, canal2, n2, m2):
    if m1 != n2:
        print("Las columnas del canal 1 deben ser iguales a las filas del canal 2")

    resultado = [[0.0] * m2 for _ in range(n1)]

    for i in range(n1):
        for j in range(m2):
            for k in range(m1):
                resultado[i][j] += canal1[i][k] * canal2[k][j]

    return resultado

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


def entropia(valores):
    h = 0
    for p in valores:
        if p > 0:
            h = h - p * math.log2(p)
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

    return math.log2(utiles)


def capacidad_sin_ruido(canal):
    # C = log2(n)
    n = len(canal)
    return math.log2(n)



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
              " I =", round(mejor_info, 6))

        desde = mejor_p - paso
        hasta = mejor_p + paso
        paso = paso / 10
        if desde < 0:
            desde = 0
        if hasta > 1:
            hasta = 1

    return mejor_p, mejor_info


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
        print(f"  Error detectado en fila {i+1}, columna {j+1} -> corregido")
        matriz[i][j] = 1 - matriz[i][j]  
    else:
        print("  Errores que no se pueden corregir")
        return "", ""

    
    cadena_corregida = ""
    for fila in matriz:
        for bit in fila:
            cadena_corregida += str(bit)

    texto = ""
    for i in range(filas):
        codigo = bits_a_byte(matriz[i])
        texto += chr(codigo)

    return cadena_corregida, texto


if __name__ == "__main__":
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

    print("\n--- CANAL SIN RUIDO Y/O DETERMINANTE ---")
    
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

    print("\n--- EQUIVOCACION, PERDIDA E INFORMACION MUTUA ---")
    matriz_sim = matriz_simultaneos(proEntrada, matriz)
    matriz_post = matriz_posteriori(proEntrada, matriz, proSalida)

    print("Equivocacion (H(A/B)): ", equivocacion(matriz_sim, matriz_post))
    print("Perdida (H(B/A)): ", perdida(matriz_sim, matriz))
    print("Informacion mutua (I(A;B)): ", informacion_mutua_sim(matriz_sim, proEntrada, proSalida))

    print("\n--- REDUCCION DE CANAL ---")
    canal_reducido = reducir_todo(matriz)

    print("\n--- CAPACIDAD DEL CANAL ---")
    tipos = tipos_de_canal(canal_reducido)
    
    if len(tipos) > 0:
        print("  Cumple los tipos:", tipos)
        for tipo in tipos:
            c = capacidad_por_tipo(canal_reducido, tipo)
            print("  Capacidad como", tipo, ":", round(c, 4), "bits/simbolo")
    else:
        print("  No es sin ruido ni determinante")
        if len(canal_reducido) == 2:
            p, c = capacidad_general(canal_reducido)
            print("  Capacidad:", round(c, 4), "bits/simbolo, con p(x1) =", round(p, 4))
        else:
            print("  Esta busqueda solo esta hecha para canales de 2 entradas")
    print()

    print("\n--- PROBABILIDAD DE ERROR ---")
    decision = decision_maxima(matriz)
    
    print("Regla de decision (salida -> entrada decidida):")
    for j in range(len(decision)):
        print("  b" + str(j + 1), "->", "a" + str(decision[j] + 1))
    
    pe = probabilidad_error(proEntrada, matriz)
    print("Probabilidad de error:", pe)

    print("\n--- DETECTAR Y CORREGIR ERRORES ---")
    # 10100000101011101001111110011001 lo paso a matriz
    matriz_errores = []
    for i in range(0, len(cadenaEntrada), 8):
        bloque = cadenaEntrada[i:i+8]
        matriz_errores.append(int(bloque, 2))

    cadena_corr, texto = recuperar_mensaje(matriz_errores)

    print("Cadena de entrada original: ", cadenaEntrada)
    print("Cadena de entrada corregida:", cadena_corr)