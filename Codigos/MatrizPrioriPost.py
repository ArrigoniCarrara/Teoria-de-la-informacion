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
    # H(A) = suma de P(a) * log2(1 / P(a))
    h = 0
    for p in priori:
        if p > 0:
            h += p * math.log2(1 / p)
    return h


def entropias_aposteriori(post):
    # H(A/b_j) = suma sobre i de P(a_i | b_j) * log2(1 / P(a_i | b_j))
    n = len(post)
    m = len(post[0])
    h = [0 for _ in range(m)]
    for j in range(m):
        for i in range(n):
            p = post[i][j]
            if p > 0:
                h[j] += p * math.log2(1 / p)
    return h


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


def entropia_afin(sim):
    # H(A,B) = suma de P(a,b) * log2(1 / P(a,b))
    n = len(sim)
    m = len(sim[0])
    h = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                h += sim[i][j] * math.log2(1 / sim[i][j])
    return h


def informacion_mutua(sim, priori, salida):
    # I(A,B) = suma de P(a,b) * log2( P(a,b) / (P(a) * P(b)) )
    n = len(sim)
    m = len(sim[0])
    info = 0
    for i in range(n):
        for j in range(m):
            if sim[i][j] > 0:
                info += sim[i][j] * math.log2(sim[i][j] / (priori[i] * salida[j]))
    return info

def entropia_salida(salida):
    # H(B) = suma de P(b) * log2(1 / P(b))
    h = 0
    for p in salida:
        if p > 0:
            h += p * math.log2(1 / p)
    return h

def mostrar(nombre, mat):
    print(nombre)
    for fila in mat:
        print([round(x, 4) for x in fila])


if __name__ == "__main__":
    priori = [0.12, 0.24, 0.14, 0.50]
    canal = [[0.25, 0.15, 0.30, 0.30],
             [0.23, 0.27, 0.25, 0.25],
             [0.10, 0.40, 0.25, 0.25],
             [0.34, 0.26, 0.20, 0.20]]

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

    hB = entropia_salida(salida)
    print("H(B) =", round(hB, 4), "bits")
    print("Equivocación H(A/B) =", round(equivocacion(simultaneos, posteriori), 4), "bits")
    print("Pérdida H(B/A) =", round(perdida(simultaneos, canal), 4), "bits")
    print("Entropía afín H(A,B) =", round(entropia_afin(simultaneos), 4), "bits")
    print("Información mutua I(A,B) =", round(informacion_mutua(simultaneos, priori, salida), 4), "bits")