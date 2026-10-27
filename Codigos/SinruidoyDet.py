def sinruido(matriz, n, m):
    for j in range(m):
        x = 0
        for i in range(n):
            if(matriz[i][j] != 0):
                if(x != 0):
                    return 0
                else:
                    x += 1
    return 1

def determinante(matriz, n, m):
    for i in range(n):
            x = 0
            for j in range(m):
                if(matriz[i][j] != 0):
                    if(x != 0):
                        return 0
                    else:
                        x += 1
    return 1   

if __name__ == "__main__":
    matriz = [[0, 1, 0],
              [0, 0, 1],
              [0, 1, 0],
              [1, 0, 0]]
    m = 3
    n = 4

    if(sinruido(matriz, n, m)):
        print("Es un canal con ruido")

    if(determinante(matriz, n, m)):
        print("Es un canal determinante")