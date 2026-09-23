"""
==========================================================================
 TEORIA DE LA INFORMACION - MENU UNIFICADO (VALORES HARDCODEADOS)
==========================================================================
Pensado para examen: cada modulo tiene, mas abajo, un bloque de
"DATOS DE ENTRADA" con variables hardcodeadas (como en los scripts
originales). Antes de ejecutar, edita el bloque del modulo que vayas a
usar y despues elegi el numero correspondiente en el menu de la consola.

No hay input() para cargar datos (salvo para elegir la opcion del menu):
todo se carga modificando las variables de cada bloque.

Modulos:
    1) Entropia.py               -> Entropia de una fuente sin memoria
    2) Entropia_Matriz.py        -> Entropia de una fuente markoviana (con memoria)
    3) Fuente_montecarlo.py      -> Monte Carlo a partir de una cadena sin memoria
    4) FuenteMatriz_montecarlo.py-> Monte Carlo a partir de una cadena CON memoria (orden 1)
    5) Secuencia.py              -> Extension de una fuente de orden N
    6) Tipo_codigo.py            -> Analisis de un codigo (Kraft, UD, instantaneo, compacto...)
    7) Wbinario.py               -> Entropia de una fuente binaria con probabilidad w
==========================================================================
"""

import math
import random
from math import log2


# ==========================================================================
# 1) ENTROPIA.PY - Entropia de una fuente SIN memoria
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
LISTA_1 = []
# ---------------------------------------------------------------------------


def entropia_simple(lista, listaInfo):
    entropia = 0
    for i, num in enumerate(lista):
        entropia += num * listaInfo[i]
    return entropia


def generar_lista_info_simple(lista, listaInfo):
    for num in lista:
        if(num != 0):
            listaInfo.append(log2(1 / num))
        else:
            listaInfo.append(0)


def menu_entropia_simple():
    print("\n--- ENTROPIA DE UNA FUENTE SIN MEMORIA (Entropia.py) ---")
    lista = LISTA_1
    listaInfo = []
    generar_lista_info_simple(lista, listaInfo)
    print("Probabilidades:", lista)
    print("Informacion I(pi):", listaInfo)
    print("Entropia = ", entropia_simple(lista, listaInfo))


# ==========================================================================
# 2) ENTROPIA_MATRIZ.PY - Entropia de una fuente CON memoria (markoviana)
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
# matriz[i][j] = P(siguiente = i | actual = j)  -> cada COLUMNA suma 1
MATRIZ_2 = []  # Ejemplo: [[0.5, 0.3], [0.5, 0.7]]
# ---------------------------------------------------------------------------


def multiplicar_matriz_por_vector(matriz, vector):
   
    n = len(vector)
    vector_resultado = [0.0] * n
    
    for fila in range(n):
        suma_probabilidades = 0.0
        
        for columna in range(n):
            # Cambiamos el orden geométrico de la multiplicación
            suma_probabilidades += matriz[fila][columna] * vector[columna]
            
        vector_resultado[fila] = suma_probabilidades
        
    return vector_resultado


def vector_estacionario(matriz_transicion, tolerancia=0.001):

    cantidad_estados = len(matriz_transicion)
    vector_actual = [1.0 / cantidad_estados] * cantidad_estados
    
    while True:
        vector_siguiente = multiplicar_matriz_por_vector(matriz_transicion, vector_actual)
        
        se_estabilizo = True
        for i in range(cantidad_estados):
            diferencia = abs(vector_siguiente[i] - vector_actual[i])
            
            if diferencia >= tolerancia:
                se_estabilizo = False
                break
                
        if se_estabilizo:
            return vector_siguiente
            
        vector_actual = vector_siguiente

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
    matriz = MATRIZ_2
    

    
    vector = vector_estacionario(matriz)
    print("Vector estacionario:", vector)
    entropia = obtener_entropia_matriz(matriz, vector)
    print("Entropia de la fuente:", entropia)
    
        


# ==========================================================================
# 3) FUENTE_MONTECARLO.PY - Fuente sin memoria + Monte Carlo
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
CADENA_3 = ""
NUM_3 = 5  # cantidad de simbolos a predecir
# ---------------------------------------------------------------------------


def listas_paralelas(cadena, listaALF, listaPro):
    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char) / long)

    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0])) # Ordeno los eventos para mayor comodidad (en el orden que corresponda)

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
    cadena = CADENA_3
    num = NUM_3
    listaInfo = []
    listaALF = []
    listaPro = []
    prediccion = []
    listas_paralelas(cadena, listaALF, listaPro)
    # Si es una cadena de caracteres con probabilidades ya generadas escribir listaPRO aca abajo
    generar_lista_info_simple(listaPro, listaInfo)
    entropia = entropia_simple(listaPro, listaInfo)
    montecarlo_fuente(num, listaALF, listaPro, prediccion)

    print("Cadena:", cadena)
    print("Alfabeto:", listaALF)
    print("Probabilidades:", listaPro)
    print("Cantidad de informacion (I(i)): ", listaInfo)
    print("Entropia H(S): ", entropia)
    print("Prediccion:", prediccion)


# ==========================================================================
# 4) FUENTEMATRIZ_MONTECARLO.PY - Fuente CON memoria (matriz) + Monte Carlo
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
CADENA_4 = ""  # Ingresa cadena de entrenamiento
N_4 = 20        # longitud de la nueva cadena a generar
# ---------------------------------------------------------------------------


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
            print("Es una fuente con memoria (VER TOLERANCIA)")
            return
    print("Es una fuente de memoria nula (VER TOLERANCIA)")


def menu_fuente_matriz_montecarlo():
    print("\n--- FUENTE CON MEMORIA (MATRIZ) + MONTE CARLO (FuenteMatriz_montecarlo.py) ---")
    cadena = CADENA_4
    if not cadena:
        print("CADENA_4 esta vacia. Cargala en el bloque de datos de entrada arriba.")
        return

    listaALF = []
    listaPro = []
    listas_paralelas(cadena, listaALF, listaPro)
    print("Alfabeto", listaALF)

    matriz = []
    obtener_matriz(cadena, listaALF, matriz)

    tolerancia = 0.01
    tipo_de_memoria(matriz, tolerancia)
    print("-------------------")
    print("Entropia: ", obtener_entropia_matriz(matriz, vector_estacionario(matriz)))
    imprimir_matriz(matriz, listaALF)
    print("-----MATRIZ PARA COPIAR-----")
    print(matriz)

    nueva_cadena = montecarlo_matriz(listaALF, matriz, N_4)
    print("Nueva cadena: ", nueva_cadena)


# ==========================================================================
# 5) SECUENCIA.PY - Extension de una fuente de orden N
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
ALFABETO_5 = []
DISTRIBUCION_5 = []
N_5 = 0
# ---------------------------------------------------------------------------


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
    nuevoAlf = []
    nuevoPro = []
    extension_fuente(ALFABETO_5, DISTRIBUCION_5, N_5, nuevoAlf, nuevoPro)
    print("Nuevo alfabeto:", nuevoAlf)
    print("Nuevas probabilidades:", nuevoPro)


# ==========================================================================
# 6) TIPO_CODIGO.PY - Analisis de un codigo
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
COD_6 = [")", "[]", "]]", "([", "[()]", "([)]"]           # Ingresa Codigo, ej: ["0", "10", "110", "111"]
LISTAPRO_6 = [0.1, 0.50, 0.1, 0.2, 0.05, 0.05]       # Probabilidades de cada palabra-codigo, ej: [0.5, 0.25, 0.125, 0.125]
N_MONTECARLO_6 = 5     # cantidad de simbolos a predecir con Monte Carlo (al final)
# ---------------------------------------------------------------------------


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
    cod = COD_6
    listaPro = LISTAPRO_6
    print(cod)

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
    print("Lista alfabeto: ", listaALF)
    print("Lista Li: ", listaLong)

    kraft = inecuacion_kraft(cod, listaALF)
    print("Kraft: ", kraft)

    if univocamente_decodificable(cod):
        if listaPro:
            listaInfo = []
            generar_lista_info_tipo_codigo(listaPro, listaInfo, listaALF)
            entropia = entropia_tipo_codigo(listaPro, listaInfo)
            print("Entropia de la Fuente: ", entropia)

            L_media = long_media(listaPro, listaLong)
            print("Longitud media: ", L_media)

            if compacto(cod, listaInfo, listaLong):
                print("Es Compacto")
            else:
                print("No es Compacto")

            prediccion = []
            montecarlo_tipo_codigo(N_MONTECARLO_6, cod, listaPro, prediccion)
            print("Prediccion Monte Carlo:", prediccion)
        else:
            print("LISTAPRO_6 esta vacia: cargala en el bloque de datos si queres "
                  "entropia, longitud media, compacidad y Monte Carlo.")


# ==========================================================================
# 7) WBINARIO.PY - Entropia de una fuente binaria (w, 1-w)
# ==========================================================================

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
W_7 = 0
# ---------------------------------------------------------------------------


def menu_wbinario():
    print("\n--- ENTROPIA DE UNA FUENTE BINARIA (Wbinario.py) ---")
    listaPro = [W_7, 1 - W_7]
    listaInfo = []
    generar_lista_info_simple(listaPro, listaInfo)
    print(listaPro)
    print(listaInfo)
    print("La entropia es = ", entropia_simple(listaPro, listaInfo))


# ==========================================================================
# MENU PRINCIPAL
# ==========================================================================
DESCRIPCIONES = {
    "1": "Entropia de una fuente SIN memoria: dado un vector de probabilidades"
         " (variable LISTA_1), calcula H(X) = sum(p_i * log2(1/p_i)).",
    "2": "Entropia de una fuente CON memoria (markoviana): a partir de una matriz"
         " de transicion (variable MATRIZ_2), verifica si es ergodica, calcula el"
         " vector estacionario y con eso la entropia de la fuente.",
    "3": "Fuente sin memoria + Monte Carlo: a partir de una cadena de texto"
         " (CADENA_3) arma el alfabeto y sus probabilidades, y genera NUM_3"
         " simbolos aleatorios siguiendo esa distribucion.",
    "4": "Fuente con memoria (matriz) + Monte Carlo: a partir de una cadena"
         " (CADENA_4) arma la matriz de transicion de orden 1, dice si tiene"
         " memoria o no, la imprime, y genera una cadena nueva de largo N_4.",
    "5": "Extension de una fuente de orden N: usando ALFABETO_5, DISTRIBUCION_5"
         " y N_5, genera todas las combinaciones de N simbolos con sus probabilidades.",
    "6": "Analisis de un codigo (COD_6, LISTAPRO_6): verifica si es no singular,"
         " instantaneo y/o univocamente decodificable, calcula la inecuacion de"
         " Kraft, entropia, longitud media, si es compacto, y una prediccion Monte Carlo.",
    "7": "Entropia de una fuente binaria con probabilidad W_7 y 1-W_7.",
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
    print(" (editar los valores hardcodeados de cada bloque antes de correr)")
    print("==========================================================")
    print(" 1) Entropia de una fuente sin memoria              [LISTA_1]")
    print(" 2) Entropia de una fuente con memoria (matriz)     [MATRIZ_2]")
    print(" 3) Fuente sin memoria + Monte Carlo                [CADENA_3, NUM_3]")
    print(" 4) Fuente con memoria (matriz) + Monte Carlo        [CADENA_4, N_4]")
    print(" 5) Extension de una fuente de orden N               [ALFABETO_5, DISTRIBUCION_5, N_5]")
    print(" 6) Analisis de un codigo                            [COD_6, LISTAPRO_6, N_MONTECARLO_6]")
    print(" 7) Entropia de una fuente binaria (w, 1-w)          [W_7]")
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