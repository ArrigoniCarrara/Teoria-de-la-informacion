def comprimir_rlc(mensaje):
    resultado = bytearray()
    i = 0
    while i < len(mensaje):
        caracter = mensaje[i]
        cantidad = 1
        # Cuento cuántas veces se repite seguido el mismo carácter 
        while i + cantidad < len(mensaje) and mensaje[i + cantidad] == caracter and cantidad < 255:
            cantidad += 1
        resultado.append(ord(caracter))  
        resultado.append(cantidad)       
        i += cantidad
    return resultado


def rlc_a_texto(comprimido):
    texto = ""
    for i in range(0, len(comprimido), 2):
        caracter = chr(comprimido[i])
        cantidad = comprimido[i + 1]
        texto += caracter + str(cantidad)
    return texto


if __name__ == "__main__":
    mensaje = "UUOOOOAAAIEUUUU"
    comprimido = comprimir_rlc(mensaje)
    print("Mensaje original:", mensaje)
    print("Cadena RLC:", rlc_a_texto(comprimido))  
    print("Bytearray:", list(comprimido))          # [97, 3, 98, 1, 99, 2, 100, 5]