def compuesto(canal1, n1, m1, canal2, n2, m2):
    if m1 != n2:
        print("Las columnas del canal 1 deben ser iguales a las filas del canal 2")

    resultado = [[0.0] * m2 for _ in range(n1)]

    for i in range(n1):            
        for j in range(m2):        
            for k in range(m1):    
                resultado[i][j] += canal1[i][k] * canal2[k][j]

    return resultado


if __name__ == "__main__":
    canal1 = [[0.7, 0.0, 0.3, 0.0],
              [0.2, 0.6, 0.0, 0.2]]

    canal2 = [[0.9, 0.0, 0.1],
              [0.0, 1.0, 0.0],
              [0.1, 0.1, 0.8],
              [0.0, 0.5, 0.5]]

    n1 = len(canal1)
    m1 = len(canal1[0])    # corregido: antes decía len(canal2[0])

    n2 = len(canal2)
    m2 = len(canal2[0])

    for fila in compuesto(canal1, n1, m1, canal2, n2, m2):
        print([round(p, 4) for p in fila])