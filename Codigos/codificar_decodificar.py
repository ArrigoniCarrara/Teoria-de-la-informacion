import Huffman
def codifico(cad, alfabeto, codigo):
    cod = ""
    for car in cad:
        cod += codigo[alfabeto.find(car)] 
    return cod

def decodifico(cad_codificada, alfabeto, codigo):
    decod = ""      
    aux = ""     # Acumulador temporal de bits
    
    for bit in cad_codificada:
        aux += bit
        
        if aux in codigo:
            # Busco en que posicion esta ese codigo
            indice = codigo.index(aux)
            # Concateno la letra directamente al string final
            decod += alfabeto[indice]
            aux = ""
            
    return decod

def tasa_compresion(cadena_original, cadena_codificada): # NO VEO QUE ESTO ESTE EXPLICADO
    bits_originales = len(cadena_original) * 8 
    
    bits_comprimidos = len(cadena_codificada)
    
    if bits_comprimidos == 0:
        return 0.0
        
    return bits_originales / bits_comprimidos
    
if __name__ == "__main__":
    cad = "HOLA"
    alfabeto = " ,.:;ABCDEFGHIJKLMNÑOQRSTUVWXYZ"  
    pro = [
    0.175990, 0.014093, 0.015034, 0.000542, 0.002109, 0.111066, 0.015368, 0.030176,
    0.038747, 0.101604, 0.004873, 0.008762, 0.007953, 0.049740, 0.003706, 0.000034, 
    0.048149, 0.021041, 0.050490, 0.002018, 0.073793, 0.019583, 0.010246, 0.051446, 
    0.058406, 0.031093, 0.033240, 0.008930, 0.000012, 0.000706, 0.007851, 0.003199  ]

    codigo = Huffman.huffman(pro)
    for i in range(len(alfabeto)):
        print(alfabeto[i], pro[i], codigo[i])

    cad_codificada = codifico(cad, alfabeto, codigo) 
    print("Cadena codificada: ", cad_codificada)

    cad_decodificada = decodifico(cad_codificada, alfabeto, codigo)
    print("Cadena Decodificada: ", cad_decodificada)
    print(cad == cad_decodificada)

    tasa = tasa_compresion(cad, cad_codificada)
    print(f"Tasa de compresión: {tasa:.2f}") 