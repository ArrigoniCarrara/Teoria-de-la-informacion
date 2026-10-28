def compuesto(canal1, n1, m1, canal2, n2, m2):
    if m1 != n2:
        print("Las columnas del canal 1 deben ser iguales a las filas del canal 2")
    resultado = [[0.0] * m2 for _ in range(n1)]
    for i in range(n1):
        for j in range(m2):
            for k in range(m1):
                resultado[i][j] += canal1[i][k] * canal2[k][j]
    return resultado


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


if __name__ == "__main__":
    canal = [[0.2, 0.3, 0.5],
             [0.0, 0.0, 1.0],
             [0.0, 0.0, 1.0]]

    reducir_todo(canal)