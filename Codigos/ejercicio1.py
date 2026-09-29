import math
import random
from math import log2

# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
CADENA_4 = "-+-+*//++///*/-////+---////-+/+--+-+/-/+-+/-+*++//"  # Ingresa cadena 
N_4 = 20        # longitud de la nueva cadena a generar
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

def multiplicar_matriz_por_vector(matriz, vector):
   
    n = len(vector)
    vector_resultado = [0.0] * n
    
    for fila in range(n):
        suma_probabilidades = 0.0
        
        for columna in range(n):
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

def tipo_de_memoria(matriz, tolerancia):
    n = len(matriz)
    for i in range(n):
        fila = matriz[i]
        if max(fila) - min(fila) > tolerancia:
            return True
    return False

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


cadena = CADENA_4

listaALF = []
listaPro = []
listas_paralelas(cadena, listaALF, listaPro)
print("Alfabeto", listaALF)
print("Lista Probabilidades: ", listaPro) # si la fuente es de memoria la probabilidad de cada evento acá

matriz = []
obtener_matriz(cadena, listaALF, matriz)

tolerancia = 0.01
if (tipo_de_memoria(matriz, tolerancia)):
    print("Es una fuente con memoria (VER TOLERANCIA)")
else:
    print("Es una fuente de memoria nula (VER TOLERANCIA)")

vector = vector_estacionario(matriz)
# En el caso que sea una fuente sin memoria la funcion vector_estacionario calcularia el vector de probabilidades de la fuente, asi que no hace falta calcualr la entropia de manera distinta
print("Entropia: ", obtener_entropia_matriz(matriz, vector))
imprimir_matriz(matriz, listaALF)

if(tipo_de_memoria(matriz, tolerancia)):
    print("Vector estacionario: ", vector)
else:
    nuevoAlf = []
    nuevoPro = []
    listaInfo = []
    extension_fuente(listaALF, listaPro, 2, nuevoAlf, nuevoPro)
    print("Nuevo alfabeto:", nuevoAlf)
    print("Nuevas probabilidades:", nuevoPro)
    generar_lista_info_simple(nuevoPro, listaInfo)
    entropia = entropia_simple(nuevoPro, listaInfo)
    print("Entropia  N . H(S): ", entropia)
    
