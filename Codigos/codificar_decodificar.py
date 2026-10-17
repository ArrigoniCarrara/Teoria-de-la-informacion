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

    
if __name__ == "__main__":
    cad = "ABACBAACABA"
    alfabeto = "ABC"   
    codigo = ["111", "10", "0"] 
    
    cad_codificada = codifico(cad, alfabeto, codigo) 
    print("Cadena codificada: ", cad_codificada)

    cad_decodificada = decodifico(cad_codificada, alfabeto, codigo)
    print("Cadena Decodificada: ", cad_decodificada)
    print(cad == cad_decodificada)