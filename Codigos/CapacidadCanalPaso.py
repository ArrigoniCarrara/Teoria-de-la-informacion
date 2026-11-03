from math import log2

def informacion_mutua(canal, pa):
    n = len(canal)
    m = len(canal[0])

    pb = []
    for j in range(m):
        suma = 0
        for i in range(n):
            suma = suma + pa[i] * canal[i][j]
        pb.append(suma)

    info = 0
    for i in range(n):
        for j in range(m):
            if pa[i] > 0 and canal[i][j] > 0:
                info = info + pa[i] * canal[i][j] * log2(canal[i][j] / pb[j])
    return info


def estimar_capacidad(canal, paso):
    # Prueba P(a1) = 0, paso, 2*paso, ... hasta 1 (con P(a2) = 1 - P(a1))
    # y se queda con la que da mayor información mutua
    cantidad = int(1 / paso + 0.0000001)
    mejor_p = 0
    mejor_info = -1

    for k in range(cantidad + 1):
        p = k * paso
        if p > 1:
            p = 1
        info = informacion_mutua(canal, [p, 1 - p])
        if info > mejor_info:
            mejor_info = info
            mejor_p = p

    return mejor_info, mejor_p


if __name__ == "__main__":
    canal = [[0.77, 0.23],
            [0.20, 0.80]]

    for paso in [0.1, 0.01, 0.001]:
        capacidad, p = estimar_capacidad(canal, paso)
        print("Paso", paso, "-> C =", round(capacidad, 6),
              "bits/simbolo, con P(a1) =", round(p, 4))