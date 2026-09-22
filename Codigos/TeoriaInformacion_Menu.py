"""
==========================================================================
 TEORIA DE LA INFORMACION - MENU UNIFICADO
==========================================================================
Este archivo reune, en un solo script, todos los programas que estaban
sueltos en archivos separados. Cada opcion del menu corresponde a uno de
los archivos originales, con su logica intacta (solo se adaptaron los
valores "hardcodeados" para poder pedirlos por teclado, o se dejaron
como ejemplo por defecto).

Archivos originales integrados:
    1) Entropia.py               -> Entropia de una fuente sin memoria
    2) Entropia_Matriz.py        -> Entropia de una fuente markoviana (con memoria)
    3) Fuente_montecarlo.py      -> Generar cadena aleatoria (Monte Carlo) a partir de una cadena sin memoria
    4) FuenteMatriz_montecarlo.py-> Generar cadena aleatoria (Monte Carlo) a partir de una cadena CON memoria (orden 1)
    5) Secuencia.py              -> Extension de una fuente de orden N
    6) Tipo_codigo.py            -> Analisis de un codigo (Kraft, UD, instantaneo, compacto, etc.)
    7) Wbinario.py               -> Entropia de una fuente binaria con probabilidad w
==========================================================================
"""

import math
import random
from math import log2


# ==========================================================================
# 1) ENTROPIA.PY
#    Calcula la entropia H(X) = sum( p_i * log2(1/p_i) ) de una fuente sin
#    memoria a partir de un vector de probabilidades dado. Trae un ejemplo
#    de 27 simbolos ya cargado, pero tambien se puede ingresar uno propio.
# ==========================================================================
def entropia_simple(lista, listaInfo):
    entropia = 0
    for i, num in enumerate(lista):
        entropia += num * listaInfo[i]
    return entropia


def generar_lista_info_simple(lista, listaInfo):
    for num in lista:
        # Nota original: si la probabilidad es 0, log2(1/0) da error
        # (matematicamente seria infinito), por eso se recomienda no
        # incluir simbolos con probabilidad 0 en esta version.
        listaInfo.append(log2(1 / num))


def menu_entropia_simple():
    print("\n--- ENTROPIA DE UNA FUENTE SIN MEMORIA (Entropia.py) ---")
    ejemplo = [0.125, 0.025, 0.1, 0.025, 0.005000000000000001, 0.020000000000000004,
               0.1, 0.020000000000000004, 0.08000000000000002, 0.025, 0.005000000000000001,
               0.020000000000000004, 0.005000000000000001, 0.0010000000000000002,
               0.004000000000000001, 0.020000000000000004, 0.004000000000000001,
               0.016000000000000004, 0.1, 0.020000000000000004, 0.08000000000000002,
               0.020000000000000004, 0.004000000000000001, 0.016000000000000004,
               0.08000000000000002, 0.016000000000000004, 0.06400000000000002]

    opcion = input("Usar la lista de ejemplo (27 probabilidades) [E] o ingresar la tuya [I]? ").strip().lower()
    if opcion == "i":
        lista = leer_lista_probabilidades()
    else:
        lista = ejemplo

    listaInfo = []
    generar_lista_info_simple(lista, listaInfo)
    print("Probabilidades:", lista)
    print("Informacion I(pi):", listaInfo)
    print("Entropia = ", entropia_simple(lista, listaInfo))


# ==========================================================================
# 2) ENTROPIA_MATRIZ.PY
#    Trabaja con fuentes markovianas (con memoria) representadas por una
#    matriz de transicion. Verifica si la fuente es ergodica, calcula el
#    vector estacionario y a partir de el calcula la entropia de la fuente.
# ==========================================================================
def es_ergodica(M):
    """
    Verifica si la fuente markoviana M es ergodica: comprueba que el
    grafo de transiciones sea fuertemente conexo, es decir, que desde
    cada estado exista un camino (directo o compuesto por varios
    pasos) hacia todos los demas estados, y viceversa.
    """
    n = len(M)
    if n == 0 or any(len(fila) != n for fila in M):
        raise ValueError("La matriz debe ser cuadrada (n x n) y no vacia.")

    directo = [[j for j in range(n) if M[i][j] > 0] for i in range(n)]
    inverso = [[i for i in range(n) if M[i][j] > 0] for j in range(n)]

    def alcanzables(adyacencia, inicio):
        visitados = {inicio}
        pendientes = [inicio]
        while pendientes:
            actual = pendientes.pop()
            for vecino in adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    pendientes.append(vecino)
        return visitados

    return len(alcanzables(directo, 0)) == n and len(alcanzables(inverso, 0)) == n


def vector_estacionario(M):
    """
    Calcula el vector estacionario V* de la fuente markoviana M, mediante
    eliminacion gaussiana con pivoteo parcial, sin librerias externas.
    """
    n = len(M)
    if n == 0 or any(len(fila) != n for fila in M):
        raise ValueError("La matriz debe ser cuadrada (n x n) y no vacia.")

    if not es_ergodica(M):
        raise ValueError(
            "La fuente no es ergodica: no existe un camino que conecte "
            "todos los estados entre si, por lo que no hay un unico "
            "vector estacionario."
        )

    A = [[M[i][j] - (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    aug = [fila[:] + [0.0] for fila in A]
    aug[-1] = [1.0] * n + [1.0]

    for col in range(n):
        fila_pivote = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[fila_pivote][col]) < 1e-12:
            continue
        aug[col], aug[fila_pivote] = aug[fila_pivote], aug[col]

        pivote = aug[col][col]
        aug[col] = [valor / pivote for valor in aug[col]]

        for f in range(n):
            if f != col:
                factor = aug[f][col]
                if factor != 0:
                    aug[f] = [aug[f][k] - factor * aug[col][k] for k in range(n + 1)]

    v = [aug[i][n] for i in range(n)]
    return [0.0 if abs(x) < 1e-12 else x for x in v]


def entropia_matriz_aux(lista, listaInfo):
    entropia = 0
    for i, num in enumerate(lista):
        entropia += num * listaInfo[i]
    return entropia


def generar_lista_info_matriz(lista, listaInfo):
    for num in lista:
        if num != 0:
            listaInfo.append(log2(1 / num))
        else:
            listaInfo.append(0)


def obtener_entropia_matriz(matriz, vector):
    aux = 0
    n = len(matriz)
    for j in range(n):
        vecPro_aux = []
        vecInfo_aux = []
        for i in range(n):
            vecPro_aux.append(matriz[i][j])
        generar_lista_info_matriz(vecPro_aux, vecInfo_aux)
        entropia_j = entropia_matriz_aux(vecPro_aux, vecInfo_aux)
        aux = aux + entropia_j * vector[j]
    return aux


def menu_entropia_matriz():
    print("\n--- ENTROPIA DE UNA FUENTE MARKOVIANA / CON MEMORIA (Entropia_Matriz.py) ---")
    matriz = leer_matriz("Ingrese la matriz de transicion (fila = destino, columna = origen)")

    if es_ergodica(matriz):
        vector = vector_estacionario(matriz)
        print("Vector estacionario:", vector)
        entropia = obtener_entropia_matriz(matriz, vector)
        print("Entropia de la fuente:", entropia)
    else:
        print("La fuente no es ergodica")


# ==========================================================================
# 3) FUENTE_MONTECARLO.PY
#    A partir de una cadena de texto, arma el alfabeto y las probabilidades
#    de cada simbolo (fuente sin memoria) y luego, por el metodo de Monte
#    Carlo, genera una prediccion de "num" simbolos siguiendo esa distribucion.
# ==========================================================================
def listas_paralelas(cadena, listaALF, listaPro):
    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char) / long)

    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0]))

    listaALF.clear()
    listaPro.clear()

    for char, pro in parejas_ordenadas:
        listaALF.append(char)
        listaPro.append(pro)


def montecarlo_fuente(num, listaALF, listaPro, prediccion):
    listaAcum = []
    ant = 0
    for pro in listaPro:
        listaAcum.append(ant + pro)
        ant = ant + pro

    for i in range(num):
        rand = random.random()
        ant = 0
        n = 0
        for j in listaAcum:
            if ant <= rand < j:
                prediccion.append(listaALF[n])
                break
            n = n + 1
            ant = j


def menu_fuente_montecarlo():
    print("\n--- FUENTE SIN MEMORIA + MONTE CARLO (Fuente_montecarlo.py) ---")
    ejemplo = "ABDAACAABACADAABDAADABDAAABDCDCDCDC"
    opcion = input("Usar la cadena de ejemplo [E] o ingresar una propia [I]? ").strip().lower()
    cadena = ejemplo if opcion != "i" else input("Ingrese la cadena: ")

    num = int(input("Cuantos simbolos quiere predecir (num)? "))

    listaALF = []
    listaPro = []
    prediccion = []
    listas_paralelas(cadena, listaALF, listaPro)
    montecarlo_fuente(num, listaALF, listaPro, prediccion)

    print("Cadena:", cadena)
    print("Alfabeto:", listaALF)
    print("Probabilidades:", listaPro)
    print("Prediccion:", prediccion)


# ==========================================================================
# 4) FUENTEMATRIZ_MONTECARLO.PY
#    A partir de una cadena, arma la matriz de transicion de orden 1
#    (fuente CON memoria), indica si la fuente tiene memoria o es de
#    memoria nula, la imprime en forma de tabla y genera una nueva cadena
#    aleatoria siguiendo esa matriz mediante Monte Carlo.
# ==========================================================================
def imprimir_matriz(matriz, alfabeto=None):
    if not matriz:
        print("[]")
        return

    matriz_formateada = [
        [f"{elem:.2f}" if isinstance(elem, float) else str(elem) for elem in fila]
        for fila in matriz
    ]

    ancho_max = max(len(str(elem)) for fila in matriz_formateada for elem in fila)
    if alfabeto:
        ancho_max = max(ancho_max, max(len(str(letra)) for letra in alfabeto))

    num_cols = len(matriz[0])

    if alfabeto:
        encabezado_cols = " ".join([f"{str(col):>{ancho_max}}" for col in alfabeto])
        print(" " * (ancho_max + 3) + "Destino (siguiente)")
        print(" " * (ancho_max + 3) + " " + encabezado_cols)

    print(" " * (ancho_max + 1) + "┌" + " " * (ancho_max * num_cols + num_cols + 1) + "┐")

    for idx, fila in enumerate(matriz_formateada):
        elementos = [f"{elem:>{ancho_max}}" for elem in fila]
        etiqueta_fila = f"{str(alfabeto[idx]):>{ancho_max}} │ " if alfabeto else "│ "
        print(etiqueta_fila + " ".join(elementos) + " │")

    print(" " * (ancho_max + 1) + "└" + " " * (ancho_max * num_cols + num_cols + 1) + "┘")


def obtener_matriz(cadena, listaALF, matriz):
    """
    matriz[i][j] = P(siguiente = listaALF[i] | actual = listaALF[j])
    Fila = simbolo siguiente (destino), Columna = simbolo actual (origen).
    Cada columna suma 1.
    """
    n = len(listaALF)
    conteo = [[0] * n for _ in range(n)]
    total_desde = [0] * n

    for k in range(len(cadena) - 1):
        actual = cadena[k]
        siguiente = cadena[k + 1]

        col = listaALF.index(actual)
        fila = listaALF.index(siguiente)

        conteo[fila][col] += 1
        total_desde[col] += 1

    matriz.clear()
    for i in range(n):
        matriz.append([0] * n)

    for j in range(n):
        for i in range(n):
            if total_desde[j] > 0:
                matriz[i][j] = conteo[i][j] / total_desde[j]
            else:
                matriz[i][j] = 0


def montecarlo_matriz(listaALF, matriz, n):
    cadena = ''
    act = random.choice(listaALF)
    cadena += act

    for i in range(n - 1):
        act_j = listaALF.index(act)

        ant = 0
        listaAcum = []
        for fila in range(len(matriz)):
            ant = ant + matriz[fila][act_j]
            listaAcum.append(ant)

        rand = random.random()
        ant = 0
        siguiente = act  # por seguridad

        for j in range(len(listaAcum)):
            aux = listaAcum[j]
            if ant <= rand < aux:
                siguiente = listaALF[j]
                break
            ant = aux

        cadena += siguiente
        act = siguiente

    return cadena


def tipo_de_memoria(matriz, tolerancia):
    n = len(matriz)
    for i in range(n):
        fila = matriz[i]
        if max(fila) - min(fila) > tolerancia:
            print("Es una fuente con memoria (NO HACER MUCHO CASO)")
            return
    print("Es una fuente de memoria nula (NO HACER MUCHO CASO)")


def menu_fuente_matriz_montecarlo():
    print("\n--- FUENTE CON MEMORIA (MATRIZ) + MONTE CARLO (FuenteMatriz_montecarlo.py) ---")
    cadena = input("Ingrese la cadena de entrenamiento: ")

    listaALF = []
    listaPro = []
    listas_paralelas(cadena, listaALF, listaPro)
    print("Alfabeto:", listaALF)

    matriz = []
    obtener_matriz(cadena, listaALF, matriz)

    tolerancia = 0.2
    tipo_de_memoria(matriz, tolerancia)
    print("-------------------")
    imprimir_matriz(matriz, listaALF)
    print("-----MATRIZ PARA COPIAR-----")
    print(matriz)

    n = int(input("Longitud de la nueva cadena a generar: "))
    nueva_cadena = montecarlo_matriz(listaALF, matriz, n)
    print("Nueva cadena:", nueva_cadena)


# ==========================================================================
# 5) SECUENCIA.PY
#    Calcula la extension de orden N de una fuente: genera todas las
#    combinaciones posibles de N simbolos del alfabeto original junto con
#    sus probabilidades (producto de las probabilidades individuales).
# ==========================================================================
def extension_fuente(alfabeto, distribucion, N, nuevoAlfabeto, nuevaDistribucion):
    alf = ['']
    pro = [1]

    for x in range(N):
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


def menu_secuencia():
    print("\n--- EXTENSION DE UNA FUENTE DE ORDEN N (Secuencia.py) ---")
    opcion = input("Usar el ejemplo (alfabeto x,y,z) [E] o ingresar el tuyo [I]? ").strip().lower()
    if opcion == "i":
        listaAlf = input("Ingrese el alfabeto separado por comas (ej: a,b,c): ").split(",")
        listaAlf = [s.strip() for s in listaAlf]
        listaPro = leer_lista_probabilidades()
        num = int(input("Ingrese el orden N de la extension: "))
    else:
        listaAlf = ['x', 'y', 'z']
        listaPro = [0.5, 0.1, 0.4]
        num = 3

    nuevoAlf = []
    nuevoPro = []
    extension_fuente(listaAlf, listaPro, num, nuevoAlf, nuevoPro)
    print("Nuevo alfabeto:", nuevoAlf)
    print("Nuevas probabilidades:", nuevoPro)


# ==========================================================================
# 6) TIPO_CODIGO.PY
#    Analiza un codigo (lista de palabras-codigo): si es no singular,
#    instantaneo y/o univocamente decodificable, calcula la inecuacion de
#    Kraft, la entropia de la fuente asociada, la longitud media y si el
#    codigo es compacto. Al final genera una prediccion por Monte Carlo.
# ==========================================================================
def inecuacion_kraft(cod, listaALF):
    r = len(listaALF)
    aux = 0
    for x in cod:
        aux += r ** -len(x)
    return aux


def listas_tipo_codigo(cod, listaALF, listaLong):
    for x in cod:
        listaLong.append(len(x))
        for ch in x:
            if ch not in listaALF:
                listaALF.append(ch)


def nosingular(cod):
    return len(cod) == len(set(cod))


def instantaneo(cod):
    if nosingular(cod):
        for i in range(len(cod)):
            for j in range(len(cod)):
                if i != j:
                    if cod[i].startswith(cod[j]):
                        return False
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

            if not S_siguiente:
                return True

            if S_siguiente & C:
                return False

            if S_siguiente in conjuntos_vistos:
                return True

            conjuntos_vistos.append(S_siguiente)
            S_i = S_siguiente
    return False


def long_media(listaPro, listaLong):
    aux = 0
    for i in range(len(listaPro)):
        aux += listaPro[i] * listaLong[i]
    return aux


def entropia_tipo_codigo(lista, listaInfo):
    entropia = 0
    for i, num in enumerate(lista):
        entropia += num * listaInfo[i]
    return entropia


def generar_lista_info_tipo_codigo(lista, listaInfo, listaALF):
    r = len(listaALF)
    print("I(Pi): ")
    for num in lista:
        valor = math.log(1 / num, r)
        listaInfo.append(valor)
        print("I(", num, ") = ", valor)


def compacto(cod, listaInfo, listaLong):
    if univocamente_decodificable(cod):
        for i in range(len(listaInfo)):
            if math.ceil(listaInfo[i]) < listaLong[i]:
                return False
        return True
    return False


def montecarlo_tipo_codigo(num, cod, listaPro, prediccion):
    listaAcum = []
    ant = 0
    for pro in listaPro:
        listaAcum.append(ant + pro)
        ant = ant + pro

    for i in range(num):
        rand = random.random()
        ant = 0
        n = 0
        for j in listaAcum:
            if ant <= rand < j:
                prediccion.append(cod[n])
                break
            n = n + 1
            ant = j


def menu_tipo_codigo():
    print("\n--- ANALISIS DE UN CODIGO (Tipo_codigo.py) ---")
    cod = input("Ingrese las palabras-codigo separadas por comas (ej: 0,10,110,111): ").split(",")
    cod = [s.strip() for s in cod]
    print("Codigo:", cod)

    if nosingular(cod):
        print("Es No Singular")
        if instantaneo(cod):
            print("Es Univocamente Decodificable")
            print("Es Instantaneo")
        else:
            if univocamente_decodificable(cod):
                print("Es Univocamente Decodificable")
            else:
                print("No es Univocamente Decodificable")
            print("No es Instantaneo")
    else:
        print("Es Singular")

    listaALF = []
    listaLong = []
    listas_tipo_codigo(cod, listaALF, listaLong)
    print("Lista alfabeto:", listaALF)
    print("Lista Li:", listaLong)

    kraft = inecuacion_kraft(cod, listaALF)
    print("Kraft:", kraft)

    if univocamente_decodificable(cod):
        usar_pro = input("Ingresar las probabilidades de cada palabra-codigo para calcular entropia/long. media/compacidad? (s/n) ").strip().lower()
        if usar_pro == "s":
            print(f"Ingrese {len(cod)} probabilidades (deben sumar 1), una por linea:")
            listaPro = [float(input(f"  p[{i}]: ")) for i in range(len(cod))]

            listaInfo = []
            generar_lista_info_tipo_codigo(listaPro, listaInfo, listaALF)
            entropia = entropia_tipo_codigo(listaPro, listaInfo)
            print("Entropia de la Fuente:", entropia)

            L_media = long_media(listaPro, listaLong)
            print("Longitud media:", L_media)

            if compacto(cod, listaInfo, listaLong):
                print("Es Compacto")
            else:
                print("No es Compacto")

            usar_mc = input("Generar una prediccion por Monte Carlo? (s/n) ").strip().lower()
            if usar_mc == "s":
                n = int(input("Cuantos simbolos predecir? "))
                prediccion = []
                montecarlo_tipo_codigo(n, cod, listaPro, prediccion)
                print("Prediccion:", prediccion)


# ==========================================================================
# 7) WBINARIO.PY
#    Calcula la entropia de una fuente binaria con probabilidades w y 1-w.
# ==========================================================================
def menu_wbinario():
    print("\n--- ENTROPIA DE UNA FUENTE BINARIA (Wbinario.py) ---")
    w = float(input("Escriba el valor de w (entre 0 y 1): "))
    listaPro = [w, 1 - w]
    listaInfo = []
    generar_lista_info_simple(listaPro, listaInfo)
    print(listaPro)
    print(listaInfo)
    print("La entropia es = ", entropia_simple(listaPro, listaInfo))


# ==========================================================================
# UTILIDADES DE ENTRADA DE DATOS
# ==========================================================================
def leer_lista_probabilidades():
    n = int(input("Cuantas probabilidades va a ingresar? "))
    lista = []
    for i in range(n):
        lista.append(float(input(f"  p[{i}]: ")))
    return lista


def leer_matriz(titulo="Ingrese la matriz"):
    print(titulo)
    n = int(input("Tamaño de la matriz (n x n), ingrese n: "))
    matriz = []
    print("Ingrese cada fila con sus valores separados por comas (ej: 0.2,0.5,0.3)")
    for i in range(n):
        fila = input(f"  Fila {i}: ").split(",")
        matriz.append([float(x.strip()) for x in fila])
    return matriz


# ==========================================================================
# MENU PRINCIPAL
# ==========================================================================
DESCRIPCIONES = {
    "1": "Entropia de una fuente SIN memoria: dado un vector de probabilidades,"
         " calcula H(X) = sum(p_i * log2(1/p_i)).",
    "2": "Entropia de una fuente CON memoria (markoviana): a partir de una matriz"
         " de transicion, verifica si es ergodica, calcula el vector estacionario"
         " y con eso la entropia de la fuente.",
    "3": "Fuente sin memoria + Monte Carlo: a partir de una cadena de texto arma"
         " el alfabeto y sus probabilidades, y genera una prediccion aleatoria de"
         " simbolos siguiendo esa distribucion.",
    "4": "Fuente con memoria (matriz) + Monte Carlo: a partir de una cadena arma"
         " la matriz de transicion de orden 1, dice si tiene memoria o no, la"
         " imprime, y genera una nueva cadena aleatoria siguiendola.",
    "5": "Extension de una fuente de orden N: genera todas las combinaciones de N"
         " simbolos del alfabeto original junto con sus probabilidades.",
    "6": "Analisis de un codigo: verifica si es no singular, instantaneo y/o"
         " univocamente decodificable, calcula la inecuacion de Kraft, entropia,"
         " longitud media, si es compacto, y permite generar una prediccion.",
    "7": "Entropia de una fuente binaria con probabilidad w y 1-w.",
}

OPCIONES = {
    "1": menu_entropia_simple,
    "2": menu_entropia_matriz,
    "3": menu_fuente_montecarlo,
    "4": menu_fuente_matriz_montecarlo,
    "5": menu_secuencia,
    "6": menu_tipo_codigo,
    "7": menu_wbinario,
}


def mostrar_menu():
    print("\n==========================================================")
    print(" MENU - TEORIA DE LA INFORMACION")
    print("==========================================================")
    print(" 1) Entropia de una fuente sin memoria")
    print(" 2) Entropia de una fuente con memoria (matriz / markoviana)")
    print(" 3) Fuente sin memoria + Monte Carlo")
    print(" 4) Fuente con memoria (matriz) + Monte Carlo")
    print(" 5) Extension de una fuente de orden N")
    print(" 6) Analisis de un codigo (Kraft, UD, instantaneo, compacto...)")
    print(" 7) Entropia de una fuente binaria (w, 1-w)")
    print(" d) Ver descripcion de una opcion")
    print(" 0) Salir")
    print("==========================================================")


def main():
    while True:
        mostrar_menu()
        eleccion = input("Elija una opcion: ").strip().lower()

        if eleccion == "0":
            print("Saliendo...")
            break
        elif eleccion == "d":
            sub = input("De que opcion (1-7) quiere ver la descripcion? ").strip()
            print(DESCRIPCIONES.get(sub, "Opcion invalida."))
        elif eleccion in OPCIONES:
            try:
                OPCIONES[eleccion]()
            except Exception as e:
                print("Ocurrio un error:", e)
        else:
            print("Opcion invalida, intente de nuevo.")


if __name__ == "__main__":
    main()
