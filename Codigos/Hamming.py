import math

def hamming(cod):
    longitud = len(cod[0])
    dif_min = longitud    # la distancia máxima posible es la longitud

    for i in range(len(cod)):
        cad_actual = cod[i]
        for j in range(i + 1, len(cod)):     # j empieza en i + 1
            dif_j = 0
            for pos_car in range(longitud):
                if cod[j][pos_car] != cad_actual[pos_car]:
                    dif_j += 1

            if dif_j < dif_min:
                dif_min = dif_j
    return dif_min

def cant_errores(dh):
    if(dh > 0):
        return dh - 1
    return 0

def cant_correcciones(dh):
    if(dh > 0):
        return math.floor((dh - 1)/ 2)
    return 0


if __name__ == "__main__":
    cod = ["0110000","0000011", "0101101", "0100110"]
    distancia_hamming = hamming(cod)
    print("Distancia de Hamming: ", distancia_hamming)
    print("Se pueden detectar ", cant_errores(distancia_hamming), " errores")
    print("Se pueden corregir ", cant_correcciones(distancia_hamming), " errores")