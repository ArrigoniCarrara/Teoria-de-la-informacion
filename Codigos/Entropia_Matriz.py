from math import log2
 
def es_ergodica(M):
    """
    Verifica si la fuente markoviana M es ergódica: comprueba que el
    grafo de transiciones sea fuertemente conexo, es decir, que desde
    cada estado exista un camino (directo o compuesto por varios
    pasos) hacia todos los demás estados, y viceversa.
 
    M debe ser cuadrada (n x n) de cualquier tamaño.
    """
    n = len(M)
    if n == 0 or any(len(fila) != n for fila in M):
        raise ValueError("La matriz debe ser cuadrada (n x n) y no vacía.")
 
    # Grafo directo: i -> j si M[i][j] > 0. Grafo inverso: j -> i.
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
 
    # El grafo es fuertemente conexo si desde el estado 0 se alcanzan
    # todos los demás (grafo directo) y todos los demás alcanzan al
    # estado 0 (equivale a recorrer el grafo inverso desde el 0).
    return len(alcanzables(directo, 0)) == n and len(alcanzables(inverso, 0)) == n
 
 
def vector_estacionario(M):
    """
    Calcula el vector estacionario V* de la fuente markoviana M (con
    la convención tradicional: filas = estado actual, columnas =
    estado siguiente, filas suman 1).
 
    Primero verifica que la fuente sea ergódica; si no lo es, no existe
    un único vector estacionario y se lanza un error. Si lo es, resuelve:
 
        V* = V* · M     =>     (Mᵀ - I) · V* = 0     con   sum(V*) = 1
 
    mediante eliminación gaussiana con pivoteo parcial, sin librerías
    externas. Devuelve V* como lista de floats. Funciona para M de
    cualquier tamaño n x n.
    """
    n = len(M)
    if n == 0 or any(len(fila) != n for fila in M):
        raise ValueError("La matriz debe ser cuadrada (n x n) y no vacía.")
 
    if not es_ergodica(M):
        raise ValueError(
            "La fuente no es ergódica: no existe un camino que conecte "
            "todos los estados entre sí, por lo que no hay un único "
            "vector estacionario."
        )
 
    
    A = [[M[i][j] - (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
 
    aug = [fila[:] + [0.0] for fila in A]
    aug[-1] = [1.0] * n + [1.0]
 
    # Eliminación gaussiana con pivoteo parcial
    for col in range(n):
        fila_pivote = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[fila_pivote][col]) < 1e-12:
            continue  # columna aún dependiente, se sigue con la próxima
        aug[col], aug[fila_pivote] = aug[fila_pivote], aug[col]
 
        pivote = aug[col][col]
        aug[col] = [valor / pivote for valor in aug[col]]
 
        for f in range(n):
            if f != col:
                factor = aug[f][col]
                if factor != 0:
                    aug[f] = [aug[f][k] - factor * aug[col][k] for k in range(n + 1)]
 
    v = [aug[i][n] for i in range(n)]
    return [0.0 if abs(x) < 1e-12 else x for x in v]  # limpia -0.0 y ruido numérico
 

def Entropia(lista, listaInfo):

    i = 0
    entropia = 0
    for num in lista:
        entropia += num * listaInfo[i]
        i = i + 1
    return entropia


def Generolista (lista, listaInfo):

    for num in lista:
        if (num != 0):
         listaInfo.append(log2(1/num))
        else:
            listaInfo.append(0)


def obtener_entropia(matriz, vector):
    aux = 0
    n = len(matriz)
    for j in range(n):  
        vecPro_aux = []
        vecInfo_aux = []
        for i in range(n):
            vecPro_aux.append(matriz[i][j])  
        Generolista(vecPro_aux, vecInfo_aux)
        entropia_j = Entropia(vecPro_aux, vecInfo_aux)
        aux = aux + entropia_j * vector[j]
    return aux


 
matriz =[] # Ingrese Matriz

if es_ergodica(matriz):
    vector = []
    vector = vector_estacionario(matriz)
    print(vector)
    entropia = obtener_entropia(matriz, vector) 
    print(entropia)
else:
    print("La fuente no es ergodica")