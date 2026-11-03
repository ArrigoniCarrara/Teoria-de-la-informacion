import math

def Listas(cod, listaALF, listaLong):
    for x in cod:
        listaLong.append(len(x))
        for i in range(len(x)):
            if x[i] not in listaALF:
                listaALF.append(x[i])


def Long_media(listaPro, listaLong):
    aux = 0
    for i in range(len(listaPro)):
        aux += listaPro[i] * listaLong[i]
    return aux


def Entropia(lista, listaInfo):
    i = 0
    entropia = 0
    for num in lista:
        entropia += num * listaInfo[i]
        i = i + 1
    return entropia


def Generolista(lista, listaInfo, listaALF):
    r = len(listaALF)
    for num in lista:
        listaInfo.append(math.log(1 / num, r))


def rendimiento_redundancia(pro, cod):
    listaALF = []
    listaLong = []
    Listas(cod, listaALF, listaLong)

    # Entropia de la fuente en base r
    listaInfo = []
    Generolista(pro, listaInfo, listaALF)
    h = Entropia(pro, listaInfo)

    # Longitud media del codigo
    L = Long_media(pro, listaLong)

    # Rendimiento y redundancia
    rendimiento = h / L
    redundancia = 1 - rendimiento

    print("  r =", len(listaALF))
    print("  H_r(S) =", round(h, 4))
    print("  L =", round(L, 4))

    return rendimiento, redundancia


if __name__ == "__main__":
    pro = [0.2, 0.15, 0.1, 0.3, 0.25]
    cod = ["01", "111", "110", "101", "100"]

    n, R = rendimiento_redundancia(pro, cod)

    print("Rendimiento (n) =", round(n, 4))
    print("Redundancia (R) =", round(R, 4))