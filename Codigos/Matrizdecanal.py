def listas_paralelas(cadena, listaALF, listaPro):
    long = len(cadena)

    for char in cadena:
        if char not in listaALF:
            listaALF.append(char)
            listaPro.append(cadena.count(char) / long)

    parejas_ordenadas = sorted(zip(listaALF, listaPro), key=lambda x: ord(x[0])) # Ordeno los eventos para mayor comodidad (en el orden que corresponda)

    listaALF.clear()
    listaPro.clear()

    for char, pro in parejas_ordenadas:
        listaALF.append(char)
        listaPro.append(pro)

def proba(cad, cod, car):
    cant_0 = 0
    cant_1 = 0
    for i in range(len(cad)):
        if car == cad[i]:
            if cod[i] == 0:
                cant_0 = cant_0 + 1
            else:
                cant_1 = cant_1 + 1
    

def generoMC(mat, n,cad, cod, pro, alf):
    m = 2 # Codigo binario
    for poscar in range(n):
        cant_0, cant_1 = proba(cad, cod, alf[poscar])
        mat[poscar][0] = cant_0
        mat[poscar][1] = cant_1

if __name__ == "__main__":
    cadenafuente = "abcacaabbcacaabcacaaabcaca"
    codigo = "01010110011001000100010011"
    listaALF = []
    listaPro = []
    listas_paralelas(cadenafuente, listaALF, listaPro)
    matriz = [[]]
    n = len(listaALF)

    for i in range(n):
        for j in range(2):
            matriz[i][j] = 0

    generoMC(matriz, n,cadenafuente, codigo, listaPro, listaALF)
    print(matriz)