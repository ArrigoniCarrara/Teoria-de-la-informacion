import math

def extension_fuente(alfabeto, distribucion, N, nuevoAlfabeto, nuevaDistribucion):
    alf = ['']
    pro = [1]

    for x in range(N):  # cada x++ es un orden
        alfTemp = []
        proTemp = []
        for i in range(len(alfabeto)):
            for j in range(len(alf)):
                alfTemp.append(alfabeto[i] + alf[j])
                proTemp.append(distribucion[i] * pro[j])
        alf = alfTemp
        pro = proTemp

    nuevoAlfabeto.extend(alf)
    nuevaDistribucion.extend(pro)


def InecuacionKraft(cod, listaALF):
    r = len(listaALF)
    aux = 0
    for x in cod:
        aux += r ** -len(x)
    return aux


def Listas(cod, listaALF, listaLong):
    for x in cod:
        listaLong.append(len(x))
        for i in range(len(x)):
            if x[i] not in listaALF:
                listaALF.append(x[i])


def nosingular(cod):
    if len(cod) != len(set(cod)):
        return False
    return True


def instantaneo(cod):  # LOS ELEMENTOS DE LA LISTA DEBEN SER STRINGS
    if nosingular(cod):
        for i in range(len(cod)):
            for j in range(len(cod)):
                if i != j:
                    if cod[i].startswith(cod[j]):
                        return False  # prefijo
    else:
        return False
    return True


def univocamente_decodificable(cod):
    if nosingular(cod):

        if instantaneo(cod):
            return True

        C = set(cod)
        S1 = C
        conjuntos_vistos = []
        S_i = S1

        while True:
            S_siguiente = set()

            for x in S1:
                for y in S_i:
                    if x != y:
                        if y.startswith(x):
                            sufijo = y[len(x):]
                            S_siguiente.add(sufijo)
                        elif x.startswith(y):
                            sufijo = x[len(y):]
                            S_siguiente.add(sufijo)

            if not S_siguiente:  # conjunto de sufijos vacio: es UD
                return True

            if S_siguiente & C:  # algun sufijo es palabra del codigo: no es UD
                return False

            if S_siguiente in conjuntos_vistos:  # se repitio un S_i: es UD
                return True

            conjuntos_vistos.append(S_siguiente)
            S_i = S_siguiente
    return False


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


def Compacto(cod, listaInfo, listaLong):
    bool = True
    if univocamente_decodificable(cod):
        for i in range(len(listaInfo)):
            if math.ceil(listaInfo[i]) < listaLong[i]:
                bool = False
                break
    return bool


def cumple_shannon(pro, cod, N, es_extension=False):
    # pro: distribucion de la fuente original
    # cod: si es_extension es False -> codigo ORIGINAL (la extension se arma sola)
    #      si es_extension es True  -> palabras de la extension de orden N (ya hechas)
    # N:   orden de la extension

    if not univocamente_decodificable(cod):
        return False

    listaALF = []
    listaLong = []
    Listas(cod, listaALF, listaLong)

    # Nombres de los simbolos de la extension y sus probabilidades
    simbolos = []
    for i in range(len(pro)):
        simbolos.append("s" + str(i + 1))
    nombres = []
    nuevoPro = []
    extension_fuente(simbolos, pro, N, nombres, nuevoPro)

    if es_extension:
        if len(cod) != len(pro) ** N:
            print("Hacen falta len(pro) ** N palabras codigo")
            return False
        nuevoCod = cod
    else:
        nuevoCod = []
        otraPro = []
        extension_fuente(cod, pro, N, nuevoCod, otraPro)

    longitudes = []
    for palabra in nuevoCod:
        longitudes.append(len(palabra))

    print("  Simbolo  Prob.  Palabra codigo  Li")
    for i in range(len(nombres)):
        print("  ", nombres[i], round(nuevoPro[i], 4), nuevoCod[i], longitudes[i])

    Ln = Long_media(nuevoPro, longitudes)

    listaInfo = []
    Generolista(pro, listaInfo, listaALF)
    h = Entropia(pro, listaInfo)

    promedio = Ln / N
    cota_inferior = h
    cota_superior = h + 1 / N

    print("  N =", N)
    print("  r =", len(listaALF))
    print("  H_r(S) =", round(h, 4))
    print("  L_N =", round(Ln, 4))
    print("  L_N / N =", round(promedio, 4))
    print("  Cota:", round(cota_inferior, 4), "<= L_N/N <", round(cota_superior, 4))

    cumple_inferior = promedio >= cota_inferior - 0.000000001
    cumple_superior = promedio < cota_superior
    return cumple_inferior and cumple_superior


if __name__ == "__main__":

    # ---------- Parte 1: clasificacion de un codigo ----------
    cod = ["11", "010", "00"]
    listaPro = [0.5, 0.2, 0.3]
    print(cod)

    if not nosingular(cod):
        print("Clasificacion: Codigo Bloque (Singular)")
    else:
        if instantaneo(cod):
            print("Clasificacion: Instantaneo")
        else:
            if univocamente_decodificable(cod):
                print("Clasificacion: Univocamente Decodificable")
            else:
                print("Clasificacion: No Singular")

    listaALF = []
    listaLong = []
    Listas(cod, listaALF, listaLong)
    print("Lista alfabeto: ", listaALF)
    print("Lista Li: ", listaLong)

    kraft = InecuacionKraft(cod, listaALF)
    print("Kraft: ", kraft)

    if univocamente_decodificable(cod):
        listaInfo = []
        Generolista(listaPro, listaInfo, listaALF)
        entropia = Entropia(listaPro, listaInfo)
        print("Entropia de la Fuente: ", entropia)

        L_media = Long_media(listaPro, listaLong)
        print("Longitud media: ", L_media)

        if Compacto(cod, listaInfo, listaLong):
            print("Es Compacto")
        else:
            print("No es Compacto")

    # ---------- Parte 2: Primer Teorema de Shannon ----------
    print()
    print("===== Primer Teorema de Shannon =====")

    ordenes = [1, 2]   

    for N in ordenes:
        if N == 1:
            print("Codigo original (sin extension)")
        else:
            print("Extension de orden", N)
        print("Cumple Shannon:", cumple_shannon(listaPro, cod, N))
        print()

    # Uso de funcion cuando ya nos dan la extension de orden n
    pro = [0.5, 0.2, 0.3]
    C1 = ["11", "010", "00"]
    C2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]

    print("C1 (orden 1):")
    print("Cumple Shannon:", cumple_shannon(pro, C1, 1))
    print()

    print("C2 (extension de orden 2):")
    print("Cumple Shannon:", cumple_shannon(pro, C2, 2, True))