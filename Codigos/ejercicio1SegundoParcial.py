from math import log2
 
# ---------------- DATOS DE ENTRADA (editar aca) --------------------------
MENSAJE = "GIIHGGGHGIHHIHIIGFHH"
ORDEN_EXTENSION = 3
# ---------------------------------------------------------------------------
 
 
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
 
 
def extension_fuente(alfabeto, distribucion, N, nuevoAlfabeto, nuevaDistribucion):
    alf = ['']
    pro = [1]
 
    for x in range(N):  # cada x++ es un orden
        alfTemp = []
        proTemp = []
        for i in range(len(alfabeto)):
            for j in range(len(alf)):
                alfTemp.append(alfabeto[i] + alf[j])
                proTemp.append(distribucion[i] * pro[j])
        alf = alfTemp
        pro = proTemp
 
    nuevoAlfabeto.extend(alf)
    nuevaDistribucion.extend(pro)
 

def huffman(probs):
    items = [[p, ""] for p in probs]
    codificar_huffman(sorted(items))
    return [code for _, code in items]
 
 
def codificar_huffman(items):
    # Caso base: quedan dos nodos, se asigna 0 y 1
    if len(items) == 1:
        items[0][1] = "0"
        return
    if len(items) == 2:
        items[0][1] = "0"
        items[1][1] = "1"
        return
 
    # Se toman los dos de menor probabilidad y se los combina en un nodo nuevo
    items = sorted(items, key=lambda x: x[0])
    a, b = items[0], items[1]
    nuevo = [a[0] + b[0], ""]
 
    # Llamada recursiva con la lista reducida
    codificar_huffman(items[2:] + [nuevo])
 
    # Al volver, el nodo combinado ya tiene su codigo:
    # los dos nodos que lo formaron lo extienden con 0 y 1
    a[1] = nuevo[1] + "0"
    b[1] = nuevo[1] + "1"
 
 
def metricas(probs, codigos):
    h = -sum(p * log2(p) for p in probs)                  # entropia
    l = sum(p * len(c) for p, c in zip(probs, codigos))   # longitud media
    n = h / l                                             # rendimiento
    return h, l, n, 1 - n                                 # redundancia = 1 - rendimiento
 
 
def codifico(cad, alfabeto, codigo):
    cod = ""
    for car in cad:
        cod += codigo[alfabeto.find(car)]
    return cod
 
 
def tasa_compresion(cadena_original, cadena_codificada):
    bits_originales = len(cadena_original) * 8            # ASCII: 8 bits por caracter
 
    bits_comprimidos = len(cadena_codificada)             # solo los codigos de los simbolos
 
    if bits_comprimidos == 0:
        return 0.0
 
    return bits_originales / bits_comprimidos
 
 
def cumple_shannon(h, L, N):
    promedio = L / N
    return h - 0.000000001 <= promedio and promedio < h + 1 / N
 
 
if __name__ == "__main__":
    print("Mensaje:", MENSAJE)

    # Probabilidades de los simbolos y entropia de la fuente
    
    alfabeto = []
    pro = []
    listas_paralelas(MENSAJE, alfabeto, pro)
 
    print("\nProbabilidades y entropia de la fuente")
    for s, p in zip(alfabeto, pro):
        print(f"   P({s}) = {p:.4f}")
 
    # Codigo binario optimo para la fuente (Huffman)

    codigo = huffman(pro)
    h, l, n, r = metricas(pro, codigo)
 
    print(f"   H2(S) = {h:.4f}")
 
    print("\nCodigo binario optimo para la fuente (Huffman)")
    print(f"   {'Simbolo':<8} {'Prob.':<10} Codigo")
    for s, p, c in zip(alfabeto, pro, codigo):
        print(f"   {s:<8} {p:<10.4f} {c}")
 
    # Tasa de compresion 
    
    mensaje_codificado = codifico(MENSAJE, "".join(alfabeto), codigo)
    tasa = tasa_compresion(MENSAJE, mensaje_codificado)
 
    print("\nTasa de compresion")
    print(f"   Bits originales: {len(MENSAJE) * 8}")
    print(f"   Bits codificados: {len(mensaje_codificado)}")
    print(f"   Tasa de compresion = {tasa:.4f} : 1")
 
    # Codigo binario optimo para la extension de orden 3 (Huffman)
    
    alfabeto_ext = []
    pro_ext = []
    extension_fuente(alfabeto, pro, ORDEN_EXTENSION, alfabeto_ext, pro_ext)
    codigo_ext = huffman(pro_ext)
 
    print(f"\nCodigo binario optimo para la extension de orden {ORDEN_EXTENSION} (Huffman)")
    print(f"   {len(alfabeto_ext)} simbolos de {ORDEN_EXTENSION} caracteres")
    print(f"   {'Simbolo':<8} {'Prob.':<10} Codigo")
    for s, p, c in zip(alfabeto_ext, pro_ext, codigo_ext):
        print(f"   {s:<8} {p:<10.4f} {c}")
 
    
    # Longitud media, rendimiento y redundancia de cada codigo

    h_ext, l_ext, n_ext, r_ext = metricas(pro_ext, codigo_ext)
 
    print("\nLongitud media, rendimiento y redundancia")
    print("   Codigo para la fuente:")
    print(f"      L = {l:.4f}")
    print(f"      η = {n:.4f}")
    print(f"      R = {r:.4f}")
    print(f"   Codigo para la extension de orden {ORDEN_EXTENSION}:")
    print(f"      L = {l_ext:.4f}   (bits por simbolo de la extension)")
    print(f"      η = {n_ext:.4f}")
    print(f"      R = {r_ext:.4f}")
 
    
    # Primer Teorema de Shannon:  H(S) <= L_N / N < H(S) + 1/N
    
    print("\nPrimer Teorema de Shannon")
    for N, L_N, nombre in [(1, l, "Fuente"), (ORDEN_EXTENSION, l_ext, "Extension")]:
        cumple = cumple_shannon(h, L_N, N)
        print(f"   {nombre} (N = {N}): {h:.4f} <= {L_N / N:.4f} < {h + 1 / N:.4f}  ->  "
              f"{'Cumple' if cumple else 'No cumple'}")
 