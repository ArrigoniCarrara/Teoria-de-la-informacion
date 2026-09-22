import math 
from Fuente_montecarlo import Montecarlo
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

def Generolista (lista, listaInfo):
    r = len(listaALF)
    print("T(Pi): ")
    for num in lista:
         listaInfo.append(math.log(1/num, r))
         print("I(", num, ") = ", math.log(1/num, r))

def Compacto(cod, listaInfo, listaLong):
    bool = True
    if(univocamente_decodificable(cod)):
        for i in range(len(listaInfo)):
            if(math.ceil(listaInfo[i]) < listaLong[i]):
                bool = False
                break

    return bool

cod = [".,", ";", ",,", ":", "...", ",:;"]
listaPro = [0.10, 0.5, 0.10, 0.20, 0.05, 0.05]
print(cod)

if(nosingular(cod)):
    print("Es No Singular")
    if(instantaneo(cod)):
        print("Es Univocamente Decodificable")
        print("Es Instantaneo")
    else:
        if(univocamente_decodificable(cod)):
            print("Es Univocamente Decodificable")
        else:
            print("No es Univocamente Decodificable")
        print("No es Instantaneo")
else:
    print("Es Singular")


listaALF = []
listaLong = []
Listas(cod, listaALF, listaLong)
print("Lista alfabeto: ", listaALF)
print("Lista Li: ", listaLong)

kraft = InecuacionKraft(cod, listaALF)
print("Kraft: ", kraft)
if (univocamente_decodificable(cod)):
    listaInfo = []

    Generolista(listaPro, listaInfo)
    entropia = Entropia(listaPro, listaInfo)
    print("Entropia de la Fuente: ", entropia)

    L_media = Long_media(listaPro, listaLong)

    print("Longitud media: ", L_media)

    if(Compacto(cod, listaInfo, listaLong)):
        print("Es Compacto")
    else:
        print("No es Compacto")

n = int(input())
prediccion = []
Montecarlo(n, cod, listaPro, prediccion)
print(prediccion)