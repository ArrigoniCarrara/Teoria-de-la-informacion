def decision_maxima(canal):
    n = len(canal)
    m = len(canal[0])

    decision = []
    for j in range(m):
        mejor_i = 0
        mejor_valor = canal[0][j]

        for i in range(1, n):
            if canal[i][j] > mejor_valor:
                mejor_valor = canal[i][j]
                mejor_i = i

        decision.append(mejor_i)

    return decision


def probabilidad_error(pa, canal):
    m = len(canal[0])
    decision = decision_maxima(canal)

    p_acierto = 0
    for j in range(m):
        i = decision[j]
        p_conjunta = pa[i] * canal[i][j]
        p_acierto = p_acierto + p_conjunta

    return 1 - p_acierto


if __name__ == "__main__":
    pa = [4/15, 3/15, 8/15]
    canal = [[0.6, 0.3, 0.1],
             [0.1, 0.8, 0.1],
             [0.3, 0.3, 0.4]]

    decision = decision_maxima(canal)

    print("Regla de decision (salida -> entrada decidida):")
    for j in range(len(decision)):
        print("  b" + str(j + 1), "->", "a" + str(decision[j] + 1))

    pe = probabilidad_error(pa, canal)
    print("Probabilidad de error:", round(pe, 4))