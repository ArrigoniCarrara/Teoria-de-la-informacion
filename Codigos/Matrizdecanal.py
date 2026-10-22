def listas_paralelas(cadena, listaALF, listaPro):
    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char) / long)

    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0]))  # Ordeno los eventos para mayor comodidad

    listaALF.clear()
    listaPro.clear()

    for char, pro in parejas_ordenadas:
        listaALF.append(char)
        listaPro.append(pro)


def proba(cad, sal, car_ent, alfSalida):
    cantidades = [0 for _ in range(len(alfSalida))]
    for i in range(len(cad)):
        if cad[i] == car_ent:
            cantidades[alfSalida.index(sal[i])] += 1
    deno = sum(cantidades)
    return [c / deno for c in cantidades]


def generoMC(mat, n, m, cad, sal, alfEntrada, alfSalida):
    for poscar in range(n):
        fila = proba(cad, sal, alfEntrada[poscar], alfSalida)
        for j in range(m):
            mat[poscar][j] = fila[j]


if __name__ == "__main__":
    cadenaEntrada = "1101011001101010010101010100011111"
    cadenaSalida = "1001111111100011101101010111110110"

    alfEntrada = []
    proEntrada = []
    listas_paralelas(cadenaEntrada, alfEntrada, proEntrada)

    alfSalida = []
    proSalida = []
    listas_paralelas(cadenaSalida, alfSalida, proSalida)

    n = len(alfEntrada)   # cantidad de símbolos de entrada
    m = len(alfSalida)    # cantidad de símbolos de salida

    matriz = [[0 for _ in range(m)] for _ in range(n)]

    generoMC(matriz, n, m, cadenaEntrada, cadenaSalida, alfEntrada, alfSalida)

    print("Alfabeto entrada:", alfEntrada, "Probabilidades a priori:", proEntrada)
    print("Alfabeto salida:", alfSalida, "Probabilidades salida:", proSalida)
    for i in range(n):
        print(alfEntrada[i], matriz[i])