from math import log2

def entropia(valores):
    h = 0
    for p in valores:
        if p > 0:
            h = h - p * log2(p)
    return h


def es_uniforme(canal):
    primera = sorted(canal[0])

    for fila in canal:
        actual = sorted(fila)
        for k in range(len(primera)):
            diferencia = abs(primera[k] - actual[k])
            if diferencia > 0.000001:
                return False
    return True


def es_determinante(canal):
    for fila in canal:
        cantidad_no_nulos = 0
        for p in fila:
            if p > 0:
                cantidad_no_nulos = cantidad_no_nulos + 1
                if abs(p - 1) > 0.000001:
                    return False
        if cantidad_no_nulos != 1:
            return False
    return True


def es_sin_ruido(canal):
    if not es_determinante(canal):
        return False

    n = len(canal)
    m = len(canal[0])
    if n != m:
        return False

    for j in range(m):
        unos_en_columna = 0
        for i in range(n):
            if canal[i][j] > 0:
                unos_en_columna = unos_en_columna + 1
        if unos_en_columna != 1:
            return False
    return True


def capacidad_determinante(canal):
    # C = log2(m_utiles), con m_utiles = columnas que tienen al menos un 1
    n = len(canal)
    m = len(canal[0])
    utiles = 0

    for j in range(m):
        columna_usada = False
        for i in range(n):
            if canal[i][j] > 0:
                columna_usada = True
        if columna_usada:
            utiles = utiles + 1

    return log2(utiles)


def capacidad_sin_ruido(canal):
    # C = log2(n)
    n = len(canal)
    return log2(n)


def capacidad_uniforme(canal):
    # C = log2(m) - H(fila)
    m = len(canal[0])
    h_fila = entropia(canal[0])
    return log2(m) - h_fila


def tipos_de_canal(canal):
    # Devuelve una lista con TODOS los tipos que cumple el canal
    tipos = []
    if es_sin_ruido(canal):
        tipos.append("sin ruido")
    if es_determinante(canal):
        tipos.append("determinante")
    if es_uniforme(canal):
        tipos.append("uniforme")
    return tipos


def capacidad_por_tipo(canal, tipo):
    if tipo == "sin ruido":
        return capacidad_sin_ruido(canal)
    if tipo == "determinante":
        return capacidad_determinante(canal)
    return capacidad_uniforme(canal)

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
            if canal[i][j] > 0 and pb[j] > 0:
                termino = pa[i] * canal[i][j] * log2(canal[i][j] / pb[j])
                info = info + termino
    return info


def capacidad_general(canal):
    mejor_p = 0.5
    mejor_info = -1

    desde = 0.1
    hasta = 0.9
    paso = 0.1

    for ronda in range(6):
        print("  Ronda", ronda + 1, ": p de", round(desde, 6), "a", round(hasta, 6),
              "con paso", paso)

        p = desde
        while p <= hasta + 0.0000001:
            pa = [p, 1 - p]
            info = informacion_mutua(canal, pa)
            if info > mejor_info:
                mejor_info = info
                mejor_p = p
            p = p + paso

        print("    Mejor hasta ahora: p =", round(mejor_p, 6),
              " I =", round(mejor_info, 6))

        desde = mejor_p - paso
        hasta = mejor_p + paso
        paso = paso / 10
        if desde < 0:
            desde = 0
        if hasta > 1:
            hasta = 1

    return mejor_p, mejor_info


def analizar(nombre, canal):
    print("Canal:", nombre)

    tipos = tipos_de_canal(canal)

    if len(tipos) > 0:
        print("  Cumple los tipos:", tipos)
        for tipo in tipos:
            c = capacidad_por_tipo(canal, tipo)
            print("  Capacidad como", tipo, ":", round(c, 4), "bits/simbolo")
    else:
        print("  No es sin ruido, determinante ni uniforme")
        if len(canal) == 2:
            p, c = capacidad_general(canal)
            print("  Capacidad:", round(c, 4), "bits/simbolo, con p(x1) =", round(p, 4))
        else:
            print("  Esta busqueda solo esta hecha para canales de 2 entradas")
    print()


if __name__ == "__main__":
    analizar("Ejercicio",
             [[0.8, 0.1, 0.1],
              [0.4, 0.6, 0.0],
              [0.2, 0.3, 0.5]])