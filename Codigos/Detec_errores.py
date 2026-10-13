def paridad_par(char):
    binario = bin(ord(char))
    binario = binario[2:] # Hago slicing para deshacerme de "0b"

    cant = 0
    for bit in binario:
        if(bit == '1'):
            cant += 1

    char_paridad = '1'
    if(cant % 2 == 0):
        char_paridad = '0'

    binario = binario + char_paridad
    return binario

def verificar(binario):
    cant = 0
    for i in range(len(binario) - 1):
        if(binario[i] == '1'):
            cant += 1

    char_paridad = '1'
    if(cant % 2 == 0):
        char_paridad = '0'

    return char_paridad == binario[len(binario) - 1]

if __name__ == "__main__":
    char = '/'
    binario = paridad_par(char)
    print("Binario con ultimo bit de paridad: ", binario)

    if(verificar(binario)):
        print("Correcto")
    else:
        print("Incorrecto")