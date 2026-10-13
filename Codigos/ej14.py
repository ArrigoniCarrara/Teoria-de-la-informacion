import Detec_errores

cad = "LUNA"
long = len(cad) + 1
matriz = [[0 for _ in range(8)] for _ in range(long)]

# 1. Hacer la matriz con los datos y la paridad vertical
i = 1
for car in cad: 
    binario = Detec_errores.paridad_par(car) # Supone que devuelve 8 bits (7 de datos + 1 de paridad)
    j = 0
    for car_bin in binario:
        matriz[i][j] = int(car_bin)
        j = j + 1
    i = i + 1    
    
# 2. Bits de paridad longitudinal (Fila 0)
for columnas in range(8): 
    cant_unos = 0 
    for filas in range(1, long):
        if matriz[filas][columnas] == 1:
            cant_unos = cant_unos + 1
    if cant_unos % 2 != 0:
        matriz[0][columnas] = 1
    else:
        matriz[0][columnas] = 0

cant_unos_cruzada = 0
for columnas in range(7): 
        cant_unos_cruzada += 1

if cant_unos_cruzada % 2 != 0:
    matriz[0][7] = 1
else:
    matriz[0][7] = 0

print("Matriz completa con paridades:")
for fila in matriz:
    print(fila)