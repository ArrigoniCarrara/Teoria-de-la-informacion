from Fuente_montecarlo import Listasparalelas
import random
from Entropia_Matriz import Entropia

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


def ObtenerMatriz(cadena, listaALF, matriz):
    """
    Recibe una cadena y un listaALF YA CALCULADO, y completa matriz con la
    matriz de transición de orden 1, con la convención de la cátedra:
    
    matriz[i][j] = P(siguiente = listaALF[i] | actual = listaALF[j])
    
    Es decir: la COLUMNA j representa el símbolo actual (origen),
    la FILA i representa el símbolo siguiente (destino),
    y cada COLUMNA suma 1.
    """
    n = len(listaALF)

    # conteo[i][j] = veces que, estando en el símbolo j, se pasó al símbolo i
    conteo = [[0] * n for _ in range(n)]

    # cantidad de veces que cada símbolo aparece "como origen" (columna)
    total_desde = [0] * n

    for k in range(len(cadena) - 1):
        actual = cadena[k]
        siguiente = cadena[k + 1]

        col = listaALF.index(actual)      # símbolo actual -> columna
        fila = listaALF.index(siguiente)  # símbolo siguiente -> fila

        conteo[fila][col] += 1
        total_desde[col] += 1

    # Normalizamos por columna
    matriz.clear()
    for i in range(n):
        matriz.append([0] * n)

    for j in range(n):
        for i in range(n):
            if total_desde[j] > 0:
                matriz[i][j] = conteo[i][j] / total_desde[j]
            else:
                matriz[i][j] = 0


def Montecarlo(listaALF, matriz, n):
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

        for j in range(len(listaAcum)):
            aux = listaAcum[j]
            if ant <= rand < aux:
                siguiente = listaALF[j]
                break
            ant = aux

        cadena += siguiente
        act = siguiente

    return cadena


def TipodeMemoria(matriz, tolerancia):
    n = len(matriz)
    for i in range(n):
        fila = matriz[i]
        if max(fila) - min(fila) > tolerancia:
            print("Es una fuente con memoria (NO HACER MUCHO CASO)")
            return

    print("Es una fuente de memoria nula (NO HACER MUCHO CASO)")


cadena = "" #Ingresa Cadena
listaALF = []
listaPro = []
Listasparalelas(cadena, listaALF, listaPro)
print("Alfabeto", listaALF) 
matriz = []
ObtenerMatriz(cadena, listaALF, matriz)
tolerancia = 0.2
TipodeMemoria(matriz, tolerancia)
print("-------------------") 
imprimir_matriz(matriz, listaALF)
print("-----MATRIZ PARA COPIAR-----")
print(matriz) 
n = 20
cadena = Montecarlo(listaALF, matriz, n)
print("Nueva cadena: ", cadena)