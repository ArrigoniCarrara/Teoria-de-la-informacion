from math import log2

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

# Huffman es óptimo: ningún código libre de prefijo tiene menor longitud media L. 
# Si hay empates, puede dar códigos distintos según el orden, pero el mismo L.
def huffman(probs):
    items = [[p, ""] for p in probs]
    codificar(sorted(items))
    return [code for _, code in items]

def codificar(items):
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
    codificar(items[2:] + [nuevo])

    # Al volver, el nodo combinado ya tiene su código:
    # los dos nodos que lo formaron lo extienden con 0 y 1
    a[1] = nuevo[1] + "0"
    b[1] = nuevo[1] + "1"

def metricas(probs, codigos):
    h = -sum(p * log2(p) for p in probs)                  # entropía
    l = sum(p * len(c) for p, c in zip(probs, codigos))   # longitud media
    n = h / l                                           # eficiencia
    return h, l, n, 1 - n

if __name__ == "__main__":
    cadena = "58784784525368669895745123656253698989656452121702300223659"
    listaALF = []
    pro = []

    listas_paralelas(cadena, listaALF, pro)
    codigo = huffman(pro)

    print(f"{'Símbolo':<8} {'Prob.':<10} Código") #Imprime SIMBOLO PROBABILIDAD CODIGO
    for s, p, c in zip(listaALF, pro, codigo):
        print(f"{s:<8} {p:<10.4f} {c}")

    h, l, n, r = metricas(pro, codigo)
    print(f"H(S) = {h} bits")
    print(f"L = {l} bits")
    print(f"n = {n}")
    print(f"R = {r}")