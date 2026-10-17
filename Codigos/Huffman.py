from math import log2

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
    H = -sum(p * log2(p) for p in probs)                  # entropía
    L = sum(p * len(c) for p, c in zip(probs, codigos))   # longitud media
    eta = H / L                                           # eficiencia
    return H, L, eta, 1 - eta                             # redundancia = 1 - eta

if __name__ == "__main__":
    pro = [0.20, 0.27, 0.40, 0.13]
    codigo = huffman(pro)
    for p, c in zip(pro, codigo):
        print(f"{p:.2f} -> {c}")

    H, L, eta, R = metricas(pro, codigo)
    print(f"H(S) = {H:.2f} bits")
    print(f"L = {L:.2f} bits")
    print(f"η = {eta:.4f}")
    print(f"R = {R:.4f}")