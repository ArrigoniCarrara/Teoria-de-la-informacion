import math


def prob_salida(priori, canal):
    # P(b_j) = suma sobre i de P(a_i) * P(b_j | a_i)
    n = len(priori)
    m = len(canal[0])
    salida = [0 for _ in range(m)]
    for j in range(m):
        for i in range(n):
            salida[j] += priori[i] * canal[i][j]
    return salida


def matriz_posteriori(priori, canal, salida):
    # P(a_i | b_j) = P(b_j | a_i) * P(a_i) / P(b_j)
    n = len(priori)
    m = len(salida)
    post = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            post[i][j] = canal[i][j] * priori[i] / salida[j]
    return post


def matriz_simultaneos(priori, canal):
    # P(a_i, b_j) = P(a_i) * P(b_j | a_i)
    n = len(priori)
    m = len(canal[0])
    sim = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            sim[i][j] = priori[i] * canal[i][j]
    return sim


def entropia_apriori(priori):
    # H(A) = suma sobre i de P(a_i) * log2(1 / P(a_i))
    h = 0
    for p in priori:
        if p > 0:
            h += p * math.log2(1 / p)
    return h


def entropias_aposteriori(post):
    # H(A/b_j) = suma sobre i de P(a_i | b_j) * log2(1 / P(a_i | b_j))
    # Devuelve una lista con un valor por cada símbolo de salida b_j
    n = len(post)
    m = len(post[0])
    h = [0 for _ in range(m)]
    for j in range(m):
        for i in range(n):
            p = post[i][j]
            if p > 0:
                h[j] += p * math.log2(1 / p)
    return h


def mostrar(nombre, mat):
    print(nombre)
    for fila in mat:
        print([round(x, 4) for x in fila])


if __name__ == "__main__":
    priori = [0.4411764705882353, 0.5588235294117647]
    canal = [[0.4, 0.6], [0.2631578947368421, 0.7368421052631579]]

    assert len(priori) == len(canal), "priori y canal deben tener la misma cantidad de filas"

    salida = prob_salida(priori, canal)
    posteriori = matriz_posteriori(priori, canal, salida)
    simultaneos = matriz_simultaneos(priori, canal)

    print("P(salida):", [round(x, 4) for x in salida])
    mostrar("Posteriori P(A|B):", posteriori)
    mostrar("Simultáneos P(A,B):", simultaneos)

    hA = entropia_apriori(priori)
    hAb = entropias_aposteriori(posteriori)

    print("H(A) =", round(hA, 4), "bits")
    for j in range(len(hAb)):
        print("H(A/b" + str(j + 1) + ") =", round(hAb[j], 4), "bits")