import math

def extension_fuente(alfabeto, distribucion, N, nuevoAlfabeto, nuevaDistribucion):
    alf = ['']
    pro = [1]
    
    for x in range(N): #cada x++ es un orden
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

def InecuacionKraft(cod, listaALF):
    r = len(listaALF)
    aux = 0
    for x in cod:
        aux += r ** -len(x)
    return aux

def Listas(cod, listaALF, listaLong):

    long = len(cod)

    for x in cod:
        listaLong.append(len(x))
        long = len(x)
        for i in range(long):
            if x[i] not in listaALF:
                listaALF.append(x[i])       

def nosingular(cod):
    if(len(cod) != len(set(cod))):
        return False
    return True

def instantaneo(cod):    # IMPORTANTE LOS ELEMENTOS DE LA LISTA DEBEN ESTAR COMO STRING
    if(nosingular(cod)):  # Lo corroboro igual por si se utiliza fuera del main
        for i in range(len(cod)): # Un toque ineficiente pero no importa
            for j in range(len(cod)):
                if i != j: 
                    if cod[i].startswith(cod[j]):
                        return False # prefijo
    else:
        return False                
    return True 

def univocamente_decodificable(cod):

    if(nosingular(cod)):

        if(instantaneo(cod)): # Corroboro que sea singular y si es instantaneo devuelvo True
            return True
        
        C = set(cod)
        S1 = C 
        conjuntos_vistos = [] # Lista para ir guardando los S_i
        S_i = S1 

        while True: #Ciclo Infinito hasta que haya un return
            S_siguiente = set()
        
            for x in S1:
                for y in S_i:

                    if x != y:

                        if y.startswith(x):
                            sufijo = y[len(x):]
                            S_siguiente.add(sufijo)
                    
                        elif x.startswith(y):
                            sufijo = x[len(y):]
                            S_siguiente.add(sufijo)
        
                
            if not S_siguiente: # Si el conjunto de sufijos está vacio es UD.
                return True
            
                
            if S_siguiente & C: # Si algun S_i contiene una palabra de C, el código no es UD
                return False
            
                
            if S_siguiente in conjuntos_vistos: # Si se obtiene un S_i que ya aparecio antes, el código es UD
                return True
            
                
            conjuntos_vistos.append(S_siguiente) 
            S_i = S_siguiente


def Long_media(listaPro, listaLong):
    aux = 0
    for i in range(len(listaPro)):
        aux += listaPro[i] * listaLong[i]
    return aux


def Entropia(lista, listaInfo):
    i = 0
    entropia = 0
    for num in lista:
        entropia += num * listaInfo[i]
        i = i + 1
    return entropia

def Generolista (lista, listaInfo, listaALF):
    r = len(listaALF)
    for num in lista:
         listaInfo.append(math.log(1/num, r))

def Compacto(cod, listaInfo, listaLong):
    bool = True
    if(univocamente_decodificable(cod)):
        for i in range(len(listaInfo)):
            if(math.ceil(listaInfo[i]) < listaLong[i]):
                bool = False
                break

    return bool

def cumple_shannon(cod, pro, n, listaALF):
    nuevoCod = []
    nuevoPro = []
    listainfo = []
    extension_fuente(cod, pro, n, nuevoCod, nuevoPro)

    longitudes = []
    for palabra in nuevoCod:
        longitudes.append(len(palabra))

    Ln = Long_media(nuevoPro, longitudes)

    Generolista(nuevoPro, listainfo, listaALF)   # ahora r = 3
    h_extension = Entropia(nuevoPro, listainfo)
    h = h_extension / n

    print(f"n = {n}  |  H_{len(listaALF)}(S) = {h:.2f}  |  L{n} = {Ln:.2f}")

    cota_inferior = h - 1e-9
    cota_superior = h + 1 / n
    return cota_inferior <= Ln / n < cota_superior

cod = ["0", "100", "101", "11100", "110", "11101", "11110", "11111"]
listaPro = [0.512, 0.128, 0.128, 0.032, 0.128, 0.032, 0.032, 0.008 ]
print(cod)

if not nosingular(cod):
    print("Clasificacion: Codigo Bloque (Singular)")
else:
    if instantaneo(cod):
        print("Clasificacion: Instantaneo")
    else:
        if univocamente_decodificable(cod):
            print("Clasificacion: Univocamente Decodificable")
        else:
            print("Clasificacion: No Singular")

listaALF = []
listaLong = []
Listas(cod, listaALF, listaLong)
print("Lista alfabeto: ", listaALF)
print("Lista Li: ", listaLong)

kraft = InecuacionKraft(cod, listaALF)
print("Kraft: ", kraft)
if (univocamente_decodificable(cod)):
    listaInfo = []

    Generolista(listaPro, listaInfo, listaALF)
    entropia = Entropia(listaPro, listaInfo)
    print("Entropia de la Fuente: ", entropia)

    L_media = Long_media(listaPro, listaLong)

    print("Longitud media: ", L_media)

    if(Compacto(cod, listaInfo, listaLong)):
        print("Es Compacto")
    else:
        print("No es Compacto")

print("Cumple Shannon" if cumple_shannon(cod, listaPro, 1, listaALF) else "No cumple Shannon")
